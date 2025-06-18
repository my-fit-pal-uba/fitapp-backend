from trainer_module.services.abstract_trainer_service import AbstractTrainerService
from trainer_module.repository.abstract_trainer_repository import (
    AbstractTrainerRepository,
)

from typing import List, Dict


class TrainerService(AbstractTrainerService):
    def __init__(self, abstract_trainer_service: AbstractTrainerRepository):
        self.repository: AbstractTrainerRepository = abstract_trainer_service

    def register_client(
        self, nombre: str, apellido: str, patient_id: int, trainer_id: int
    ) -> None:
        paciente = self.repository.find_patient_by_full_identity(
            nombre, apellido, patient_id
        )
        if not paciente:
            raise ValueError(
                "Paciente no encontrado con nombre, apellido e ID provistos."
            )

        self.repository.link_patient_to_trainer(patient_id, trainer_id)

    def get_clients_by_trainer(self, trainer_id: int) -> List[dict]:
        return self.repository.get_clients_by_trainer(trainer_id)

    def share_exercise(self, exercise_id: int, client_id: int) -> None:
        if not self.repository.exercise_exists(exercise_id):
            raise ValueError("Ejercicio no encontrado con el ID proporcionado.")

        if not self.repository.client_exists(client_id):
            raise ValueError("Cliente no encontrado con el ID proporcionado.")

        self.repository.share_exercise(exercise_id, client_id)

    def share_dish(self, dish_id: int, client_id: int) -> None:
        if not self.repository.dish_exists(dish_id):
            raise ValueError("Plato no encontrado con el ID proporcionado.")

        if not self.repository.client_exists(client_id):
            raise ValueError("Cliente no encontrado con el ID proporcionado.")

        self.repository.share_dish(dish_id, client_id)

    def client_dishes(self, client_id: int) -> List[dict]:
        if not self.repository.client_exists(client_id):
            raise ValueError("Cliente no encontrado con el ID proporcionado.")

        return self.repository.client_dishes(client_id)

    def client_exercises(self, client_id: int) -> List[dict]:
        if not self.repository.client_exists(client_id):
            raise ValueError("Cliente no encontrado con el ID proporcionado.")

        return self.repository.client_exercises(client_id)