import typer

app = typer.Typer()


@app.command()
def migrate():
    """
    Crea la estrutura de base de datos
    """
    from app.scripts.migrate import migrate

    migrate()


@app.command()
def init_db():
    """
    Crea los registros de la base de datos de las tablas principales
    """
    from app.scripts.initdb import init_db as create_rows

    create_rows()


if __name__ == "__main__":
    app()
