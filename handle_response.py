from flask import make_response, jsonify, Response
from model.entity_error import Error

def HandleResponse(err: Error) -> tuple[Response, Error]:
    if err != None:
        return jsonify(err.error()), err.code()

    return make_response('', 200)

def HandleResponseWithBody(response: dict, err: Error) -> tuple[Response, Error]:
    if err != None:
        return jsonify(err.error()), err.code()

    return jsonify(response), 200