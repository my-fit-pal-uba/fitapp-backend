from nutrition_module.service.abstract_nutrition_service import AbstractNutritionService


class Nutrition(AbstractNutritionService):

    def __init__(self):
        pass

    def post_dish(self, dish):
        return ""

    def register_dish(self, dish):
        return ""

    def get_dishes(self):
        return []

    def post_dish_history(self, dish):
        pass

    def register_calories_history(self, calories):
        return ""
