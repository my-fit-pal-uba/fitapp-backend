from abc import abstractmethod


class AbstractExerciseRepository:
    @abstractmethod
    def search_exercises(self, name: str) -> list:
        pass

    @abstractmethod
    def get_exercises(self) -> list:
        pass

    @abstractmethod
    def filter_by_muscular_group(self, muscular_group: str) -> list:
        pass

    @abstractmethod
    def filter_by_type(self, type: str) -> list:
        pass

    @abstractmethod
    def filter_by_place(self, place: str) -> list:
        pass
