from abc import abstractmethod
from typing import List, Dict


class AbstractTrainerService:
    """An abstract base class that defines the interface for trainer services.
    Subclasses should implement the methods to provide concrete trainer management logic.
    """

    @abstractmethod
    def register_client(
        self, nombre: str, apellido: str, patient_id: int, trainer_id: int
    ) -> None:
        """
        Registra (vincula) un paciente a un entrenador.

        Parámetros:
        - nombre: str - nombre del paciente
        - apellido: str - apellido del paciente
        - patient_id: int - ID del paciente
        - trainer_id: int - ID del entrenador
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def get_clients_by_trainer(self, trainer_id: int) -> List[Dict[str, any]]:
        """
        Devuelve la lista de clientes vinculados a un entrenador.

        Parámetros:
        - trainer_id: int - ID del entrenador

        Retorna:
        - List[Dict]: Lista de diccionarios con keys 'user_id', 'first_name', 'last_name'
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def share_exercise(self, exercise_id: int, client_id: int) -> None:
        """
        Comparte un ejercicio con un cliente.

        Parámetros:
        - exercise_id: int - ID del ejercicio a compartir
        - client_id: int - ID del entrenador que comparte el ejercicio
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    @abstractmethod
    def share_dish(self, dish_id: int, client_id: int) -> None:
        """
        Comparte un plato con un cliente.

        Parámetros:
        - dish_id: int - ID del plato a compartir
        - client_id: int - ID del entrenador que comparte el plato
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    @abstractmethod
    def client_dishes(self, client_id: int) -> List[Dict[str, any]]:
        """
        Obtiene los platos compartidos con un cliente específico.

        Parámetros:
        - client_id: int - ID del cliente

        Retorna:
        - List[Dict]: Lista de diccionarios con los platos compartidos
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    @abstractmethod
    def client_exercises(self, client_id: int) -> List[Dict[str, any]]:
        """
        Obtiene los ejercicios compartidos con un cliente específico.

        Parámetros:
        - client_id: int - ID del cliente

        Retorna:
        - List[Dict]: Lista de diccionarios con los ejercicios compartidos
        """
        raise NotImplementedError("Subclasses should implement this method.")
    