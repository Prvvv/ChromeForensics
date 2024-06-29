import os
import sqlite3
import shutil

chrome_profile_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default')

if not os.path.exists(chrome_profile_path):
    print("Chrome profile folder not found.")
    exit()

temp_history_path = os.path.join(os.environ['TEMP'], 'History')
shutil.copy2(os.path.join(chrome_profile_path, 'History'), temp_history_path)

try:
    connection = sqlite3.connect(temp_history_path)
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(downloads)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    if 'tab_url' in column_names:
        cursor.execute("SELECT tab_url FROM downloads ORDER BY end_time DESC")

        rows = cursor.fetchall()

        for row in rows:
            print(f"URL: {row[0]}")
    else:
        print("Column 'tab_url' not found in the 'downloads' table.")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    
    if connection:
        connection.close()

    os.remove(temp_history_path)
