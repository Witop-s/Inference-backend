import logging
logging.warning("⚠️ function_app.py loaded")

import azure.functions as func

# Importer les handlers
try:
    from handlers.main_inner_voice import inner_voice
except Exception as e:
    logging.error(f"❌ inner_voice failed to import: {e}")

try:
    from handlers.main_fact_filter import inner_voice_fact_filter
except Exception as e:
    logging.error(f"❌ inner_voice_fact_filter failed to import: {e}")

try:
    from handlers.main_inspector import inspector
except Exception as e:
    logging.error(f"❌ inspector failed to import: {e}")

try:
    from handlers.main_get_scenario import get_scenario
except Exception as e:
    logging.error(f"❌ get_scenario failed to import: {e}")

try:
    from handlers.main_endgame import endgame
except Exception as e:
    logging.error(f"❌ endgame failed to import: {e}")

app = func.FunctionApp()

@app.function_name(name="ping")
@app.route(route="ping", auth_level=func.AuthLevel.ANONYMOUS)
def ping(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("ping called")
    return func.HttpResponse("pong", status_code=200)