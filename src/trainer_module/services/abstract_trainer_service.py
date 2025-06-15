from abc import abstractmethod
from typing import List


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