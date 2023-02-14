import json
import os.path as path

import jsonpath_rw_ext as jsonpath

import cfg.configuration_loader as cl


class StatsExtractor:

    def __init__(self):
        config_loader = cl.ConfigurationLoader()
        self.input_file = config_loader.get_toml_config().get("json_report").get("input_file_path")
        self.write_stats_file = config_loader.get_toml_config().get("json_report").get("write_stats_file")
        self.output_file = config_loader.get_toml_config().get("json_report").get("output_file_path")

    def extract_stats_from_results(self) -> dict:
        """
        Extracts the node "stats" from the results file and returns it
        :return: stats as dict
        """

        if path.isfile(self.input_file):
            with open(self.input_file, "r") as f:
                return jsonpath.match('$.stats', json.load(f))[0]
        else:
            raise FileNotFoundError("Input file doesn't exist")

    def extract_stats_from_results_to_file(self) -> None:
        """
        Writes the "stats" dict as a json in a new file
        """

        if self.write_stats_file:
            if path.isdir(path.dirname(self.output_file)):

                stat = self.extract_stats_from_results()
                with open(self.output_file, "w") as f:
                    f.write(json.dumps(stat, indent=4))
            else:
                raise RuntimeError("Stated output path doesn't exists")
