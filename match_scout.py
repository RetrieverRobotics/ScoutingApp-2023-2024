import data_collection
from data_collection import PRE_MATCH, MATCH, POST_MATCH
from flask import abort, Blueprint, render_template, request
import json

bp = Blueprint(__name__, "match_scout", url_prefix="/scout/match")

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

    row = data_collection.ScoutingData.process_data({**pre_match, **match, **post_match})
    data_collection.sheets_api.save_to_sheets(row)

    