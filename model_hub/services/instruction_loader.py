import json

_instructions_cache = None

def load_instructions(file_path="instructions.json"):
    global _instructions_cache
    if _instructions_cache is None:
        with open(file_path, "r") as f:
            _instructions_cache = json.load(f)
    return _instructions_cache

def get_instruction(name):
    instructions = load_instructions()
    return instructions.get(name)
