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
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert SQL assistant proficient in writing accurate and optimized "
                    "PostgreSQL and TimescaleDB SQL queries. Your task is to generate correct SQL queries "
                    "based on the user's question, using the provided database schema. Ensure that the SQL "
                    "syntax is correct, and only output the SQL query without any additional text or explanations."
                )
            },
            {
                "role": "user",
                "content": f"""
Please generate a valid PostgreSQL SELECT statement that answers the following question: '{question}'. Use TimescaleDB syntax where applicable. Use only the tables and columns provided in the schema below. Do not assume any additional tables or columns. Only respond with the SQL query, and do not include any explanation or comments. If the question cannot be answered with the given schema, output an error message.

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

The database also uses TimescaleDB extensions, so take advantage of Timescale-specific functionality when relevant, especially for time-based queries.
"""
            }
        ]
    )
    sql_query = completion.choices[0].message.content.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    print(sql_query)
    return sql_query



def generate_response(results):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who can interpret and summarize database query results "
                    "in a clear and user-friendly manner."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Given the following database query results, please summarize the information in a clear "
                    f"and friendly way for the user. If appropriate, include key details or statistics, and "
                    f"present the information in an easily understandable format. Here are the results: {results}"
                )
            }
        ]
    )
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
            response = generate_response(results)
            print(f"Results for question '{question}': {response.content}")


main()