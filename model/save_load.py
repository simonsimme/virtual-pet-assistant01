import json

def save_game(pet, filename="savegame.json"):
    with open(filename, "w") as f:
        json.dump(pet.to_dict(), f)

def load_game(pet, item_lookup, filename="savegame.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            pet.from_dict(data, item_lookup)
            return True
    except FileNotFoundError:
        return False # File not found, return False
def save_exists(filename="savegame.json"):
    """Check if a save file exists."""
    try:
        with open(filename, "r") as f:
            return True
    except FileNotFoundError:
        return False