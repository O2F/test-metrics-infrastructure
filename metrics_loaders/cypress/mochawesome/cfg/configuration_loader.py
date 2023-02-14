"""Load cfg from .toml file."""
import toml
import json


# Read local `cfg.toml` file.
#cfg = toml.load('cfg.toml')
class ConfigurationLoader:

    def get_toml_config(self):
        return toml.load('config.toml')


    def console_prettify(self):
        print(json.dumps(self.get_toml_config(),
                         sort_keys=True,
                         indent=4,
                         separators=(',', ': '))
              )
#c = ConfigurationLoader()
#c.console_prettify()