from nutrition_module.routes.nutrition_controller import NutritionController


class NutritionProxy:

    def __init__(self, nutrition_controller):
        self.nutrition_controller: NutritionController = nutrition_controller

    def get(self):
        pass
