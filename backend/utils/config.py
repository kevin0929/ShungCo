import yaml


try:
    with open("config.yaml") as file:
        CONFIG = yaml.safe_load(file)
except FileNotFoundError:
    raise FileNotFoundError("Please provide a config yaml file.")
