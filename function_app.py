import logging
logging.warning("⚠️ function_app.py loaded")

import azure.functions as func

# Importer les handlers
from functions.main_inner_voice import inner_voice
from functions.main_fact_filter import inner_voice_fact_filter
from functions.main_inspector import inspector
from functions.main_get_scenario import get_scenario
from functions.main_endgame import endgame

app = func.FunctionApp()

@app.function_name(name="ping")
@app.route(route="ping", auth_level=func.AuthLevel.ANONYMOUS)
def ping(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("ping called")
    return func.HttpResponse("pong", status_code=200)
