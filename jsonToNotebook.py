import json
import os

# Paste your JSON text here
notebook_json = """"""

# Convert string to JSON object
path = os.path.join(os.path.dirname(__file__), "notebook.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Save as .ipynb file
with open("deepfake_detection.ipynb", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Notebook saved as deepfake_detection.ipynb")
// filepath: c:\Users\avina\Desktop\Main\cOOntent\My project\DeepFake\deepfake_detection_complete.ipynb