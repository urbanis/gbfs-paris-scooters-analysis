import psycopg2
import json
import os

def new_database_connection():
    # connect to the database
    return psycopg2.connect(
        database='', 
        user='', 
        password='', 
        host='', 
        port= ''
    )

# read JSON data from file

conn = new_database_connection()

dir_path = "./json_files/"
files = os.listdir(dir_path)

for file in files:
    file_dir = dir_path + file
    
    with open(file_dir) as f:
        data = json.load(f)
    
        with conn:
            cur = conn.cursor()

            file_name = file[:-5]
            file_date = file_name[10:]
            year = file_date[:4]
            month = file_date[4:6]
            day = file_date[6:8]

            hours = file_date[9:11]
            minutes = file_date[11:13]

            file_date_formatted = year + "-" + month + "-" + day + " " + hours + ":" + minutes+ ":" + "00"
            
            print(file_name)
            print(file_date_formatted)

            cur.execute("INSERT INTO gbfsreports(name, date) VALUES (%s, %s) RETURNING id;", (file_name, file_date_formatted))
            gbfsreports_id = cur.fetchone()[0]

            for item in data:
                bike_id = item["bike_id"]
                lat = item["lat"]
                lon = item["lon"]
                is_reserved = item["is_reserved"]
                is_disabled = item["is_disabled"]
                current_range_meters = item["current_range_meters"]
                vehicle_type_id = item["vehicle_type_id"]
                last_reported = item["last_reported"]
                vehicle_type = item["vehicle_type"]
                
                cur.execute("INSERT INTO gbfsparis(bike_id, lat, lon, is_reserved, is_disabled, current_range_meters, vehicle_type_id, last_reported, vehicle_type, gbfsreports_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (bike_id, lat, lon, is_reserved, is_disabled, current_range_meters, vehicle_type_id, last_reported, vehicle_type, gbfsreports_id))
            
            # commit the changes to the database
            conn.commit()

            # close the cursor and connection
            cur.close()
    
conn.close()