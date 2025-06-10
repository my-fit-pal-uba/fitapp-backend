from abc import abstractmethod

class AbstractDietRepository:
    @abstractmethod
    def get_diets(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_diet_by_id(self, diet_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    @abstractmethod
    def post_diet(self, diet):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    @abstractmethod
    def remove_diet(self, diet_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    @abstractmethod
    def get_dishes_from_diet(self, diet_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")