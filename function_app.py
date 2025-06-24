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

@app.function_name(name="inner_voice")
@app.route(route="inner-voice", auth_level=func.AuthLevel.ANONYMOUS)
def inner_voice_func(req: func.HttpRequest) -> func.HttpResponse:
    return inner_voice(req)

@app.function_name(name="fact_filter")
@app.route(route="inner-voice-fact-filter", auth_level=func.AuthLevel.ANONYMOUS)
def fact_filter_func(req: func.HttpRequest) -> func.HttpResponse:
    return inner_voice_fact_filter(req)

@app.function_name(name="inspector")
@app.route(route="inspector", auth_level=func.AuthLevel.ANONYMOUS)
def inspector_func(req: func.HttpRequest) -> func.HttpResponse:
    return inspector(req)

@app.function_name(name="get_scenario")
@app.route(route="get-scenario", auth_level=func.AuthLevel.ANONYMOUS)
def get_scenario_func(req: func.HttpRequest) -> func.HttpResponse:
    return get_scenario(req)

@app.function_name(name="endgame")
@app.route(route="endgame", auth_level=func.AuthLevel.ANONYMOUS)
def endgame_func(req: func.HttpRequest) -> func.HttpResponse:
    return endgame(req)
