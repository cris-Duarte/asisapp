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
    usuarios()
    cargaalumno()
    cargamateria()


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
    #### Usuarios Legacy
    #u = Usuario(nombre="Root", apellido="root", ci=1234, email="root@root.com", telefono='0991001188',activo=True, con="r00t", tipo=1)
    #db.session.add(u)
    #db.session.commit()
    #u = Usuario(nombre="Cristhian", apellido="Duarte", ci=1234, email="cristhian@gmail.com", telefono='0991001188', activo=True, con="r00t", tipo=3)
    #db.session.add(u)
    #db.session.commit()
    ##
    db.session.add(Carrera(nombre_carrera="Plan Común"))
    db.session.add(Carrera(nombre_carrera="Contaduría Pública"))
    db.session.add(Carrera(nombre_carrera="Administración de Empresas"))
    db.session.add(Carrera(nombre_carrera="Economía"))
    db.session.add(Carrera(nombre_carrera="Tributación"))
    db.session.add(Carrera(nombre_carrera="Ingeniería Comercial"))
    db.session.commit()

def usuarios():
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

def cargaalumno():
    f = open("alumnos.csv")
    reader = csv.reader(f)
    for ci, n, a in reader:
        a = Alumno(\
        nombre=n,\
        apellido=a,\
        ci=ci,\
        con=ci)
        db.session.add(a)

    db.session.commit()

def cargamateria():
    f = open("materias.csv")
    reader = csv.reader(f)
    for n, cu, s, ca in reader:
        m = Materia(\
        nombre=n,\
        codigo=codigo(),\
        curso=cu,\
        seccion=s,\
        carrera=ca)
        db.session.add(m)
        db.session.commit()


if __name__ == "__main__":
    cli()
