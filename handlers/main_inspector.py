import json
import logging
from copy import deepcopy
from typing import Tuple, Dict, Any, Set

import azure.functions as func
from pydantic import BaseModel, ValidationError

from chains import gamemaster_chain
from models.inspector_model import JsonInput, JsonOutput

from chains.inspector_chain import inspector_chain
from chains.gamemaster_chain import gamemaster_chain

def inspector(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger: inspector')

    try:
        # Debug: vérifier si on reçoit bien quelque chose
        logging.info(f"Request method: {req.method}")
        logging.info(f"Request headers: {dict(req.headers)}")

        body_json = req.get_json()
        logging.info(f"Raw JSON received: {body_json}")
        logging.info(f"JSON type: {type(body_json)}")

        if body_json is None:
            logging.error("get_json() returned None")
            return func.HttpResponse("No JSON data received", status_code=400)

        scenario_model = JsonInput(**body_json)
        logging.info("JsonInput model created successfully")

        if is_wildcard_been_used(scenario_model):
            logging.info("Wildcard has been used, invoking gamemaster chain")
            gamemaster_result = gamemaster_chain.invoke(scenario_model)
            merged_dict = deep_merge_dicts(deepcopy(body_json), gamemaster_result.model_dump())
            scenario_model = JsonInput(**merged_dict)
            body_json = merged_dict
            logging.info("Gamemaster chain invoked successfully, scenario model updated to %s", scenario_model)

        x_marked_fields, censored_body = extract_nested_fields_by_description(
            body_json,
            scenario_model,
            '[X]'
        )
        logging.info(f"Extracted [X] fields: {list(x_marked_fields.keys())}")

        result = inspector_chain.invoke(censored_body)
        merged_result_dict = merge_extracted_fields(result.model_dump(), body_json)
        merged_result = JsonOutput(**merged_result_dict)

        return func.HttpResponse(merged_result.model_dump_json(), mimetype="application/json", status_code=200)

    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return func.HttpResponse(f"Invalid JSON: {str(e)}", status_code=400)
    except ValidationError as e:
        logging.error(f"Pydantic validation error: {e}")
        return func.HttpResponse(f"Validation error: {str(e)}", status_code=400)
    except Exception as e:
        logging.error(f"Error main_inspector: {e}")
        logging.error(f"Exception type: {type(e)}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        return func.HttpResponse(f"An error occurred! {str(e)}", status_code=500)

def deep_merge_dicts(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge `update` into `base`."""
    merged = deepcopy(base)

    for key, value in update.items():
        if (
            key in merged and
            isinstance(merged[key], dict) and
            isinstance(value, dict)
        ):
            merged[key] = deep_merge_dicts(merged[key], value)
        else:
            merged[key] = deepcopy(value)

    return merged


def is_wildcard_been_used(scenario_model: JsonInput) -> bool:
    """
    Check if the inspector has used a wildcard tool in the scenario model.

    Args:
        scenario_model: The scenario model containing the dialogue and tools used.

    Returns:
        bool: True if a wildcard tool was used, False otherwise.
    """
    for inspector_wildcards in scenario_model.scenario.inspector_wildcards:
        if inspector_wildcards.use_tool:
            return True
    return False

def extract_fields_by_description_prefix(data: Dict[str, Any], model_class: BaseModel, prefix: str = '[X]') -> Tuple[
    Dict[str, Any], Dict[str, Any]]:
    """
    Extract fields from JSON data based on Pydantic model field descriptions that start with a prefix

    Args:
        data: JSON data dict
        model_class: Pydantic model class to inspect for field descriptions
        prefix: Prefix to look for in field descriptions (e.g., '[X]')

    Returns:
        extracted: Dict with fields that have descriptions starting with prefix
        remaining: Dict with remaining fields
    """
    # Get field names that have descriptions starting with the prefix
    fields_to_extract = get_fields_with_description_prefix(model_class, prefix)

    # Extract those fields from the data
    extracted = {}
    remaining = deepcopy(data)

    for field_name in fields_to_extract:
        if field_name in data:
            extracted[field_name] = data[field_name]
            remaining.pop(field_name, None)

    return extracted, remaining


def get_fields_with_description_prefix(model_class: BaseModel, prefix: str) -> Set[str]:
    """
    Get field names from a Pydantic model where the description starts with a specific prefix

    Args:
        model_class: Pydantic model class
        prefix: Prefix to search for in descriptions

    Returns:
        Set of field names that match the criteria
    """
    matching_fields = set()

    # Get the model's field info
    logging.info("Checking model class for fields with description prefix")

    fields_info = model_class.model_fields
    for field_name, field_info in fields_info.items():
        # logging.info(f"Checking field {field_name}")
        description = getattr(field_info, 'description', None)
        # logging.info(f"Field {field_name} description: {description}")
        if description and description.startswith(prefix):
            matching_fields.add(field_name)

    return matching_fields


def extract_nested_fields_by_description(data: Dict[str, Any], model_class: BaseModel, prefix: str = '[X]') -> Tuple[
    Dict[str, Any], Dict[str, Any]]:
    """
    Recursively extract fields based on description prefix, handling nested Pydantic models

    Args:
        data: JSON data dict
        model_class: Root Pydantic model class
        prefix: Prefix to look for in field descriptions

    Returns:
        extracted: Dict with all fields (including nested) that match the prefix
        remaining: Dict with remaining fields
    """
    extracted = {}
    remaining = deepcopy(data)

    def recursive_extract(current_data, current_model, path=""):
        if not isinstance(current_data, dict) or not current_model:
            return

        # Get fields for current model level
        fields_to_extract = get_fields_with_description_prefix(current_model, prefix)

        # Extract matching fields at current level
        for field_name in fields_to_extract:
            if field_name in current_data:
                full_path = f"{path}.{field_name}" if path else field_name
                extracted[full_path] = current_data[field_name]

                # Remove from remaining data
                if path:
                    # Navigate to nested location and remove
                    remove_nested_field(remaining, full_path)
                else:
                    remaining.pop(field_name, None)

        # Process nested models
        if hasattr(current_model, 'model_fields'):
            # Pydantic v2
            fields_info = current_model.model_fields
            for field_name, field_info in fields_info.items():
                if field_name in current_data and field_name not in fields_to_extract:
                    # Get the field type
                    field_type = field_info.annotation

                    # Handle nested BaseModel
                    if isinstance(field_type, type) and issubclass(field_type, BaseModel):
                        new_path = f"{path}.{field_name}" if path else field_name
                        recursive_extract(current_data[field_name], field_type, new_path)

                    # Handle List[BaseModel]
                    elif hasattr(field_type, '__origin__') and field_type.__origin__ is list:
                        list_item_type = field_type.__args__[0] if field_type.__args__ else None
                        if list_item_type and isinstance(list_item_type, type) and issubclass(list_item_type,
                                                                                              BaseModel):
                            if isinstance(current_data[field_name], list):
                                for i, item in enumerate(current_data[field_name]):
                                    new_path = f"{path}.{field_name}.{i}" if path else f"{field_name}.{i}"
                                    recursive_extract(item, list_item_type, new_path)

    recursive_extract(data, model_class)
    return extracted, remaining


def remove_nested_field(data, path):
    """Remove a field from nested dict using dot notation path"""
    keys = path.split('.')
    current = data
    for i, key in enumerate(keys[:-1]):
        if isinstance(current, dict):
            current = current.get(key, {})
        elif isinstance(current, list) and key.isdigit():
            idx = int(key)
            if 0 <= idx < len(current):
                current = current[idx]
            else:
                logging.warning(f"Index {idx} out of bounds for list at path {'.'.join(keys[:i+1])}")
                return  # out of bounds
        else:
            logging.warning(f"Invalid path segment '{key}' at path {'.'.join(keys[:i+1])}")
            return  # path invalid

    # Remove the final key
    final_key = keys[-1]
    if isinstance(current, dict):
        current.pop(final_key, None)
    elif isinstance(current, list) and final_key.isdigit():
        idx = int(final_key)
        if 0 <= idx < len(current):
            current.pop(idx)

def merge_extracted_fields(base_data: Dict[str, Any], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge extracted fields back into base data

    Args:
        base_data: Base data dict
        extracted_data: Extracted fields to merge back

    Returns:
        Merged data dict
    """
    result = deepcopy(base_data)

    for path, value in extracted_data.items():
        logging.info(f"Setting field {path} to value *silenced*")
        set_nested_field(result, path, value)

    return result


def set_nested_field(data, path, value):
    """Set a field in nested dict using dot notation path"""
    keys = path.split('.')
    current = data

    # Navigate to parent, creating dicts as needed
    for key in keys[:-1]:
        if key.isdigit():
            # Handle array index
            idx = int(key)
            if not isinstance(current, list):
                current = []
            while len(current) <= idx:
                current.append({})
            current = current[idx]
        else:
            if key not in current:
                current[key] = {}
            current = current[key]

    # Set final value
    final_key = keys[-1]
    if final_key.isdigit() and isinstance(current, list):
        idx = int(final_key)
        while len(current) <= idx:
            current.append(None)
        current[idx] = value
    else:
        current[final_key] = value