import MySQLdb
from sense_hat import SenseHat
from time import sleep

# ----------------- Configuration -----------------
DB_HOST = "localhost"
DB_USER = "root"      # Or use 'iot_user'
DB_PASS = ""          
DB_NAME = "mydb"

# Parameterized table name so it can easily be swapped between 
# 'trainingdb1' and 'trainingdb2' or 'trainingdb3' etc.
TARGET_TABLE = "trainingdb1" 
PI_ID = 1

# Initialize the Sense HAT hardware globally
try:
    sense = SenseHat()
except Exception as e:
    print(f"Failed to initialize Sense HAT: {e}")
    exit(1)

def push_to_db(event):
    """
    Callback function that is triggered when the Sense HAT joystick moves.
    Ensures data is only pulled and pushed once the stick is 'pressed'.
    """
    # Only fire tracking logic if the hardware event detects a manual "press" 
    # This acts as our debounce/safety logic preventing loops of uploads.
    if event.action != 'pressed':
        return
        
    try:
        # Read environment sensors
        temp = round(sense.get_temperature(), 2)
        humi = round(sense.get_humidity(), 2)
        press = round(sense.get_pressure(), 2)
    except Exception as e:
        print(f"Could not read sensing data. {e}")
        return

    try:
        # Open connection
        conn = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            db=DB_NAME
        )
        cursor = conn.cursor()
        
        # Prepare parameterized SQL for the target joystick database
        # F-strings safely handle dynamic configuration naming for the physical Table,
        # whilst %s protects our data insertion layer from malicious injection.
        sql = f"""
            INSERT INTO {TARGET_TABLE} 
            (ID, rec_temp, rec_humi, rec_press) 
            VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(sql, (PI_ID, temp, humi, press))
        conn.commit()
        
        print(f"Event Success: Uploaded [Temp: {temp}C, Humi: {humi}%, Press: {press}hPa] to {TARGET_TABLE}")
        
    except MySQLdb.Error as db_err:
        print(f"Database Error: {db_err}")
    except Exception as e:
        print(f"Unexpected Error inside upload routine: {e}")
    finally:
        # Carefully close objects down individually preventing data leaks
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()

# ----------------- Main Event Loop -----------------
if __name__ == "__main__":
    print(f"Starting Stage 2 Script...")
    print(f"Listening for joystick presses to log data to table: '{TARGET_TABLE}'.")
    print(f"Press Ctrl+C to terminate.")
    
    # Register our push function against any joystick movement
    sense.stick.direction_any = push_to_db
    
    try:
        # Keep the program thread alive continuously to monitor the joystick
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        print("\nTermination signal received (Ctrl+C). Shutting down.")
