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
    url = "https://api.spoonacular.com/food/menuItems/search"

    params = {
        "apiKey": os.getenv("SPOONCULAR_API_KEY"),
        "query": menu_item,
        'number': 1,
        'addMenuItemInformation': True,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    res = {}

    if response.status_code == 200:
        data = response.json()
        menu_items = data.get("menuItems", [])

        if "menuItems" in data and data["menuItems"]:
            first_menu_item = data["menuItems"][0]
            if "images" in first_menu_item and first_menu_item["images"]:
                image_url = first_menu_item["images"][0]
            else:
                image_url = None
        else:
            image_url = None

        for menu_item in menu_items:
            caloric_breakdown = menu_item.get("nutrition", {}).get("caloricBreakdown", None)

            if caloric_breakdown is not None:
                percent_protein = caloric_breakdown.get("percentProtein", None)
                percent_fat = caloric_breakdown.get("percentFat", None)
                percent_carbs = caloric_breakdown.get("percentCarbs", None)

            nutrition = menu_item.get("nutrition", {})

            calories = nutrition.get("calories", None)
            fat = nutrition.get("fat", None)
            protein = nutrition.get("protein", None)
            carbs = nutrition.get("carbs", None)

            # if calories is not None:
            #     print("Calories:", calories)
            # if fat is not None:
            #     print("Fat:", fat)
            # if protein is not None:
            #     print("Protein:", protein)
            # if carbs is not None:
            #     print("Carbs:", carbs)
        # calories = data["menuItems"][0]["calories"]
        # fat = data["menuItems"][0]["fat"]
        # protein = data["menuItems"][0]["protein"]
        # carbs = data["menuItems"][0]["carbs"]
        # nutrients = data["menuItems"][0]["nutrition"]["nutrients"]
        # nutrient_info = []
        #
        # for i in range(0, len(nutrients)):
        #     nutrient_info.append(nutrients[i])
        res = {'image_url': image_url, 'percent_protein': percent_protein, 'percent_fat': percent_fat,
               'percent_carbs': percent_carbs, 'fat': fat, 'protein': protein, 'carbs': carbs}

        # Выведем результат
        # print("Ссылка на изображение:", image_url)
        # print("calories_percent", percent_protein, percent_fat, percent_carbs)
        # print("calories", calories)
        # print("fat", fat)
        # print("protein", protein)
        # print("carbs", carbs)
        # print("Информация о питательных веществах:",  nutrient_info)

        return res


    else:
        print(f'Ошибка при выполнении запроса для блюда')
        return None
