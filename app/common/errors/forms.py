from dataclasses import dataclass

from pydantic import ValidationError


@dataclass
class FormErrorDetail:
    """Define los atributos de un error de formulario que se mostrará en la respuesta
    JSON."""

    field: str
    message: str


class FormErrors:
    """Contiene los datos de error de un formulario generados por
    pydantic.ValidationError"""

    def __init__(self, validation_error: ValidationError) -> None:
        self._errors = validation_error.errors()
        self._total_errors = len(self._errors)

    @property
    def total_errors(self) -> int:
        """Cantidad total de errores encontrados."""
        return self._total_errors

    def check(
        self,
        field_loc: str | tuple[int | str, ...],
        *,
        message: str = None,
        type_error: str = None,
    ):
        """
        Verifica si existe un error en el formulario por el campo especificado
        Adicionalmente se puede especificar el tipo de error y/o el mensaje asociado.

        Este método es utilizado principalmente para testing.

        Args:
            field_loc (str | tuple[int | str, ...]): Nombre del campo o ubicación donde
            ocurre el error, se puede especificar un string directamente o una tupla de
            str e int con la ubicación completa del campo, ejemplos:
                - "username" es equivalente a ("username",)
                - ("username",)
                - ("addresses", 0)
                - ("user", "username")

            message (str, opcional): Mensaje asociado al error
            type_error (str, opcional): Tipo de error a verificar

        """
        if isinstance(field_loc, str):
            field_loc = (field_loc,)

        error = next(filter(lambda e: e["loc"] == field_loc, self._errors), None)
        assert error is not None, f"Error {field_loc} not found"

        if message:
            assert message in error["msg"]

        if type_error:
            assert type_error == error["type"]
