import psycopg2
import openai

openai.api_key = "your_openai_key"

# Use the connection string provided
CONNECTION_STRING = "postgres://tsdbadmin@qbam0sz08b.sxf6w90jzu.tsdb.cloud.timescale.com:36743/tsdb?sslmode=require"

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
    prompt = f"Generate a SQL query to answer the following question about a fitness database in PostgreSQL: '{question}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_response(results):
    prompt = f"Here are the database query results: {results}. Summarize this information in a friendly way."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def main(question):
    sql_query = get_sql_query(question)
    results = run_query(sql_query)
    if "Error" in results:
        return f"Failed to execute query: {results}"
    return generate_response(results)
