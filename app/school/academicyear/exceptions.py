from app.common.errors.exceptions import ResourceNotFound


class AcademicYearNotFound(ResourceNotFound):
    """
    Representa un tipo de error cuando no existe un registro de año escolar en la base
    de datos.
    """
