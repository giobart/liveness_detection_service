from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from tools.img_tools import *
import traceback

import json

liveness_api = Blueprint('liveness_api', __name__)


@liveness_api.route('/liveness_check', methods=['POST'])
def add_face():
    req = request.json
    try:
        frames = req['frames']
        base64arr_to_tensor(frames)
        if check_liveness(base64arr_to_tensor(frames)):
            resp = jsonify({"result": True})
            return resp, 200
        else:
            resp = jsonify({"result": False})
            return resp, 200

    except Exception as e:
        traceback.print_exc()
        print(e)
        return "Internal server error: " + str(e), 500
