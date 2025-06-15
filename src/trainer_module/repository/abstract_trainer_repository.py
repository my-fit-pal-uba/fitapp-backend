from abc import abstractmethod

class AbstractTrainerRepository:

    @abstractmethod
    def find_patient_by_full_identity(self, nombre: str, apellido: str, patient_id: int):
        """
        Busca un paciente por nombre, apellido e ID exactos.
        
        :return: El paciente si existe, None si no.
        """
        pass

    @abstractmethod
    def link_patient_to_trainer(self, patient_id: int, trainer_id: int) -> None:
        """
        Asocia el paciente con el entrenador en la base de datos.
        """
        pass
    

    @abstractmethod
    def get_clients_by_trainer(self, trainer_id: int) -> list[dict]:
        """
        Devuelve todos los clientes (ID, nombre, apellido) asociados a un entrenador.

        :param trainer_id: ID del entrenador
        :return: Lista de diccionarios con las claves: user_id, first_name, last_name
        """
        pass