from flask import Flask
from controller import blueprints
from flask_cors import CORS
import os
from tools.model_tools import *

__all__ = ('create_app',)


def create_app(config=None, app_name='liveness_detection_service'):
    """
    Initializes the application and its utilities.
    """

    app = Flask(app_name, template_folder=os.path.join('templates'), static_folder=os.path.join('static'))
    CORS(app)

    if config:
        app.config.from_pyfile(config)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    model_init()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5007)
