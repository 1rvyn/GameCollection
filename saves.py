import json


class Saves:
    def __init__(self, fp: str):
        self.fp = fp

    # Gets a value from a specified key within the saves.json
    def get(self, key):
        try:
            with open(self.fp, "r") as data:
                settings = json.load(data)
                if isinstance(key, list):
                    for k in key:
                        settings = settings.get(k)
                    return settings
                elif isinstance(key, str):
                    return settings.get(key)
        except:
            return None

    # Writes a value from a specified key within the saves.json
    def write(self, key, value):
        with open(self.fp, "r") as data:
            settings = json.load(data)
            settings[key] = value
            with open(self.fp, "w") as wdata:
                json.dump(settings, wdata, indent=4, sort_keys=True)

    # Saves specified scores for a specfied user
    def save_score(self, save_name, username, value):
        game_saves = self.get(save_name)
        if not game_saves:
            game_saves = dict()
        game_saves[username] = value
        self.write(save_name, game_saves)
