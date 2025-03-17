import json

class TestDataManager:
    @staticmethod
    def get_test_data(file_path="TestData/test_data.json"):
        with open(file_path, "r") as file:
            return json.load(file)


