import json
import os

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
