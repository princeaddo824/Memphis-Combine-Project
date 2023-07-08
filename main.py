import pandas as pd
from flask import Flask, render_template, request
import csv

app = Flask(__name__)

PLAYER_NAMES = list(pd.read_csv("data/combine_data.csv").PLAYER)
POSITION = list(pd.read_csv("data/combine_data.csv").POS)

dict_player_info = {}

# converts the working data set into a dictionary.This provides an efficient and convenient way to access and display
# player's data

with open('data/combine_data.csv', 'r') as inp:
    reader = csv.reader(inp)
    dict_from_csv = {rows[1]: rows[1:] for rows in reader}
dict_player_info = dict_from_csv


# Route to the home page
@app.route('/')
def home():
    return render_template('index.html', player_names=dict_player_info)


# Route to the player information display page
@app.route('/player', methods=['POST'])
def profile():
    selected_name = request.form['department']
    return render_template('player.html', selected_name=selected_name, player_names=dict_player_info)


if __name__ == "__main__":
    app.run(debug=True)
