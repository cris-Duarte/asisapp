from flask.cli import FlaskGroup
import csv
from project import *

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    seed_db()
    desdearchivo()


def seed_db():
    db.session.add(TipoUsuario(descripcion="Administrador"))
    db.session.add(TipoUsuario(descripcion="Coordinador"))
    db.session.add(TipoUsuario(descripcion="Profesor"))
    db.session.add(Curso(descripcion="Primero"))
    db.session.add(Curso(descripcion="Segundo"))
    db.session.add(Curso(descripcion="Tercero"))
    db.session.add(Curso(descripcion="Cuarto"))
    db.session.add(Curso(descripcion="Quinto"))
    db.session.commit()
    u = Usuario(nombre="Root", apellido="root", ci=1234, email="root@root.com", telefono='0991001188',activo=True, con="r00t", tipo=1)
    db.session.add(u)
    db.session.commit()
    u = Usuario(nombre="Cristhian", apellido="Duarte", ci=1234, email="cristhian@gmail.com", telefono='0991001188', activo=True, con="r00t", tipo=3)
    db.session.add(u)
    db.session.commit()
    db.session.add(Carrera(nombre_carrera="Plan Común",responsable=2))
    db.session.add(Carrera(nombre_carrera="Contaduría Pública",responsable=2))
    db.session.add(Carrera(nombre_carrera="Administración de Empresas",responsable=2))
    db.session.add(Carrera(nombre_carrera="Economía",responsable=2))
    db.session.add(Carrera(nombre_carrera="Tributación",responsable=2))
    db.session.add(Carrera(nombre_carrera="Ingeniería Comercial",responsable=2))
    db.session.commit()


def desdearchivo():
    f = open("usuarios.csv")
    reader = csv.reader(f)
    for n, a, e, t in reader:
        u = Usuario(\
        nombre=n,\
        apellido=a,\
        email=e,\
        activo=True,\
        tipo=t)
        db.session.add(u)

    db.session.commit()


if __name__ == "__main__":
    cli()
