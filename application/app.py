from flask import Flask

import routes


def create_app():
    app = Flask(__name__)
    return app


app = create_app()

app.add_url_rule("/", view_func=routes.overview)
app.add_url_rule("/repos", view_func=routes.repos)
app.add_url_rule("/open_pr", view_func=routes.open_pr)
