import yaml


def yaml_demo():
    data = {"project": "lab4", "libs": ["numpy", "pandas"], "version": 1}
    text = yaml.dump(data, allow_unicode=True)
    return yaml.safe_load(text)