from faker import Faker

__fake = Faker(["en_US", "es_CO"])

# Instancia de Faker para generar datos ficticios basados en USA con fines generales.
fakeUS = __fake["en_US"]

# Instancia de Faker para generar datos ficticios basados en Colombia
fakeCO = __fake["es_CO"]
