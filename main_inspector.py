import json
import logging
import azure.functions as func
from chains.inspector_chain import inspector_chain

def inspector(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger: inspector')

    try:
        body_json = req.get_json()
        result = inspector_chain.invoke(body_json)
        return func.HttpResponse(result.json(), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("An error occurred.", status_code=500)