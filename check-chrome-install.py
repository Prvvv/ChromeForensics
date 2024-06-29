import os

chrome_profile_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default')
edge_profile_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default')

if os.path.exists(chrome_profile_path):
    print("Chrome is installed - using as default browser")
    
elif os.path.exists(edge_profile_path):
    
    print("Chrome is installed, but does not seem to be running as defualt browser")
else:
    print("Chrome does not seem to be installed")
