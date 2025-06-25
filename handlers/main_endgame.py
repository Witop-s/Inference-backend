import logging
import azure.functions as func
from chains.endgame_chain import endgame_chain

def endgame(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger: inner-voice')

    try:
        body_json = req.get_json()
        result = endgame_chain.invoke(body_json)
        return func.HttpResponse(result.model_dump_json(), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("An error occurred.", status_code=500)
