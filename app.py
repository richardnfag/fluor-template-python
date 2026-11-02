import json
from wit_world import exports


class Handler(exports.Handler):
    def handle(self, request: exports.handler.Request) -> exports.handler.Response:
        return exports.handler.Response(
            status=200,
            headers=[
                exports.handler.Header(name="content-type", value="application/json"),
            ],
            body=json.dumps({"message": "Hello from {{project-name}}"}),
        )
