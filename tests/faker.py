from typing import Callable, TypeVar

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database.models import Base

__fake = Faker(["en_US", "es_CO"])

# Instancia de Faker para generar datos ficticios basados en USA con fines generales.
fakeUS = __fake["en_US"]

# Instancia de Faker para generar datos ficticios basados en Colombia
fakeCO = __fake["es_CO"]

Model = TypeVar("Model", bound=Base)


async def faker_db_func(
    db: AsyncSession,
    fake_obj_func: Callable[[AsyncSession], Model | list[Model]],
    *,
    num_rows: int = 1,
    **kwargs
) -> Model | list[Model]:
    """
    Crea registros ficticios en la base de datos en conjunto con una función que genere
    los registros.

    Args:
        db (AsyncSession): Conexión con la base de datos.
        fake_obj_func (Callable[[AsyncSession], Model | list[Model]]): Función que
        genera los datos de un modelo, debe recibir por argumento la sesión de la base
        de datos y debe devolver el modelo generado.
        num_rows (int, opcional): Cantidad de registros a generar, por defecto 1.
        **kwargs (dict, opcional): Campos manualmente especificados para el modelo.

    Returns:
        Devuelve los registros generados o un solo registro si num_rows=1
    """
    objs_generated = []
    for _ in range(num_rows):
        objs_generated.append(await fake_obj_func(db, **kwargs))

    db.add_all(objs_generated)
    await db.commit()

    if num_rows == 1:
        return objs_generated[0]
    return objs_generated
