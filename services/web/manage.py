from flask.cli import FlaskGroup
from project import *

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
    db.session.commit()
    u = Usuario(nombre="Root", apellido="root", ci=1234, email="root@root.com", telefono='0991001188',activo=True, con="r00t", tipo=1)
    db.session.add(u)
    db.session.commit()
    u = Usuario(nombre="Cristhian", apellido="Duarte", ci=1234, email="cristhian@gmail.com", telefono='0991001188', activo=True, con="r00t", tipo=3)
    db.session.add(u)
    db.session.commit()
    db.session.add(Carrera(nombre_carrera="Plan Común"))
    db.session.add(Carrera(nombre_carrera="Contaduría Pública"))
    db.session.add(Carrera(nombre_carrera="Administración de Empresas"))
    db.session.add(Carrera(nombre_carrera="Economía"))
    db.session.add(Carrera(nombre_carrera="Tributación"))
    db.session.add(Carrera(nombre_carrera="Ingeniería Comercial"))
    db.session.commit()




if __name__ == "__main__":
    cli()
