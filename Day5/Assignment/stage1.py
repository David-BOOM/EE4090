import MySQLdb
from sense_hat import SenseHat

# ----------------- Configuration -----------------
DB_HOST = "localhost"
DB_USER = "root"      # Or use 'iot_user' if avoiding sudo constraints
DB_PASS = ""          # Empty password per previous configurations
DB_NAME = "mydb"
PI_ID = 1             # Hardcoded Raspberry Pi ID

def log_environment():
    """
    Reads hardware environment sensors from SenseHAT and pushes
    the data to the local_env_records table using a parameterized SQL query.
    """
    try:
        # 1. Initialize Sense HAT
        sense = SenseHat()
        
        # 2. Read Sensors + basic validation rounding
        temp = round(sense.get_temperature(), 2)
        humi = round(sense.get_humidity(), 2)
        press = round(sense.get_pressure(), 2)
        
    except Exception as e:
        print(f"Hardware Error: Could not read from Sense HAT. {e}")
        return

    try:
        # 3. Database Connection
        conn = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            db=DB_NAME
        )
        cursor = conn.cursor()
        
        # 4. Execute Parameterized Query
        # Note: We omit rec_time as it defaults to CURRENT_TIMESTAMP in the schema
        sql = """
            INSERT INTO local_env_records 
            (ID, rec_temp, rec_humi, rec_press) 
            VALUES (%s, %s, %s, %s)
        """
        
        # Execute query safely preventing SQL Injection
        cursor.execute(sql, (PI_ID, temp, humi, press))
        
        # Commit the transaction
        conn.commit()
        print(f"Logged -> ID: {PI_ID} | Temp: {temp}C | Humi: {humi}% | Press: {press}hPa")

    except MySQLdb.Error as db_err:
        print(f"Database Error: {db_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure database resources are cleanly released
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()
            print("Database connection successfully closed.")

if __name__ == "__main__":
    log_environment()
