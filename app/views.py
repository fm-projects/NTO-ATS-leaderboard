from app import app
from flask import jsonify, render_template
import pandas as pd
import datetime
from typing import Union, Tuple


cache: Union[None, Tuple[datetime.timedelta, list]] = None


def get_task_scores(task: int):
    data = pd.read_html(f"https://sim.avt.global/public/{task}")[-1].iloc[:, :4]
    data.fillna("[NAN]", inplace=True)
    teams = [i for i in data["Команда"] if str(i) != "nan"]
    return (
        {i: max(data[data["Команда"] == i]["Очки"]) for i in teams},
        {i: list(data[data["Команда"] == i]["Участник"]) for i in teams},
    )


def get_leaderboard():
    response = []
    score, teams, teams_tasks = {}, {}, {}
    for i in ((100, 15), (101, 40), (102, 30), (103, 15)):
        data = get_task_scores(i[0])
        for j in data[0].items():
            teams[j[0]] = teams.get(j[0], set()) | set(list(data[1][j[0]]))
            score[j[0]] = score.get(j[0], 0) + i[1] * j[1]
            teams_tasks[j[0]] = teams_tasks.get(j[0], ["0"] * 4)
            teams_tasks[j[0]][i[0] % 10] = i[1] * j[1]
    response = [
        {
            "task_scores": teams_tasks[team],
            "team": team,
            "members": list(teams[team]),
            "score": score,
        }
        for team, score in score.items()
        if team != "_"
    ]
    return response


def cache_is_invalid():
    return not cache or (datetime.datetime.now() - cache[0]) > datetime.timedelta(
        minutes=5
    )


@app.route("/api/leaderboard")
def leaderboard():
    global cache
    if cache_is_invalid():
        cache = datetime.datetime.now(), get_leaderboard()
    response = jsonify({"data": cache[1]})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/")
def index():
    return render_template("index.html")
