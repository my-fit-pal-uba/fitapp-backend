class DishEquivalences:
    """
    Class to handle dish equivalences.
    This class is used to manage the equivalence of dishes in the nutrition module.
    """

    def __init__(
        self, calories: float, protein: float, carbohydrates: float, fats: float
    ):
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fats = fats

    @classmethod
    def to_equivalences(cls, dish_consumption, dish):
        """
        Convert dish consumption and dish to equivalences.
        :param dish_consumption: DishConsumption object
        :param dish: Dish object
        :return: DishEquivalences object
        """
        calories_consumption = dish_consumption.quantity * dish.calories / dish.weight
        proteins_consumption = dish_consumption.quantity * dish.proteins / dish.weight
        carbs_consumption = dish_consumption.quantity * dish.carbs / dish.weight
        fats_consumption = dish_consumption.quantity * dish.fats / dish.weight

        return cls(
            calories=calories_consumption,
            protein=proteins_consumption,
            carbohydrates=carbs_consumption,
            fats=fats_consumption,
        )

    def to_dict(self):
        """
        Convert the DishEquivalences object to a dictionary.
        :return: Dictionary representation of the DishEquivalences object
        """
        return {
            "calories": self.calories,
            "protein": self.protein,
            "carbohydrates": self.carbohydrates,
            "fats": self.fats,
        }
