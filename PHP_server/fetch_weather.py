#!/usr/bin/env python3
"""
Hong Kong Observatory Data Fetcher
Fetches real-time regional temperature data from HKO Open Data API
and inserts it into the local MySQL/MariaDB database.
"""

import requests
import pymysql
import datetime
import sys

# Official HKO Open Data API for Regional Weather
API_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'pi_user',
    'password': 'pi_password',
    'database': 'temperature_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def fetch_and_store():
    print(f"[{datetime.datetime.now()}] Fetching temperature data from HKO...")
    try:
        # Use a timeout of 10s to prevent hanging requests
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        # Parse out the temperature array
        temperatures = data.get("temperature", {}).get("data", [])
        if not temperatures:
            print("Warning: No temperature data found in the API response.")
            return

        # Connect to MySQL/MariaDB database
        connection = pymysql.connect(**DB_CONFIG)

        with connection:
            with connection.cursor() as cursor:
                # Use parameterized queries to prevent SQL Injection
                sql = "INSERT INTO temperature_records (location, temperature) VALUES (%s, %s)"
                
                inserted_count = 0
                for temp_data in temperatures:
                    place = temp_data.get("place")
                    value = temp_data.get("value")
                    
                    if place and value is not None:
                        cursor.execute(sql, (place, value))
                        inserted_count += 1
                        
            # Commit the transaction
            connection.commit()
            
        print(f"[{datetime.datetime.now()}] Successfully updated database with {inserted_count} location records.")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}", file=sys.stderr)
    except pymysql.MySQLError as e:
        print(f"Database error occurred: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    fetch_and_store()