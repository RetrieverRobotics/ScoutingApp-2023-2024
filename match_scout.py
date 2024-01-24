import data_collection
from data_collection import PRE_MATCH, MATCH, POST_MATCH
from flask import abort, Blueprint, render_template, request
import json
import os

SUBMISSIONS_PATH = "submissions.txt"

def save_submission(*parts:str):
    submissions_file.write("["+",".join(parts)+"]\n")

bp = Blueprint(__name__, "match_scout", url_prefix="/scout/match")
submissions_file = open(SUBMISSIONS_PATH, "a" if os.path.isfile(SUBMISSIONS_PATH) else "w")

#PRE_MATCH
@bp.get("/")
def index():
    return render_template("match_index.html")

#MATCH
@bp.get("/during")
def match():
    return render_template("match_scout.html")

#POST_MATCH
@bp.get("/postmatch")
def postmatch():
    return render_template("match_post.html")

@bp.get("/confirm")
def confirm_submission():
    return render_template("match_confirm.html")

@bp.post("/submit")
def submit():
    if PRE_MATCH not in request.form or MATCH not in request.form or POST_MATCH not in request.form:
        abort(400, "Something went wrong while collecting data.")
    
    pre_match = json.loads(request.form[PRE_MATCH])
    match = json.loads(request.form[MATCH])
    post_match = json.loads(request.form[POST_MATCH])

    save_submission(request.form[PRE_MATCH], request.form[MATCH], request.form[POST_MATCH])

    data = {**pre_match, **match, **post_match}

    data_collection.prep_data(data)
    row = data_collection.ScoutingData.process_data(data)
    data_collection.sheets_api.save_to_sheets(row)

    return "Success", 200
