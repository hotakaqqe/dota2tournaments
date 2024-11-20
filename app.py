from flask import Flask, render_template, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, static_folder='static')

def create_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dota2_tournaments"
        )
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/api/tournaments')
def get_tournaments():
    db = create_db_connection()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, start_date, end_date, prize_pool, winner FROM tournaments")
        tournaments = cursor.fetchall()
    finally:
        db.close()

    return jsonify([
        {
            'name': tournament['name'],
            'start_date': tournament['start_date'],
            'end_date': tournament['end_date'],
            'prize_pool': tournament['prize_pool'],
            'winner': tournament['winner']
        }
        for tournament in tournaments
    ])

@app.route('/api/teams')
def get_teams():
    db = create_db_connection()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, country, roster, logo FROM teams")
        teams = cursor.fetchall()
    finally:
        db.close()

    return jsonify([
        {
            'name': team['name'],
            'country': team['country'],
            'roster': team['roster'],
            'logo': team['logo']
        }
        for team in teams
    ])

@app.route('/')
def home():
    db = create_db_connection()
    if db is None:
        return "Error: Unable to connect to the database", 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tournaments")
        tournaments = cursor.fetchall()
    finally:
        db.close()

    return render_template("index.html", tournaments=tournaments)

@app.route('/teams')
def teams_page():
    db = create_db_connection()
    if db is None:
        return "Error: Unable to connect to the database", 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, country, roster, logo FROM teams")
        teams = cursor.fetchall()
    finally:
        db.close()

    return render_template("teams.html", teams=teams)

from flask_cors import CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
    