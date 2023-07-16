import requests
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("SPOONCULAR_API_KEY")


def detect_food(text):
    url = "https://api.spoonacular.com/food/detect"

    params = {
        "apiKey": os.getenv("SPOONCULAR_API_KEY")
    }

    payload = {
        "text": text
    }

    try:
        response = requests.post(url, params=params, data=payload)
        response.raise_for_status()

        data = response.json()
        dishes = [annotation["annotation"] for annotation in data["annotations"] if annotation["tag"] == "dish"]
        dish_names = "\n ".join(dishes)
        return dish_names

    except requests.exceptions.RequestException as e:
        print("Произошла ошибка при выполнении запроса:", e)
        return None
