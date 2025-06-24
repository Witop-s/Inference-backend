import json
import logging
import azure.functions as func
import os

def get_scenario(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger: get_scenario')

    # Get the scenario from query string instead of route
    scenario = req.params.get('scenario')
    if not scenario:
        logging.error('No scenario provided')
        return func.HttpResponse("Scenario not provided.", status_code=400)

    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, 'game', f'{scenario}.json')

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return func.HttpResponse(json.dumps(data), status_code=200, mimetype="application/json")
    except FileNotFoundError:
        return func.HttpResponse(f"Scenario '{scenario}' not found.", status_code=404)
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("An error occurred.", status_code=500)
