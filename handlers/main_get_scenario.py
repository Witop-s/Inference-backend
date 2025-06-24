import json
import logging
import azure.functions as func
import os


def find_project_root(current_path):
    """Trouve la racine du projet en cherchant function_app.py ou host.json"""
    while current_path != os.path.dirname(current_path):  # Pas encore à la racine du système
        if (os.path.exists(os.path.join(current_path, 'function_app.py')) or
                os.path.exists(os.path.join(current_path, 'host.json'))):
            return current_path
        current_path = os.path.dirname(current_path)
    return None


def get_scenario(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger: get_scenario')

    # Get the scenario from query string instead of route
    scenario = req.params.get('scenario')
    if not scenario:
        logging.error('No scenario provided')
        return func.HttpResponse("Scenario not provided.", status_code=400)

    try:
        # Trouver la racine du projet
        current_file_dir = os.path.dirname(__file__)
        project_root = find_project_root(current_file_dir)

        if not project_root:
            logging.error('Could not find project root')
            return func.HttpResponse("Configuration error.", status_code=500)

        file_path = os.path.join(project_root, 'game', f'{scenario}.json')

        # Log du chemin pour debug
        logging.info(f'Project root: {project_root}')
        logging.info(f'Trying to read file: {file_path}')
        logging.info(f'File exists: {os.path.exists(file_path)}')

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return func.HttpResponse(
            json.dumps(data),
            status_code=200,
            mimetype="application/json"
        )

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return func.HttpResponse(f"Scenario '{scenario}' not found.", status_code=404)
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("An error occurred.", status_code=500)