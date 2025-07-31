import yaml

def load_yaml(filepath:str):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def map_ign_to_name(ign: str) -> str:
    ign_to_name_mapping = load_yaml("data/player_names.yaml")
    return ign_to_name_mapping.get(ign, ign)