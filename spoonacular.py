import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SPOONCULAR_API_KEY")


def detect_dishes(text):
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
        # dishes_info = []
        data = response.json()
        # print(data)
        # for annotation in data["annotations"]:
        #     if annotation["tag"] == "dish":
        #         dish_name = annotation["annotation"]
        #         # Проверьте наличие ключа "image" в элементе
        #         if "image" in annotation:
        #             dish_image_url = annotation["image"]
        #         else:
        #             # Если ключ "image" отсутствует, установите URL изображения по умолчанию или None
        #             dish_image_url = None
        #         dish_info = {
        #             "name": dish_name,
        #             "image_url": dish_image_url
        #         }
        #         dishes_info.append(dish_info)
        # print(dishes_info)

        dishes = [annotation["annotation"] for annotation in data["annotations"] if annotation["tag"] == "dish"]

        # # print(dishes)
        # dish_names = "\n ".join(dishes)
        return dishes

    except requests.exceptions.RequestException as e:
        print("Произошла ошибка при выполнении запроса:", e)
        return None


def get_dish(text):
    # url = "https://api.spoonacular.com/recipes/visualize"
    url = "https://api.spoonacular.com/food/menuItems/search"
    get_url = "https://api.spoonacular.com/food/menuItems/"
    params = {
        "apiKey": os.getenv("SPOONCULAR_API_KEY"),
        "query": text,
        'number': 1,
    }

    #
    # payload = {
    #
    # }
    dishes_info = []

    # response = requests.post(url, params=params, data=payload)
    # response = requests.post(url, params=params)
    response = requests.get(url, params=params)
    response.raise_for_status()

    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
        # get_params = {
        #     "apiKey": os.getenv("SPOONCULAR_API_KEY"),
        #     'id': data['id']
        # }
        # name = data['name']
        # calories = data['calories']
        # photo_url = data['image']
        # dish_info = {
        #     'name': name,
        #     'calories': calories,
        #     'photo_url': photo_url
        # }
        # dishes_info.append(dish_info)
    else:
        print(f'Ошибка при выполнении запроса для блюда')
        # print(dishes_info)
        return dishes_info


def get_single_item(menu_item):
    url = "https://api.spoonacular.com/recipes/complexSearch"

    params = {
        "apiKey": os.getenv("SPOONCULAR_API_KEY"),
        "query": menu_item,
        'number': 1,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    if response.status_code == 200:
        data = response.json()
        recipe_id = data['results'][0]['id']
        recipe_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=false"
        params = {
            "apiKey": os.getenv("SPOONCULAR_API_KEY"),
        }

        ans = requests.get(recipe_url, params=params)
        ans.raise_for_status()

        if ans.status_code == 200:
            data_ans = ans.json()
            ingredient_names = [ingredient["name"] for ingredient in data_ans["extendedIngredients"]]
            image_url = data_ans["image"]
            return ingredient_names, image_url

    else:
        print(f'Ошибка при выполнении запроса для блюда')
        return None


