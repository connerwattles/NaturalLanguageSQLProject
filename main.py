import psycopg2
from openai import OpenAI
import os

client = OpenAI()

client.api_key = os.getenv('OPENAI_API_KEY')

CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

def run_query(query: str):
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except psycopg2.Error as e:
        return f"Error: {str(e)}"

def get_sql_query(question: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant proficient in PostgreSQL and TimescaleDB."},
            {
                "role": "user",
                "content": f"""Generate a PostgreSQL SELECT statement that answers the following question: '{question}'. Use TimescaleDB syntax where applicable. Only respond with PostgreSQL syntax. If there is an error, do not explain it.
                
                The tables in the database are as follows:
                
                CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                gender VARCHAR(10) CHECK(gender IN ('Male', 'Female')),
                age INT
                );

                CREATE TABLE IF NOT EXISTS MuscleGroup (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                selectedBias NUMERIC,
                region VARCHAR(20) CHECK(region IN ('Upper Body', 'Lower Body')),
                sizeConstant NUMERIC
                );

                CREATE TABLE IF NOT EXISTS Diet (
                id SERIAL PRIMARY KEY,
                type VARCHAR(20) CHECK(type IN ('Cutting', 'Maintenance', 'Bulking')),
                multiplierValue NUMERIC
                );

                CREATE TABLE IF NOT EXISTS Equipment (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                type VARCHAR(20) CHECK(type IN ('BodyWeight', 'Dumbbells', 'Machine', 'Barbell'))
                );

                CREATE TABLE IF NOT EXISTS Exercise (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                requiredEquipment INT REFERENCES Equipment(id),
                repConstant NUMERIC,
                weightConstant NUMERIC,
                video VARCHAR(100)
                );

                CREATE TABLE IF NOT EXISTS Workout (
                id SERIAL PRIMARY KEY,
                scheduledDate DATE,
                durationMinutes INT,
                exercise_ids INT[]
                );

                CREATE TABLE IF NOT EXISTS Schedule (
                id SERIAL PRIMARY KEY,
                workouts INT[]
                );

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
                
                The database also uses TimescaleDB extensions, so take advantage of Timescale-specific functionality when relevant, especially for time-based queries."""
            }
        ]
    )
    sql_query = completion.choices[0].message.content
    sql_query = sql_query.replace("```sql\n", "").replace("\n```", "").strip()
    print(sql_query)
    return sql_query



def generate_response(results):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Here are the database query results: {results}. Summarize this information in a friendly way."
        }
    ]
    )
    print(completion.choices[0].message)
    return completion.choices[0].message

def main():
    questions = input("Enter your questions, separated by commas: ").split(',')
    for question in questions:
        question = question.strip()
        sql_query = get_sql_query(question)
        results = run_query(sql_query)
        if "Error" in results:
            print(f"Failed to execute query for question '{question}': {results}")
        else:
            print(f"Results for question '{question}': {generate_response(results)}")

main()