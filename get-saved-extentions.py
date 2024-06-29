import json
import os

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
        print("No extensions found.")
