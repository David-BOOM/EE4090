import MySQLdb
from sense_hat import SenseHat

def log_temperature():
    """
    Reads the temperature from the Raspberry Pi Sense HAT 
    and inserts it into a local MySQL database.
    """
    try:
        # 1. Initialize Sense HAT and read the current temperature
        sense = SenseHat()
        temp_celsius = sense.get_temperature()
        
        # Optional: calibrate or format the temperature
        # The SenseHat temperature reads a bit high due to CPU proximity,
        # but we'll log the raw rounded value.
        temp_celsius = round(temp_celsius, 2)
        
        # 2. Configure MySQL Database connection
        # IMPORTANT: Replace these with your actual local MySQL credentials
        db_config = {
            "host": "localhost",
            "user": "iot_user",
            "passwd": "",
            "db": "iot_database"
        }
        
        # Connect to the local MySQL database
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()
        
        # 3. Prepare and execute the SQL INSERT query
        # - `sr_no` is AUTO_INCREMENT, so we don't insert it manually.
        # - `rec_time` is configured to use DEFAULT CURRENT_TIMESTAMP, so the database captures the exact insertion time.
        # - `rec_temp` is explicitly passed the read temperature.
        sql = "INSERT INTO temperature_log (rec_temp) VALUES (%s)"
        
        cursor.execute(sql, (temp_celsius,))
        
        # Commit the transaction to save the changes
        conn.commit()
        print(f"Successfully recorded temperature: {temp_celsius} °C")
        
    except MySQLdb.Error as db_err:
        # Handle database-specific errors
        print(f"Database error occurred: {db_err}")
    except Exception as e:
        # Handle exceptions like SenseHat not being available
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure database resources are cleanly released
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    log_temperature()
