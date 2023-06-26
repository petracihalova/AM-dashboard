from flask import Flask

import routes


def create_app():
    new_app = Flask(__name__)
    new_app.config.from_object("config")

    new_app.add_url_rule("/", view_func=routes.overview)
    new_app.add_url_rule("/services", view_func=routes.services)
    new_app.add_url_rule("/open_pr", view_func=routes.open_pr)
    new_app.add_url_rule("/release_notes/<id>", view_func=routes.release_notes)

    return new_app


app = create_app()
