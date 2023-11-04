from datetime import datetime, timedelta
import os
import scoutingutil
from scoutingutil import Column, Table, SheetsService

PRE_MATCH = "PRE_MATCH"
MATCH = "MATCH"
POST_MATCH = "POST_MATCH"

START = "start"
END = "end"
END_AUTO = "end-auto"

HEIGHT_LEVELS = "ABCDEFGHIJ"

MATCH_INPUT_NAMES = ("score", "move", "launch", "pickup", "dropped",
                    "defend", "steal", "stolen")

sheets_api = SheetsService()

def init_sheets_api():
    if not os.path.isfile(scoutingutil.configs.CONFIG_PATH):
        raise FileNotFoundError("Must create a config.json file to read from.")
    cnfg = scoutingutil.configs.load()
    sheets_api.config(cnfg)

def parse_isodate(dstr:str):
    return datetime.fromisoformat(dstr.replace("Z", "+00:00"))

def prep_data(data:dict[str]):
    if END_AUTO not in data:
        new_end = parse_isodate(data[START])+timedelta(seconds=45)
        #get which one happened earlier (auto cannot end after the match has ended)
        data[END_AUTO] = min(new_end, parse_isodate(data[END]))
    for name in MATCH_INPUT_NAMES:
        if isinstance(data[name], list):
            data[name] = [parse_isodate(dtstr) for dtstr in data[name] if isinstance(dtstr, str)]

#data processing functions

def count_auto(ctx:scoutingutil.ProcessingContext):
    if ctx.data is None:
        return
    end_auto = parse_isodate(ctx.raw[END_AUTO])
    for dt in ctx.data:
        if dt > end_auto:
            return
        yield dt

def count_teleop(ctx:scoutingutil.ProcessingContext):
    if ctx.data is None:
        return
    end_auto = parse_isodate(ctx.raw[END_AUTO])
    for dt in ctx.data:
        if dt > end_auto:
            yield dt


class ScoutingData(Table):
    "Data on one robot's performance in a match."
    
    #prematch
    robot = Column("ROBOT", "robot")
    team = Column("TEAM", "team")
    date = Column("DATE", "date")
    match = Column("MATCH", "match")
    scouter = Column("SCOUTER", "scouter")
    #auto
    goal_scores_auto = Column("GOAL SCORES AUTO", "score", process_data=lambda ctx: sum(1 for _ in count_auto(ctx)))
    moves_auto = Column("MOVES AUTO", "move", process_data=lambda ctx: sum(1 for _ in count_auto(ctx)))
    moves_throw_auto = Column("MOVES THROW AUTO", "launch", process_data=lambda ctx: sum(1 for _ in count_auto(ctx)))
    load_pickup_auto = Column("LOAD PICKUP AUTO", "pickup", process_data=lambda ctx: sum(1 for _ in count_auto(ctx)))
    dropped_auto = Column("DROPPED AUTO", "dropped", process_data=lambda ctx: sum(1 for _ in count_auto(ctx)))
    defends_auto = Column("DEFENDS AUTO", "defend", process_data=lambda ctx: sum(1 for _ in count_auto(ctx)))
    #teleop
    goal_scores = Column("GOAL SCORES", "score", process_data=lambda ctx: sum(1 for _ in count_teleop(ctx)))
    moves = Column("MOVES", "move", process_data=lambda ctx: sum(1 for _ in count_teleop(ctx)))
    moves_throw = Column("MOVES THROW", "launch", process_data=lambda ctx: sum(1 for _ in count_teleop(ctx)))
    load_pickup = Column("LOAD PICKUP", "pickup", process_data=lambda ctx: sum(1 for _ in count_teleop(ctx)))
    dropped = Column("DROPPED", "dropped", process_data=lambda ctx: sum(1 for _ in count_teleop(ctx)))
    defends = Column("DEFENDS", "defend", process_data=lambda ctx: sum(1 for _ in count_teleop(ctx)))
    goal_steals = Column("GOAL STEALS", "steal", process_data=lambda ctx: sum(1 for _ in count_teleop(ctx)))
    goal_stolen = Column("GOAL STOLEN", "stolen", process_data=lambda ctx: sum(1 for _ in count_teleop(ctx)))
    #postmatch
    height = Column("HEIGHT", "height", process_data=lambda ctx: HEIGHT_LEVELS[int(ctx.data)] if str(ctx.data).isdigit() else "")
    is_win = Column("IS WIN", "iswin", process_data=lambda ctx: ctx.data == "yes")
    comments = Column("COMMENTS", "comments")
