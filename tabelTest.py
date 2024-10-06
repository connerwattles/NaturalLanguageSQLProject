import psycopg2

CONNECTION_STRING = "postgres://tsdbadmin:byuPassword123@qbam0sz08b.sxf6w90jzu.tsdb.cloud.timescale.com:36743/tsdb?sslmode=require"

def test_data():
    with psycopg2.connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM User")
            print("User:", cursor.fetchall())
            
            cursor.execute("SELECT * FROM MuscleGroup")
            print("MuscleGroup:", cursor.fetchall())
            
            cursor.execute("SELECT * FROM Diet")
            print("Diet:", cursor.fetchall())
            
            cursor.execute("SELECT * FROM Equipment")
            print("Equipment:", cursor.fetchall())
            
            cursor.execute("SELECT * FROM Exercise")
            print("Exercise:", cursor.fetchall())
            
            cursor.execute("SELECT * FROM Workout")
            print("Workout:", cursor.fetchall())
            
            cursor.execute("SELECT * FROM Schedule")
            print("Schedule:", cursor.fetchall())
            
            cursor.execute("SELECT * FROM Program")
            print("Program:", cursor.fetchall())

test_data()
