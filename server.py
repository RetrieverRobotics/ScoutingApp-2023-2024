import data_collection
from flask import Flask, redirect, url_for
from markupsafe import Markup
import match_scout
import pit_scout
import waitress

app = Flask(__name__)
app.url_map.strict_slashes = False
app.jinja_env.globals["include_file"] = lambda filename : Markup(app.jinja_loader.get_source(app.jinja_env, filename)[0])

@app.get("/")
def index():
    return redirect(url_for("match_scout.index"))

def main():
    #register blueprints
    app.register_blueprint(match_scout.bp)
    app.register_blueprint(pit_scout.bp)

    #init image keeping stuffs
    pit_scout.init_folder()
    pit_scout.init_json()

    #init sheets api
    #data_collection.init_sheets_api() DEBUG

    waitress.serve(app, host="0.0.0.0", port=80, threads=48)

if __name__ == "__main__":
    main()