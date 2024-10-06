import psycopg2
import os

CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            gender VARCHAR(10) CHECK(gender IN ('Male', 'Female')),
            age INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS MuscleGroup (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            selectedBias NUMERIC,
            region VARCHAR(20) CHECK(region IN ('Upper Body', 'Lower Body')),
            sizeConstant NUMERIC
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Diet (
            id SERIAL PRIMARY KEY,
            type VARCHAR(20) CHECK(type IN ('Cutting', 'Maintenance', 'Bulking')),
            multiplierValue NUMERIC
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Equipment (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            type VARCHAR(20) CHECK(type IN ('BodyWeight', 'Dumbbells', 'Machine', 'Barbell'))
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Exercise (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            requiredEquipment INT REFERENCES Equipment(id),
            repConstant NUMERIC,
            weightConstant NUMERIC,
            video VARCHAR(100)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Workout (
            id SERIAL PRIMARY KEY,
            scheduledDate DATE,
            durationMinutes INT,
            exercise_ids INT[]
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Schedule (
            id SERIAL PRIMARY KEY,
            workouts INT[]
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Program (
            id SERIAL PRIMARY KEY,
            selectedWorkoutDaysPerWeek INT,
            experienceLevel VARCHAR(20) CHECK(experienceLevel IN ('Beginner', 'Intermediate', 'Advanced')),
            selectedGoals VARCHAR(50)[],
            selectedWorkoutTypes VARCHAR(50)[],
            selectedWorkoutDuration INT,
            selectedDiet INT REFERENCES Diet(id),
            selectedWeightUnit VARCHAR(10) CHECK(selectedWeightUnit IN ('Kgs', 'Lbs')),
            selectedDaysUntilNextWorkout INT
        );
        """
    ]
    
    with psycopg2.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            for command in commands:
                cursor.execute(command)
            conn.commit()

create_tables()
