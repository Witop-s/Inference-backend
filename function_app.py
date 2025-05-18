import azure.functions as func

from dotenv import load_dotenv
load_dotenv()

# Importer les handlers
from main_inner_voice import inner_voice
from main_fact_filter import inner_voice_fact_filter

app = func.FunctionApp()

app.route(route="inner-voice", auth_level=func.AuthLevel.ANONYMOUS)(inner_voice)
app.route(route="inner-voice-fact-filter", auth_level=func.AuthLevel.ANONYMOUS)(inner_voice_fact_filter)
