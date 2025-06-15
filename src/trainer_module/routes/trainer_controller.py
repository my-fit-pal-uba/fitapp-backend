import re
from typing import Tuple
from typing import List
from trainer_module.services.abstract_trainer_service import AbstractTrainerService


class TrainerController:
    def __init__(self, trainer_service: AbstractTrainerService):
        self.trainer_service: AbstractTrainerService = trainer_service

    def register_client(self, patient_key: str, trainer_id: int) -> Tuple[bool, str, int]:
        # Validación y parsing de clave
        if "#" not in patient_key:
            return False, "Formato de clave inválido. Debe ser 'NombreApellido#ID'", 400

        try:
            full_name, patient_id_str = patient_key.split("#")
            patient_id = int(patient_id_str)
        except ValueError:
            return False, "ID inválido en la clave", 400

        # Separar nombre y apellido (asumiendo PascalCase sin espacios)
        name_parts = re.findall('[A-Z][^A-Z]*', full_name)
        if len(name_parts) < 2:
            return False, "La clave debe contener al menos nombre y apellido", 400

        nombre = name_parts[0]
        apellido = " ".join(name_parts[1:])

        # Delegar en el service
        try:
            self.trainer_service.register_client(nombre, apellido, patient_id, trainer_id)
            return True, "Cliente vinculado exitosamente", 200
        except Exception as e:
            return False, f"Error al vincular cliente: {str(e)}", 500