from abc import abstractmethod


class AbstractTrainerRepository:

    @abstractmethod
    def find_patient_by_full_identity(
        self, nombre: str, apellido: str, patient_id: int
    ):
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

    @abstractmethod
    def exercise_exists(self, exercise_id: int) -> bool:
        """
        Verifica si un ejercicio existe por su ID.

        :param exercise_id: ID del ejercicio
        :return: True si existe, False si no.
        """
        pass

    @abstractmethod
    def client_exists(self, client_id: int) -> bool:
        """
        Verifica si un cliente existe por su ID.

        :param client_id: ID del cliente
        :return: True si existe, False si no.
        """
        pass

    @abstractmethod
    def share_exercise(self, exercise_id: int, client_id: int) -> None:
        """
        Comparte un ejercicio con un cliente.

        :param exercise_id: ID del ejercicio a compartir
        :param client_id: ID del cliente que recibe el ejercicio
        """
        pass

    @abstractmethod
    def dish_exists(self, dish_id: int) -> bool:
        """
        Verifica si un plato existe por su ID.

        :param dish_id: ID del plato
        :return: True si existe, False si no.
        """
        pass

    @abstractmethod
    def share_dish(self, dish_id: int, client_id: int) -> None:
        """
        Comparte un plato con un cliente.

        :param dish_id: ID del plato a compartir
        :param client_id: ID del cliente que recibe el plato
        """
        pass

    @abstractmethod
    def client_dishes(self, client_id: int) -> list[dict]:
        """
        Obtiene los platos compartidos con un cliente específico.

        :param client_id: ID del cliente
        :return: Lista de diccionarios con los platos compartidos
        """
        pass

    @abstractmethod
    def client_exercises(self, client_id: int) -> list[dict]:
        """
        Obtiene los ejercicios compartidos con un cliente específico.

        :param client_id: ID del cliente
        :return: Lista de diccionarios con los ejercicios compartidos
        """
        pass
