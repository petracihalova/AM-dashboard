from flask import render_template


def overview():
    return render_template("overview.html", index=True)


def services():
    return render_template("services.html", index=True)


def open_pr():
    return render_template("open_pr.html", index=True)
