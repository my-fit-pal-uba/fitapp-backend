from abc import abstractmethod
from typing import List, Dict


class AbstractTrainerService:
    """An abstract base class that defines the interface for trainer services.
    Subclasses should implement the methods to provide concrete trainer management logic."""

    @abstractmethod
    def register_client(self, nombre: str, apellido: str, patient_id: int, trainer_id: int) -> None:
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