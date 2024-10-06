import psycopg2
import os

CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

def insert_sample_data():
    sample_data = [
        # Sample user
        ("INSERT INTO Users (gender, age) VALUES (%s, %s)", ('Male', 25)),
        
        # Sample muscle group
        ("INSERT INTO MuscleGroup (name, selectedBias, region, sizeConstant) VALUES (%s, %s, %s, %s)",
         ('Chest', 1.2, 'Upper Body', 5)),
        
        # Sample diet
        ("INSERT INTO Diet (type, multiplierValue) VALUES (%s, %s)", ('Cutting', 0.8)),
        
        # Sample equipment
        ("INSERT INTO Equipment (name, type) VALUES (%s, %s)", ('Barbell', 'Barbell')),
        
        # Sample exercise
        ("INSERT INTO Exercise (name, requiredEquipment, repConstant, weightConstant, video) VALUES (%s, %s, %s, %s, %s)",
         ('Bench Press', 1, 10, 1.5, 'https://example.com/video')),
        
        # Sample workout
        ("INSERT INTO Workout (scheduledDate, durationMinutes, exercise_ids) VALUES (%s, %s, %s)",
         ('2024-10-01', 60, '{1}')),
        
        # Sample schedule
        ("INSERT INTO Schedule (workouts) VALUES (%s)", ('{1}',)),
        
        # Sample program
        ("INSERT INTO Program (selectedWorkoutDaysPerWeek, experienceLevel, selectedGoals, selectedWorkoutTypes, selectedWorkoutDuration, selectedDiet, selectedWeightUnit, selectedDaysUntilNextWorkout) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
         (3, 'Intermediate', '{Gain Strength}', '{Weightlifting}', 60, 1, 'Kgs', 3))
    ]
    
    with psycopg2.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            for query, values in sample_data:
                cursor.execute(query, values)
            conn.commit()

insert_sample_data()
