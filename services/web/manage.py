from flask.cli import FlaskGroup
from project import app, db, Usuario, TipoUsuario, Carrera, Materia

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(TipoUsuario(descripcion="Administrador"))
    db.session.add(TipoUsuario(descripcion="Coordinador"))
    db.session.add(TipoUsuario(descripcion="Profesor"))
    db.session.add(TipoUsuario(descripcion="Alumno"))
    db.session.commit()
    u = Usuario(nombre="Root", apellido="root", ci=1234, email="root@root.com", activo=True, con="r00t", tipo=1)
    db.session.add(u)
    db.session.commit()



if __name__ == "__main__":
    cli()
