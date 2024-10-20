# A file just to load the list of characters

def load_characters_from_file(file_path):
    with open(file_path, 'r') as file:
        characters = [line.strip() for line in file.readlines()]
    return characters

