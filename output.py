# Output File for taking json data, and storing it in the folder /personas
import json
import random
import string
import os
from constants import OUTPUT_DIRECTORY, INDENT_SIZE
class Output:
    def __init__(self, output):
        self.output = output

    def writeFile(self, filename = ""):
        filename.strip(".json")
        if not filename:
            filename = "".join(str(self.output["name"]).split())  + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        # path = f"{filename}.json"
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)
        path = os.path.join(OUTPUT_DIRECTORY, f"{filename}.json")
        with open(path, "w") as f:
            json.dump(self.output, f, indent=INDENT_SIZE)
        print(f"Persona saved successfully at {path}")
        with open(path, "w") as f:
            json.dump(self.output, f, indent = INDENT_SIZE)
        print(f"Persona saved successfully at {path}")

    def logFile(self):
        print(json.dumps(self.output, indent=INDENT_SIZE))