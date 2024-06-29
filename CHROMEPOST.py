import os
import sqlite3
import shutil
import time
import json
import datetime;from datetime import datetime,  timedelta
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

def checkinstall():
    
    chrome_profile_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default')
    edge_profile_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default')

    if os.path.exists(chrome_profile_path):
        print("Chrome is installed - using as default browser")    
    elif os.path.exists(edge_profile_path): 
        print("Chrome is installed, but does not seem to be running as defualt browser")
    else:
        print("Chrome does not seem to be installed")

def profilepic():
    
    possible_paths = [  
        os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\Google Profile Picture.png",
        os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\profile_picture.png",
        os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Profile 1\Google Profile Picture.png",
        os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Profile 1\profile_picture.png"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            current_dir = os.getcwd()
            copy_path = os.path.join(current_dir, os.path.basename(path))
            shutil.copy(path, copy_path)
            print(f"Profile picture copied to: {copy_path}")
            break
    else:
        print("Profile picture does not exist")



def extentions():

    extensions_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\Extensions"
    if not os.path.exists(extensions_path):
        print("Extensions directory does not exist.")
    else:
        extensions = []
        for extension_id in os.listdir(extensions_path):
            extension_dir = os.path.join(extensions_path, extension_id)
            if os.path.isdir(extension_dir):
                for version in os.listdir(extension_dir):
                    manifest_path = os.path.join(extension_dir, version, 'manifest.json')
                    if os.path.exists(manifest_path):
                        with open(manifest_path, 'r', encoding='utf-8') as file:
                            manifest = json.load(file)
                            extension_info = {
                                'name': manifest.get('name', 'Unknown'),
                                'version': manifest.get('version', 'Unknown'),
                                'description': manifest.get('description', 'No description')
                            }
                            extensions.append(extension_info)

        if extensions:
            for ext in extensions:
                print(f"Name: {ext['name']}, Version: {ext['version']}, Description: {ext['description']}")
        else:
            print("No extensions found")


def bookmarks():

    bookmarks_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\Bookmarks"
    if not os.path.exists(bookmarks_path):
        print("Bookmarks file does not exist.")
    else:
        try:
            with open(bookmarks_path, 'r', encoding='utf-8') as file:
                bookmarks_data = json.load(file)
                bookmarks = bookmarks_data['roots']['bookmark_bar']['children']
                
                for bookmark in bookmarks:
                    print(f"Name: {bookmark['name']}, URL: {bookmark['url']}")
        
        except Exception as e:
            print(f"An error occurred: {e}")




def downloadhistory():

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


def searchhistory():

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




def loginhistorysaves():

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


print("""
[1] Chrome Install State
[2] Profile Image
[3] Extentions
[4] Bookmarks
[5] Download History
[6] Search History
[7] Saved Passwords/Login History
""")

while True:

    chs = input("> ")

    if chs =="1":
        checkinstall()
        
    if chs =="2":
        profilepic()

    if chs =="3":
        extentions()

    if chs =="4":
        bookmarks()

    if chs =="5":
        downloadhistory()

    if chs =="6":
        searchhistory()

    if chs =="7":
        loginhistorysaves()
        













            

 
        

        
