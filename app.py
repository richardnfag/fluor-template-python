import json

from componentize_py_types import Err
from wit_world import exports
from wit_world.exports.handler import Error, ErrorCode, Header, Response


class Handler(exports.Handler):
    def handle(self, request: exports.handler.Request) -> Response:
        request_id = header_value(request.headers, "x-request-id")
        if request.method == "GET":
            return list_items(request, request_id)
        if request.method == "POST":
            return create_item(request, request_id)
        if request.method == "PUT":
            return update_item(request, request_id)
        if request.method == "DELETE":
            return delete_item(request, request_id)
        raise Err(Error(ErrorCode.BAD_REQUEST, f"method {request.method} is not supported"))


def list_items(request, request_id):
    name = query_param(request.query, "name")
    items = ["notebook", "pencil"]
    if name is not None:
        if name not in items:
            raise Err(Error(ErrorCode.NOT_FOUND, f"item {name} was not found"))
        items = [name]
    return respond(
        200,
        request_id,
        {
            "function": "{{project-name}}",
            "language": "python",
            "method": request.method,
            "path": request.path,
            "query": request.query,
            "requestId": request_id,
            "items": [{"name": item} for item in items],
        },
    )


def create_item(request, request_id):
    name = json_string_field(request.body, "name")
    if name is None:
        raise Err(Error(ErrorCode.BAD_REQUEST, "body must be a JSON object with a string name"))
    return respond(
        201,
        request_id,
        {
            "function": "{{project-name}}",
            "language": "python",
            "method": request.method,
            "path": request.path,
            "query": request.query,
            "requestId": request_id,
            "created": {"name": name},
        },
    )


def update_item(request, request_id):
    item_id = query_param(request.query, "id")
    if item_id is None:
        raise Err(Error(ErrorCode.BAD_REQUEST, "query parameter id is required"))
    if not request.body.lstrip().startswith("{"):
        raise Err(Error(ErrorCode.BAD_REQUEST, "body must be a JSON object"))
    return respond(
        200,
        request_id,
        {
            "function": "{{project-name}}",
            "language": "python",
            "method": request.method,
            "path": request.path,
            "query": request.query,
            "requestId": request_id,
            "updated": {"id": item_id, "body": json.loads(request.body)},
        },
    )


def delete_item(request, request_id):
    item_id = query_param(request.query, "id")
    if item_id is None:
        raise Err(Error(ErrorCode.BAD_REQUEST, "query parameter id is required"))
    return respond(
        200,
        request_id,
        {
            "function": "{{project-name}}",
            "language": "python",
            "method": request.method,
            "path": request.path,
            "query": request.query,
            "requestId": request_id,
            "deleted": item_id,
        },
    )


def respond(status, request_id, payload):
    headers = [Header(name="content-type", value="application/json")]
    if request_id is not None:
        headers.append(Header(name="x-request-id", value=request_id))
    return Response(status=status, headers=headers, body=json.dumps(payload))


def header_value(headers, name):
    for header in headers:
        if header.name.lower() == name:
            return header.value
    return None


def query_param(query, key):
    if query is None:
        return None
    for part in query.split("&"):
        name, separator, value = part.partition("=")
        if separator and name == key:
            return value
    return None


def json_string_field(body, field):
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        return None
    return value
