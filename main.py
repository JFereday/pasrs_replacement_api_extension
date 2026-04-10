import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import functions_framework
from flask import jsonify

@functions_framework.http
def ping_check(request):
    """
    HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response object, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    return jsonify({"status": "success", "message": "Pong!"}), 200


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name('jf-pasrs-replacement-9ee60432cba1.json', scope)
client = gspread.authorize(creds)


def the_pasrs_func(game_id,your_username,google_sheet):
    url = f"https://replay.pokemonshowdown.com/{game_id}"
    page = requests.get(f"{url}.json")
    data = json.loads(page.text)

    player = "p2" if data["players"].index(your_username) == 1 else "p1"
    opponent = "p1" if data["players"].index(your_username) == 1 else "p2"
    opponent_username = data["players"][0] if data["players"].index(your_username) == 1 else data["players"][1]
    itemised_log = data["log"].split("\n")

    player_pokemon = list(dict.fromkeys([item.split('|')[3].split(',')[0] for item in itemised_log if f"switch|{player}a" in item]))
    player_moves = [item.split('|')[2:4] for item in itemised_log if f"move|{player}" in item]
    cleaned_moves = [[s.replace(f"{player}a: ", "").replace(f"{player}b: ", "") for s in sublist] for sublist in player_moves]
    player_tera_event = next((item for item in itemised_log if f"terastallize|{player}" in item),None)
    if player_tera_event:
        player_tera = player_tera_event.split(": ")[1].split("|")
    else:
        player_tera = ['','']

    opponent_pokemon = list(dict.fromkeys([item.split('|')[3].split(',')[0] for item in itemised_log if f"switch|{opponent}" in item]))
    opponent_tera_event = next((item for item in itemised_log if f"terastallize|{opponent}" in item),None)
    if opponent_tera_event:
        opponent_tera = opponent_tera_event.split(": ")[1].split("|")
    else:
        opponent_tera = ['','']

    winner = [item for item in itemised_log if "|win|" in item][0].split("|")[2]

    spreadsheet = client.open(google_sheet)

    try:
        sheet = spreadsheet.worksheet("pasrs-data")
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title="pasrs-data", rows="100", cols="10")
        sheet.append_row(["Replay","Opponent","Winner","Player Lead 1","Player Lead 2","Player Back 1","Player Back 2","Opponent Lead 1","Opponent Lead 2","Opponent Back 1","Opponent Back 2","Player Tera Mon","Player Tera Type","Oppponent Tera Mon","Oppponent Tera Type"])

    new_row = [url] + [opponent_username] + [winner] + player_pokemon + opponent_pokemon + player_tera + opponent_tera
    sheet.append_row(new_row)

@functions_framework.http
def my_extension_api(request):
    the_pasrs_func("gen9vgc2026regibo3-2577336831","brumisdumb","Nerd shit")

if __name__ == "__main__":
    the_pasrs_func("gen9vgc2026regibo3-2577336831","brumisdumb","Nerd shit")
