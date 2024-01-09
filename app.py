from website import create_app
from flask import redirect, url_for, flash

app = create_app()

@app.errorhandler(404)
def page_not_found(code=404):
    flash(message=("404 - Page Not Found!", "You requested a page that does not exist on our server!"), category="danger")
    return redirect(url_for("all_routes.index"))

if __name__ == "__main__":
    app.run(debug=True, port="5000", host="0.0.0.0")