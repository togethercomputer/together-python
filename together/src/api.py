import requests


class API:
    def get_supply(self):
        model_list_endpoint = "https://computer.together.xyz"
        res = requests.get(
            model_list_endpoint,
            json={
                "method": "together_getDepth",
                "id": 1,
            },
        )
        return res.json()

    def print_all_models(self):
        model_names = self.get_supply()["result"].keys()

        model_names = [
            sub[:-1] for sub in model_names
        ]  # remove the ? after the model names
        for name in model_names:
            print(name)

    def print_available_models(self):
        res = self.get_supply()
        names = res["result"].keys()
        available_models = [
            name[:-1] for name in names if res["result"][name]["num_asks"] > 0
        ]

        for model_name in available_models:
            print(model_name)
