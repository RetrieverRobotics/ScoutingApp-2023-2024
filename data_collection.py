from datetime import datetime, timedelta
import math
import os
import scoutingutil
from scoutingutil import Column, configs, Table, SheetsService
from typing import Generator

PRE_MATCH = "PRE_MATCH"
MATCH = "MATCH"
POST_MATCH = "POST_MATCH"

START = "start"
END = "end"
END_AUTO = "end-auto"
LAUNCH_FASTEST = "launch-fastest"
LAUNCH_SLOWEST = "launch-slowest"
LAUNCH_AVERAGE = "launch-average"

HEIGHT_LEVELS = ["Didn't climb", *"ABCDEFGHIJ"]

MATCH_INPUT_NAMES = ("score", "move", "launch", "pickup", "dropped",
                    "defend", "steal", "stolen")

sheets_api = SheetsService()

def init_sheets_api():
    if not os.path.isfile(scoutingutil.configs.CONFIG_PATH):
        raise FileNotFoundError("Must create a config.json file to read from.")
    cnfg = scoutingutil.configs.load()
    try:
        sheets_api.config(cnfg)
    except Exception as e:
        token_path = os.path.abspath(cnfg.get(configs.SHEETS_TOKEN_PATH, "token.json"))
        if os.path.isfile(token_path):
            os.remove(token_path)
            sheets_api.config(cnfg)
        else:
            raise

def parse_isodate(dstr:str):
    return datetime.fromisoformat(dstr.replace("Z", "+00:00"))

def iter_auto(data, raw:dict[str]):
    if data is None:
        return
    end_auto = raw[END_AUTO]
    for dt in data:
        if dt > end_auto:
            return
        yield dt

def iter_teleop(data, raw:dict[str]):
    if data is None:
        return
    end_auto = raw[END_AUTO]
    for dt in data:
        if dt > end_auto:
            yield dt

def prep_data(data:dict[str]):
    #set all iso datetime strings to datetime objects
    data[START] = parse_isodate(data[START])
    data[END] = parse_isodate(data[END])
    for name in MATCH_INPUT_NAMES:
        if isinstance(data[name], list):
            data[name] = [parse_isodate(dtstr) for dtstr in data[name] if isinstance(dtstr, str)]

    #determine end_auto time
    if data.get(END_AUTO) is None:
        new_end = data[START]+timedelta(seconds=45)
        #get which one happened earlier (auto cannot end after the match has ended)
        data[END_AUTO] = min(new_end, data[END])
    else:
        data[END_AUTO] = parse_isodate(data[END_AUTO])

    #calculate launch timings

    dts:Generator[datetime, None, None] = iter_teleop(data["launch"], data)
    deltas = []
    fast_delta = float("inf") #min
    slow_delta = 0 #max
    current:datetime = data[END_AUTO]

    for dt in dts:
        delta = (dt-current).total_seconds()
        if delta < fast_delta:
            fast_delta = delta
        if delta > slow_delta:
            slow_delta = delta
        current = dt
        deltas.append(delta)

    data[LAUNCH_FASTEST] = fast_delta
    data[LAUNCH_SLOWEST] = slow_delta
    data[LAUNCH_AVERAGE] = sum(deltas)/len(deltas)


#data processing functions

def count_column_auto(ctx:scoutingutil.ProcessingContext):
    return sum(1 for _ in iter_auto(ctx.data, ctx.raw))

def count_column_teleop(ctx:scoutingutil.ProcessingContext):
    return sum(1 for _ in iter_teleop(ctx.data, ctx.raw))

class ScoutingData(Table):
    "Data on one robot's performance in a match."
    
    #prematch
    robot = Column("ROBOT", "robot", lambda ctx: f"{ctx.raw['team']}-{ctx.data}")
    team = Column("TEAM", "team")
    date = Column("DATE", "date")
    match = Column("MATCH", "match", process_data=lambda ctx: int(ctx.data), strict=True)
    scouter = Column("SCOUTER", "scouter")
    #auto
    goal_scores_auto = Column("GOAL SCORES AUTO", "score", process_data=count_column_auto)
    moves_auto = Column("MOVES AUTO", "move", process_data=count_column_auto)
    moves_throw_auto = Column("LAUNCHES AUTO", "launch", process_data=count_column_auto)
    load_pickup_auto = Column("LOAD PICKUP AUTO", "pickup", process_data=count_column_auto)
    dropped_auto = Column("DROPPED AUTO", "dropped", process_data=count_column_auto)
    defends_auto = Column("DEFENDS AUTO", "defend", process_data=count_column_auto)
    #teleop
    goal_scores = Column("GOAL SCORES", "score", process_data=count_column_teleop)
    moves = Column("MOVES", "move", process_data=count_column_teleop)
    launches = Column("LAUNCHES", "launch", process_data=count_column_teleop)
    launch_fastest = Column("LAUNCH FASTEST", LAUNCH_FASTEST)
    launch_slowest = Column("LAUNCH SLOWEST", LAUNCH_SLOWEST)
    launch_average = Column("LAUNCH AVERAGE", LAUNCH_AVERAGE)
    load_pickup = Column("LOAD PICKUP", "pickup", process_data=count_column_teleop)
    dropped = Column("DROPPED", "dropped", process_data=count_column_teleop)
    defends = Column("DEFENDS", "defend", process_data=count_column_teleop)
    goal_steals = Column("GOAL STEALS", "steal", process_data=count_column_teleop)
    goal_stolen = Column("GOAL STOLEN", "stolen", process_data=count_column_teleop)
    #postmatch
    height = Column("HEIGHT", "height", process_data=lambda ctx: HEIGHT_LEVELS[math.ceil(int(ctx.data)/10)] if str(ctx.data).isdigit() else "")
    is_win = Column("IS WIN", "iswin", process_data=lambda ctx: ctx.data == "yes")
    comments = Column("COMMENTS", "comments")
