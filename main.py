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
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant proficient in PostgreSQL and TimescaleDB."},
            {
                "role": "user",
                "content": f"""Generate a PostgreSQL SELECT statement that answers the following question: '{question}'. Use TimescaleDB syntax where applicable. Only respond with PostgreSQL syntax. If there is an error, do not explain it.
                
                The tables in the database are as follows:
                
                1. **User**: Columns - `gender` (Enum: 'Male' or 'Female'), `age` (Number).
                2. **Program**: Columns - `selectedWorkoutDaysPerWeek` (Number), `experienceLevel` (Enum: 'Beginner', 'Intermediate', 'Advanced'), `selectedGoals` (Array of goal values as enum strings), `selectedWorkoutTypes` (Array of workout types as enum strings), `selectedWorkoutDuration` (Number), `selectedDiet` (FK to Diet table), `selectedWeightUnit` (Enum: 'Kgs' or 'Lbs'), `selectedGymBusiness`, `selectedMuscleGroups` (Array of FK to MuscleGroup), `subscriptionStatus` (Boolean), `selectedDaysUntilNextWorkout` (Number), `selectedSoreMuscleGroups` (Array of FK to MuscleGroup).
                3. **Schedule**: Columns - `workouts` (Array of FK to Workout).
                4. **Workout**: Columns - `scheduledDate` (Date), `durationMinutes` (Number), `exercise_ids` (Array of FK to Exercise), constraints of 5-8 muscle groups.
                5. **Exercise**: Columns - `name` (String), `requiredEquipment` (FK to Equipment.id, Integer), `repConstant` (Number), `weightConstant` (Number), `video` (String).
                6. **Equipment**: Columns - `id` (Primary Key, Integer), `name` (String), `type` (Enum: 'BodyWeight', 'Dumbbells', 'Machine', 'Barbell').
                7. **MuscleGroup**: Columns - `name` (String), `selectedBias` (Number), `region` (Enum: 'Upper Body', 'Lower Body'), `sizeConstant` (Number).
                8. **Diet**: Columns - `type` (Enum: 'Cutting', 'Maintenance', 'Bulking'), `multiplierValue` (Number).
                
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
    model="gpt-4o-mini",
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