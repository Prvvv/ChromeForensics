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
    cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC")

    rows = cursor.fetchall()

    for row in rows:
        print(f"URL: {row[0]} | Title: {row[1]} | Visit Count: {row[2]} | Last Visit Time: {row[3]}")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

finally:
    if connection:
        connection.close()
    if os.path.exists(temp_history_path):
        os.remove(temp_history_path)
