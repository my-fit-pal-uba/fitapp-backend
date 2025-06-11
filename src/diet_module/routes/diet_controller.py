class DietController:
    def __init__(self):
        pass

    def get_diets(self, user_id):
        diets = [
            {
                "name": "Dieta Mediterránea",
                "description": "Enfocada en el consumo de frutas, verduras, granos enteros, pescado y aceite de oliva.",
                "calories": 2000,
            }
        ]
        return True, diets, 200
