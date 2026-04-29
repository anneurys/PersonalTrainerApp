import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('personal_trainer.db')
cur = conn.cursor()

# Create workouts table
cur.execute('''
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_date TEXT NOT NULL,
    exercise TEXT NOT NULL,
    sets INTEGER NOT NULL,
    reps INTEGER NOT NULL
)
''')

# Add sample data
cur.execute("INSERT INTO workouts (workout_date, exercise, sets, reps) VALUES ('2025-11-02', 'Bench Press', 4, 8)")
cur.execute("INSERT INTO workouts (workout_date, exercise, sets, reps) VALUES ('2025-11-03', 'Lat Pulldown', 3, 10)")
cur.execute("INSERT INTO workouts (workout_date, exercise, sets, reps) VALUES ('2025-11-04', 'Squats', 4, 6)")

conn.commit()
conn.close()

print("Database initialized ✅")
