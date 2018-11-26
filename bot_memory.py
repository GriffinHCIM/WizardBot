import os
from pathlib import Path
import json
import time


class bot_memory():
    def __init__(self, server):
        self.ready = False
        self.server = server
        if not os.path.exists(self.server):
            os.makedirs(self.server)

        self.reminders_file = self.server + "/reminders.json"
        if not os.path.exists(self.reminders_file):
            Path(self.reminders_file).touch()
        self.warnings_file = self.server + "/warnings.json"
        if not os.path.exists(self.warnings_file):
            Path(self.warnings_file).touch()
    def get_warnings(self):
        return_json = {}
        with open(self.warnings_file, 'r') as infile:
            return_json = json.load(infile)
        return return_json

    def set_warnings(self, JsonofWarnings):
        with open(self.reminders_file, 'w') as outfile:
            json.dump(JsonofWarnings, outfile)
        return JsonofWarnings

    def get_reminders(self):
        return_json = {}
        if (os.stat(self.reminders_file).st_size == 0):
            return return_json
        
        with open(self.reminders_file, 'r') as infile:
            return_json = json.load(infile)
        return return_json

    def set_reminders(self, JsonofReminders):
        with open(self.reminders_file, 'w') as outfile:
            json.dump(JsonofReminders, outfile)
        return JsonofReminders

    def update_reminders(self, JsonofReminders : list):
        previous_reminders = self.get_reminders()
        if "memory" not in previous_reminders:
            previous_reminders["memory"] = []
        
        previous_reminders["memory"] += JsonofReminders
        self.set_reminders(previous_reminders)


if __name__ == "__main__":
    memoryPath = "memory/" + "ironscape"
    memory = bot_memory("memory/ironscape")
    
    print(memory.get_reminders())
    memory.update_reminders([{"epoch":time.time(), "user":"LMAO", "message":"lol"}])
    
    print ("yup")

