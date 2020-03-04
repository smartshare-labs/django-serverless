import importlib
import json

from flask import Flask, request, abort, Response

app = Flask(__name__)


@app.route("/<function_name>", methods=["POST"])
def _route(function_name):
    test_event = request.get_json()
    if not test_event:
        test_event = {}

    test_event["headers"] = request.headers

    url_path = function_name.replace("-", "_")
    test_context = {}

    try:
        module_path = f"functions.{url_path}.handler"
        handler_module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        abort(404)

    response = handler_module.handler(test_event, test_context)
    return Response(
        response["body"], status=response["statusCode"], mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
