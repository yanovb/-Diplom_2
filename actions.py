import random
import requests


class Actions:
    @staticmethod
    def make_user(route, user_data):
        return requests.post(route, user_data)

    @staticmethod
    def make_user_without_param(route, user_data, param):
        user_data_without_param = user_data
        user_data_without_param.pop(param)
        return requests.post(route, user_data_without_param)

    @staticmethod
    def make_auth(route, user_data):
        return requests.post(route, user_data)

    @staticmethod
    def change_user_data(route, new_user_data, token=None):
        return requests.patch(route, headers={'Authorization': token}, data=new_user_data)

    @staticmethod
    def get_random_ingredients(route):
        ingredients_list = requests.get(route).json()['data']
        ingredients_id_list = list(map(lambda ingredient: ingredient['_id'], ingredients_list))
        subset_size = random.randint(1, len(ingredients_id_list))
        result = random.sample(ingredients_id_list, subset_size)
        random.shuffle(result)
        return result

    @staticmethod
    def create_order(route, ingredients, token=None):
        body = {
            'ingredients': ingredients
        }
        return requests.post(route, headers={'Authorization': token}, data=body)

    @staticmethod
    def get_orders(route, token=None):
        return requests.get(route, headers={'Authorization': token})

    @staticmethod
    def delete_user(route, token):
        return requests.delete(route, headers={'Authorization': token})
