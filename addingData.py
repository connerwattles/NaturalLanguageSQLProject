import psycopg2
import os

CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

def insert_sample_data():
    with psycopg2.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            # Insert sample user
            cursor.execute("INSERT INTO Users (gender, age) VALUES (%s, %s) RETURNING id", ('Male', 25))
            user_id = cursor.fetchone()[0]

            # Insert sample muscle group
            cursor.execute("""
                INSERT INTO MuscleGroup (name, selectedBias, region, sizeConstant)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, ('Chest', 1.2, 'Upper Body', 5))
            muscle_group_id = cursor.fetchone()[0]

            # Insert sample diet
            cursor.execute("INSERT INTO Diet (type, multiplierValue) VALUES (%s, %s) RETURNING id", ('Cutting', 0.8))
            diet_id = cursor.fetchone()[0]

            # Insert sample equipment
            cursor.execute("INSERT INTO Equipment (name, type) VALUES (%s, %s) RETURNING id", ('Barbell', 'Barbell'))
            equipment_id = cursor.fetchone()[0]

            # Insert sample exercise
            cursor.execute("""
                INSERT INTO Exercise (name, requiredEquipment, repConstant, weightConstant, video)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, ('Bench Press', equipment_id, 10, 1.5, 'https://example.com/video'))
            exercise_id = cursor.fetchone()[0]

            # Insert sample workout
            cursor.execute("""
                INSERT INTO Workout (scheduledDate, durationMinutes, exercise_ids)
                VALUES (%s, %s, %s) RETURNING id
            """, ('2024-10-01', 60, [exercise_id]))
            workout_id = cursor.fetchone()[0]

            # Insert sample schedule
            cursor.execute("INSERT INTO Schedule (workouts) VALUES (%s) RETURNING id", ([workout_id],))
            schedule_id = cursor.fetchone()[0]

            # Insert sample program
            cursor.execute("""
                INSERT INTO Program (
                    selectedWorkoutDaysPerWeek,
                    experienceLevel,
                    selectedGoals,
                    selectedWorkoutTypes,
                    selectedWorkoutDuration,
                    selectedDiet,
                    selectedWeightUnit,
                    selectedDaysUntilNextWorkout
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (
                3,
                'Intermediate',
                ['Gain Strength'],
                ['Weightlifting'],
                60,
                diet_id,
                'Kgs',
                3
            ))
            program_id = cursor.fetchone()[0]

            conn.commit()

insert_sample_data()
