from flask import Flask, render_template

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


# Error Middleware

@app.errorhandler(Exception)
def server_error(err):
    '''
    Catch and handle all unhandled exceptions.

    Unhandled exception = not catched by try + except block.
    '''
    app.logger.exception(err) # log the traceback
    return render_template("errors/error.html", error_msg="")  
