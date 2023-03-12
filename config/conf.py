import os
import yaml


class ConfigMng:

    def get_index_name(self):
        return self.config["index"]["name"]

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if os.environ.get("env") != "prod":
            with open(current_dir + '/config-dev.yaml', 'r', encoding='utf-8') as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        else:
            with open(current_dir + '/config-prod.yaml', 'r', encoding='utf-8') as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)


config_mng = ConfigMng()