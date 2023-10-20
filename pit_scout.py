from datetime import datetime, timezone
from flask import abort, Blueprint, render_template, request, send_file
import json
import os
import string

ID_INC_MAX = 999
IMAGE_PATH = "images"
JSON_PATH = "images.json"

bp = Blueprint(__name__, "pit_scout", url_prefix="/scout/pit")
_id_inc = 0

def init_folder():
    "Create image folder if it doesn't exist. Returns True if the folder had to be made, else False."
    if not os.path.isdir(IMAGE_PATH):
        os.mkdir(IMAGE_PATH)
        return True
    return False

def init_json():
    if not os.path.isfile(JSON_PATH):
        with open(JSON_PATH, "w") as f:
            f.write("{}")
        return True
    return False

def get_team_designations(team:str):
    with open(JSON_PATH) as f:
        data:dict[str, dict[str, str]] = json.load(f)
    return data.get(team)

def set_team_designation(team:str, designation:str, path:str):
    with open(JSON_PATH) as f:
        data:dict[str, dict[str, str]] = json.load(f)
    
    if team in data:
        data[team][designation] = path
    else:
        data[team] = {designation:path}
    
    with open(JSON_PATH, "w") as f:
        json.dump(data, f)

def _id_incrament():
    global _id_inc
    if _id_inc == ID_INC_MAX:
        _id_inc = 0
    else:
        _id_inc += 1
    return _id_inc

def create_id():
    return int(datetime.now(timezone.utc).timestamp()*100) * (ID_INC_MAX+1) + _id_incrament()

@bp.get("/")
def index():
    return render_template("pit_index.html")

@bp.post("/submit")
def submit():
    if "team" not in request.form or "image" not in request.files:
        abort(400, "Make sure that request has field 'team' and has file 'image'.")
    
    team = request.form["team"]
    team_des = get_team_designations(team)
    if team_des is None:
        designation = "A"
    else:
        des = sorted(team_des)
        for des_letter, letter in zip(des, string.ascii_uppercase):
            if des_letter != letter:
                designation = letter
                break
        designation = string.ascii_uppercase[string.ascii_uppercase.index(letter)+1]

    image_file = request.files["image"]
    file_extension = image_file.filename.rsplit(".",1)[-1]
    filename = f"{create_id()}.{file_extension}"

    with open(os.path.join(IMAGE_PATH, filename), "wb") as f:
        image_file.save(f)

    set_team_designation(team, designation, filename)

    return "Success", 200

@bp.get("/get/robots")
def get_robots():
    if "team" not in request.args:
        abort(400, "Make sure that request has parameter 'team'.")
    team_des = get_team_designations(request.args["team"])
    return "[]" if team_des is None else json.dumps(sorted(team_des)), 200

@bp.get("/get/image")
def get_image():
    if "team" not in request.args and "designation" not in request.args:
        abort(400, "Make sure that request has fields 'team' and 'designation'.")
    team = request.args["team"]
    designation = request.args["designation"]
    team_des = get_team_designations(team)
    if team_des is None or designation not in team_des:
        abort(404, f"Team \"{team}\" does not have robot \"{designation}\".")
    return send_file(os.path.join(IMAGE_PATH, team_des[designation]))