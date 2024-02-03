from flask import jsonify
from . import api


@api.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "page not found"}), 404


@api.app_errorhandler(500)
def server_error(e):
    return jsonify({"error": "server error"})

@api.app_errorhandler(405)
def invalid_method(e):
    return jsonify({"error": "invalid method"})