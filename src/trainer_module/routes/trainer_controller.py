import re
from typing import Tuple
from typing import List
from trainer_module.services.abstract_trainer_service import AbstractTrainerService


class TrainerController:
    def __init__(self, trainer_service: AbstractTrainerService):
        self.trainer_service: AbstractTrainerService = trainer_service

    def register_client(
        self, patient_key: str, trainer_id: int
    ) -> Tuple[bool, str, int]:
        # Validación y parsing de clave
        if "#" not in patient_key:
            return False, "Formato de clave inválido. Debe ser 'NombreApellido#ID'", 400

        try:
            full_name, patient_id_str = patient_key.split("#")
            patient_id = int(patient_id_str)
        except ValueError:
            return False, "ID inválido en la clave", 400

        # Separar nombre y apellido (asumiendo PascalCase sin espacios)
        name_parts = re.findall("[A-Z][^A-Z]*", full_name)
        if len(name_parts) < 2:
            return False, "La clave debe contener al menos nombre y apellido", 400

        nombre = name_parts[0]
        apellido = " ".join(name_parts[1:])

        # Delegar en el service
        try:
            self.trainer_service.register_client(
                nombre, apellido, patient_id, trainer_id
            )
            return True, "Cliente vinculado exitosamente", 200
        except Exception as e:
            return False, f"Error al vincular cliente: {str(e)}", 500

    def get_clients_by_trainer(self, trainer_id: int):
        return self.trainer_service.get_clients_by_trainer(trainer_id)

    def share_exercise(self, client_id: int, exercise_id: int) -> Tuple[bool, str, int]:
        try:
            self.trainer_service.share_exercise(exercise_id, client_id)
            return True, "Ejercicio compartido exitosamente", 200
        except Exception as e:
            return False, f"Error al compartir ejercicio: {str(e)}", 500

    def share_dish(self, client_id: int, dish_id: int) -> Tuple[bool, str, int]:
        try:
            self.trainer_service.share_dish(dish_id, client_id)
            return True, "Plato compartido exitosamente", 200
        except Exception as e:
            return False, f"Error al compartir plato: {str(e)}", 500

    def client_dishes(self, client_id: int) -> List[dict]:
        """
        Obtiene los platos compartidos con un cliente específico.

        :param client_id: ID del cliente
        :return: Lista de diccionarios con los platos compartidos
        """
        return self.trainer_service.client_dishes(client_id)

    def client_exercises(self, client_id: int) -> List[dict]:
        """
        Obtiene los ejercicios compartidos con un cliente específico.

        :param client_id: ID del cliente
        :return: Lista de diccionarios con los ejercicios compartidos
        """
        return self.trainer_service.client_exercises(client_id)
