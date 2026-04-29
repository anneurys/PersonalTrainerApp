from datetime import date
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Weekly workout plan: 0 = Monday ... 4 = Friday
WEEK_PLAN = {
    0: {  # Monday - Day 1
        "title": "Day 1 – Push (Chest & Shoulders Priority)",
        "exercises": [
            {"name": "Barbell Bench Press", "sets": "4", "reps": "6–8"},
            {"name": "Incline Dumbbell Press", "sets": "3", "reps": "8–10"},
            {"name": "Seated Overhead Press", "sets": "3", "reps": "6–8"},
            {"name": "Dumbbell Lateral Raises", "sets": "4", "reps": "12–15"},
            {"name": "Rope Overhead Tricep Extension", "sets": "3", "reps": "10–12"},
            {"name": "Push-Ups (pump finisher)", "sets": "2", "reps": "to failure"},
        ],
    },
    1: {  # Tuesday - Day 2
        "title": "Day 2 – Pull (Back Width Priority)",
        "exercises": [
            {"name": "Weighted Pull-Ups (wide grip)", "sets": "4", "reps": "6–8"},
            {"name": "Barbell Row", "sets": "3", "reps": "8–10"},
            {"name": "Lat Pulldown (neutral or underhand)", "sets": "3", "reps": "10–12"},
            {"name": "Face Pulls", "sets": "3", "reps": "12–15"},
            {"name": "Incline Dumbbell Curls", "sets": "3", "reps": "10–12"},
            {"name": "Hammer Curls", "sets": "2", "reps": "12–15"},
        ],
    },
    2: {  # Wednesday - Day 3
        "title": "Day 3 – Legs + Abs",
        "exercises": [
            {"name": "Barbell Back Squat", "sets": "3", "reps": "6–8"},
            {"name": "Romanian Deadlift", "sets": "3", "reps": "8–10"},
            {"name": "Walking Lunges", "sets": "2", "reps": "10 each leg"},
            {"name": "Standing Calf Raises", "sets": "3", "reps": "12–15"},
            {"name": "Hanging Leg Raises", "sets": "3", "reps": "12–15"},
            {"name": "Cable Woodchoppers", "sets": "3", "reps": "12–15/side"},
            {"name": "Plank", "sets": "3", "reps": "30–45s"},
        ],
    },
    3: {  # Thursday - Day 4
        "title": "Day 4 – Push (Shoulders & Upper Chest Priority)",
        "exercises": [
            {"name": "Incline Barbell Bench Press", "sets": "4", "reps": "6–8"},
            {"name": "Arnold Press", "sets": "3", "reps": "8–10"},
            {"name": "Dumbbell Lateral Raises (superset with pushups)", "sets": "4", "reps": "12–15"},
            {"name": "Low Incline Dumbbell Flyes", "sets": "3", "reps": "10–12"},
            {"name": "Close-Grip Bench Press", "sets": "3", "reps": "8–10"},
            {"name": "Rope Tricep Pushdowns", "sets": "2", "reps": "12–15"},
        ],
    },
    4: {  # Friday - Day 5
        "title": "Day 5 – Pull (Back Thickness + Abs)",
        "exercises": [
            {"name": "Weighted Chin-Ups", "sets": "4", "reps": "6–8"},
            {"name": "Single-Arm Dumbbell Row", "sets": "3", "reps": "8–10"},
            {"name": "Chest-Supported Row", "sets": "3", "reps": "10–12"},
            {"name": "Rear Delt Flyes", "sets": "3", "reps": "12–15"},
            {"name": "Barbell Curl", "sets": "3", "reps": "8–10"},
            {"name": "Cable Curl", "sets": "2", "reps": "12–15"},
            {"name": "Weighted Decline Sit-Ups", "sets": "3", "reps": "12–15"},
            {"name": "Ab Wheel Rollouts", "sets": "3", "reps": "8–10"},
        ],
    },
}

def get_db_connection():
    conn = sqlite3.connect('personal_trainer.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/workouts')
def workouts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT workout_date, exercise, sets, reps
        FROM workouts
        ORDER BY workout_date
    """)
    rows = cur.fetchall()
    conn.close()
    return render_template('workouts.html', workouts=rows)

@app.route('/today')
def today_workout():
    weekday_index = date.today().weekday()  # 0=Mon ... 6=Sun
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    if weekday_index in WEEK_PLAN:
        plan = WEEK_PLAN[weekday_index]
        return render_template(
            'today.html',
            weekday=weekday_names[weekday_index],
            title=plan["title"],
            exercises=plan["exercises"]
        )
    else:
        # Saturday or Sunday: rest day
        return render_template(
            'today.html',
            weekday=weekday_names[weekday_index],
            title="Rest / Recovery Day",
            exercises=[]
        )

@app.route('/add', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        workout_date = request.form['workout_date']
        exercise = request.form['exercise']
        sets = request.form['sets']
        reps = request.form['reps']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO workouts (workout_date, exercise, sets, reps) VALUES (?, ?, ?, ?)",
            (workout_date, exercise, sets, reps)
        )
        conn.commit()
        conn.close()

        # after saving, go back to workouts page
        return redirect(url_for('workouts'))

    # if GET, just show the empty form
    return render_template('add_workout.html')

if __name__ == '__main__':
    app.run(debug=True)
