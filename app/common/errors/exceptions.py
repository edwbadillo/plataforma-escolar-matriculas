class ExistsValueError(ValueError):
    """Representa un error para duplicados, errores de unicidad y otros similares."""

    field: str
    message: str

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message


class ResourceNotFound(Exception):
    """
    Representa un tipo de error cuando no existe algún recurso de la aplicación como
    puede ser un registro de la base de datos.
    """
