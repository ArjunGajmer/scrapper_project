import json
import os
from typing import Dict, List


class FileStoreManager:
    def __init__(self, base_path: str, fetch_key: str):
        self.base_path = base_path
        self.fetch_key = fetch_key
        self.file_path = os.path.join(self.base_path, self.fetch_key, 'data.json')
        self.__setup()

    def read_data(self) -> List[Dict]:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return []

    def write_data(self, data: List[Dict]):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def update_and_append_data(self, new_data: List[Dict], search_key: str):
        existing_data = self.read_data()
        existing_data_map = {item[search_key]: item for item in existing_data}
        for item in new_data:
            key_value = item[search_key]
            if key_value in existing_data_map:
                existing_data_map[key_value].update(item)
            else:
                existing_data_map[key_value] = item
        self.write_data(list(existing_data_map.values()))

    def __setup(self):
        os.makedirs(os.path.join(self.base_path, self.fetch_key), exist_ok=True)


