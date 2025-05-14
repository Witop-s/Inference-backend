import azure.functions as func
import logging

app = func.FunctionApp()

@app.route(route="inner-voice", auth_level=func.AuthLevel.ANONYMOUS)
def inner_voice(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body_json = req.get_json()
        being_written_message = body_json['being_written_message']
        history = body_json['history']
    except:
        print("Incorrect request body")
        return func.HttpResponse("Incorrect request body", status_code=400)

    print(being_written_message)
    print(history)

    return func.HttpResponse(
         "This HTTP triggered function executed successfully.",
         status_code=200
    )