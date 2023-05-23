import os
import yaml
from Scripts.Helpers.logger import Logger

class Config():
    """
        Config base class, to be inherited by others
    """

    def __init__(self, path: str) -> None:
        """Load config file

        Args:
            path (str): Relative path to the config file; e.g. Common/tiles.yaml

        Raises:
            exc: Exception
        """

        self._logger = Logger().get()

        self._base_dir = os.path.abspath(
            os.path.join(__file__, "../"))

        self._config_file_path = os.path.abspath(
            os.path.join(self._base_dir, path))

        self._logger.debug(f"Loading config file {self._config_file_path}")

        try:
            with open(self._config_file_path, encoding="UTF-8") as file:
                self._raw_data = file.read()
                self._data = yaml.load(self._raw_data, Loader=yaml.FullLoader)
        except (FileNotFoundError, yaml.YAMLError) as exc:
            print(f"Failed to load {self._config_file_path}: {exc}")
            raise exc

    def get(self) -> any:
        """Get config data

        Returns:
            any: Config data
        """
        return self._data

    def get_by_key(self, key: str) -> any:
        """Get config data by key

        Args:
            key (str): Key

        Raises:
            KeyError: Key not found

        Returns:
            any: Config data
        """
        if not key in self._data:
            print("Key not found")
            raise KeyError(f"Key {key} is not found in the {self._config_file_path}")

        return self._data.get(key)
