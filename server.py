import data_collection
from flask import Flask, redirect, url_for
from markupsafe import Markup
import match_scout
import pit_scout
import sys
import waitress

app = Flask(__name__)
app.url_map.strict_slashes = False
app.jinja_env.globals["include_file"] = lambda filename : Markup(app.jinja_loader.get_source(app.jinja_env, filename)[0])

@app.get("/")
def index():
    return redirect(url_for("match_scout.index"))

def parse_args():
    l = len(sys.argv)
    rtv = {}
    i = 1
    while i < l:
        param = sys.argv[i]
        if param.lower() == "--port":
            i += 1
            rtv["port"] = sys.argv[i]
        i += 1
    return rtv

def main():
    #register blueprints
    app.register_blueprint(match_scout.bp)
    app.register_blueprint(pit_scout.bp)

    #init image keeping stuffs
    pit_scout.init_folder()
    pit_scout.init_json()

    #init sheets api
    data_collection.init_sheets_api()

    args = parse_args()

    try:
        waitress.serve(app, host="0.0.0.0", port=args.get("port", 80), threads=48)
    finally:
        match_scout.submissions_file.close()

if __name__ == "__main__":
    main()