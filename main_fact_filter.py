import logging
import azure.functions as func
from chains.fact_filter_chain import select_facts_chain

def inner_voice_fact_filter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger: inner-voice-fact-filter')

    try:
        body_json = req.get_json()
        ai_response = select_facts_chain.invoke(body_json)

        return func.HttpResponse(
            ai_response.content,
            status_code=200,
            mimetype="text/plain"
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            "An error occurred.",
            status_code=500
        )
