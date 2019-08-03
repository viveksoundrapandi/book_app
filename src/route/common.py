from flask import Blueprint, jsonify, current_app
from flask.ext.restful import Api


common_blueprint = Blueprint('common', __name__)
common_blueprint_api = Api(common_blueprint)


@common_blueprint.route('/')
def list_routes():
    output = []
    for rule in current_app.url_map.iter_rules():
        rule.methods.remove('HEAD')
        rule.methods.remove('OPTIONS')
        methods = ','.join(rule.methods)
        line = "{:50s} {:s}".format(str(rule), methods)
        output.append(line)
    return jsonify(routes=output)
