from abc import abstractmethod


class AbstractRoutineService:
    """An abstract base class that defines the interface for routine services.
    Subclasses should implement the methods to provide concrete routine management logic.

    Methods
    -------
    create_routine(self, data: dict) -> dict:
        Abstract method to create routines.
        Should return a dictionary representing the created routine.

    search_routines(self, name: str) -> list:
        Abstract method to search routines by name.
        Should return a list of routines matching the name.

    filter_by_series(self, series: int) -> list:
        Abstract method to filter routines by series.
        Should return a list of routines that match the specified series.

    get_all_routines(self, name: str) -> list:
        Abstract method to get all routines
        Should return a list of all routines.
    """

    @abstractmethod
    def create_routine(self, data: dict) -> dict:
        """Abstract method to create routines."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def search_routines(self, name: str) -> list:
        """Abstract method to search routines by name."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def filter_by_series(self, series: int) -> list:
        """Abstract method to filter routines by series."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def get_all_routines(self, name: str) -> list:
        """Abstract method to get all routines."""
        raise NotImplementedError("Subclasses should implement this method.")
