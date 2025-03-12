class PropertyManager:
    data = {}

    @staticmethod
    def set_property(key: str, value: str):
        PropertyManager.data[key] = value

    @staticmethod
    def get_property(key: str) -> str:
        return PropertyManager.data.get(key)
