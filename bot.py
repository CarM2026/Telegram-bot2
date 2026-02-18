import requests
import telebot
import time
from datetime import datetime

# ====== CONFIGURACION ======
TOKEN = "8280541626:AAHrFhszKqt9GLQssGosOttyA4MyhV9zuGY"
CHAT_ID = -1003552307071
API_KEY = "123"

bot = telebot.TeleBot(TOKEN)

headers = {
    "x-apisports-key": API_KEY
}

# ====== FUNCIONES ======

def get_fixtures(league_id):
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&date={today}"
    response = requests.get(url, headers=headers)
    data = response.json()

    text = "\n📅 PARTIDOS DE HOY:\n"
    if data["response"]:
        for match in data["response"]:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            time_match = match["fixture"]["date"][11:16]
            text += f"{home} vs {away} - {time_match}\n"
    else:
        text += "No hay partidos hoy.\n"

    return text


def get_standings(league_id):
    url = f"https://v3.football.api-sports.io/standings?league={league_id}&season=2024"
    response = requests.get(url, headers=headers)
    data = response.json()

    text = "\n🏆 TABLA (Top 5):\n"
    try:
        standings = data["response"][0]["league"]["standings"][0][:5]
        for team in standings:
            position = team["rank"]
            name = team["team"]["name"]
            points = team["points"]
            text += f"{position}. {name} - {points} pts\n"
    except:
        text += "No disponible.\n"

    return text


def get_recent_results(league_id):
    url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&last=5"
    response = requests.get(url, headers=headers)
    data = response.json()

    text = "\n📊 ÚLTIMOS 5 PARTIDOS:\n"
    try:
        for match in data["response"]:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            goals_home = match["goals"]["home"]
            goals_away = match["goals"]["away"]
            text += f"{home} {goals_home}-{goals_away} {away}\n"
    except:
        text += "No disponible.\n"

    return text


def get_top_scorer(league_id):
    url = f"https://v3.football.api-sports.io/players/topscorers?league={league_id}&season=2024"
    response = requests.get(url, headers=headers)
    data = response.json()

    text = "\n⚽ GOLEADOR:\n"
    try:
        player = data["response"][0]
        name = player["player"]["name"]
        goals = player["statistics"][0]["goals"]["total"]
        text += f"{name} - {goals} goles\n"
    except:
        text += "No disponible.\n"

    return text


# ====== ENVIO AUTOMATICO ======

def send_daily_report():
    print("Enviando reporte...")

    # Premier League (ID 39)
    fixtures_pl = get_fixtures(39)
    standings_pl = get_standings(39)
    results_pl = get_recent_results(39)
    scorer_pl = get_top_scorer(39)

    message = "🇬🇧 PREMIER LEAGUE\n"
    message += fixtures_pl + standings_pl + results_pl + scorer_pl

    bot.send_message(chat_id=CHAT_ID, text=message)
    print("Mensaje enviado.")


# ====== LOOP ======

while True:
    send_daily_report()
    time.sleep(86400)  # 24 horas
