import logging
import azure.functions as func
from chains.alteration_chain import inner_voice_chain

def inner_voice(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger: inner-voice')

    try:
        body_json = req.get_json()
        result = inner_voice_chain.invoke(body_json)
        return func.HttpResponse(str(result), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("An error occurred.", status_code=500)
