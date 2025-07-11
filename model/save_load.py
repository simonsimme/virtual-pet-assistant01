import json
import os

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
def delete_save(filename="savegame.json"):
    """Delete the save file if it exists."""
    try:
        os.remove(filename)
        return True
    except FileNotFoundError:
        return False  # File not found, nothing to delete
    except Exception as e:
        print(f"Error deleting save file: {e}")
        return False  # Other errors, return False
def save_age_highscore(pet, filename="age_highscore.txt"):
    """Save the pet's age as a high score."""
    try:
        with open(filename, "w") as f:
            prev = load_age_highscore(filename)
            if prev is not None and pet.age < prev:
                #f.write(str(pet.age))
                print("Not saving.")
            elif prev is None or pet.age > prev:
                f.write(str(pet.age))
    except Exception as e:
        print(f"Error saving age high score: {e}")
        return False
    return True
def load_age_highscore(filename="age_highscore.txt"):
    """Load the pet's age high score."""
    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                return None
            age = int(content)
            return age
    except Exception as e:
        print(f"Error loading age high score: {e}")
        return None