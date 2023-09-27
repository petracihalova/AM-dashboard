from flask import Flask

import routes


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    app.add_url_rule("/", view_func=routes.overview)
    app.add_url_rule("/deployments", view_func=routes.deployments)
    app.add_url_rule("/open_pr", view_func=routes.open_pr)
    app.add_url_rule("/release_notes/<id>", view_func=routes.release_notes)

    return app


app = create_app()
