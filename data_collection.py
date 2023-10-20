import os
import scoutingutil
from scoutingutil import Column, Table, SheetsService

PRE_MATCH = "PRE_MATCH"
MATCH = "MATCH"
POST_MATCH = "POST_MATCH"

sheets_api = SheetsService()

def init_sheets_api():
    if not os.path.isfile(scoutingutil.configs.CONFIG_PATH):
        raise FileNotFoundError("Must create a config.json file to read from.")
    cnfg = scoutingutil.configs.load()
    sheets_api.config(cnfg)

#data processing functions

class ScoutingData(Table):
    "Data on one robot's performance in a match."
    
    robot = Column("ROBOT", "robot")
    team = Column("TEAM", "team")
    date = Column("DATE", "date")
    match = Column("MATCH", "match")
    scouter = Column("SCOUTER", "scouter")
    goal_scores_auto = Column("GOAL SCORES AUTO")
    goal_scores = Column("GOAL SCORES")
    moves_auto = Column("MOVES AUTO")
    moves = Column("MOVES")
    moves_throw_auto = Column("MOVES THROW AUTO")
    moves_throw = Column("MOVES THROW")
    load_pickup_auto = Column("LOAD PICKUP AUTO")
    load_pickup = Column("LOAD PICKUP")
    dropped_auto = Column("DROPPED AUTO")
    dropped = Column("DROPPED")
    goal_steals = Column("GOAL STEALS")
    goal_stolen = Column("GOAL STOLEN")
    height = Column("HEIGHT", "height", process_data=lambda ctx: int(ctx.data))
    is_win = Column("IS WIN", "TODO", process_data=lambda ctx: ctx.data == "yes")
    comments = Column("COMMENTS", "comments")
