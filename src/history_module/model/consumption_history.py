class consumption_history:
    def __init__(
        self,
        fecha_consumo=None,
        total_calorias=0.0,
        total_proteinas=0.0,
        total_carbohidratos=0.0,
        total_grasas=0.0,
    ):
        self.fecha_consumo = fecha_consumo
        self.total_calorias = total_calorias
        self.total_proteinas = total_proteinas
        self.total_carbohidratos = total_carbohidratos
        self.total_grasas = total_grasas

    def to_dict(self):
        return {
            "fecha_consumo": self.fecha_consumo,
            "total_calorias": self.total_calorias,
            "total_proteinas": self.total_proteinas,
            "total_carbohidratos": self.total_carbohidratos,
            "total_grasas": self.total_grasas,
        }
