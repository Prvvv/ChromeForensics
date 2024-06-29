import os
import shutil

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
    print("Profile picture does not exist.")
