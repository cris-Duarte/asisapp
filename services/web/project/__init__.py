from flask import Flask, jsonify, render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_login import LoginManager,login_user,logout_user,login_required, current_user
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
app.secret_key = b'\x9f\xa5\xb3\xaa\xfa\x8f\xdc\xe4;\xdbf_\x9a\xd2\x1dP'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "ingresar"


@app.route("/")
def index():
    return "<h6>Hello wordl</h6>"

@app.route("/ingresar")
def ingresar():
    if current_user.is_active:
        return redirect(url_for('dashboard'))
    else:
        return render_template("ingresar.html")


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/login", methods=['POST'])
def login():
    email = request.form.get("correo")
    c = request.form.get('c')
    u = Usuario.query.filter(and_(Usuario.email == email, Usuario.con == c)).first()
    if not u or u is None:
        return render_template("dashboard.html",mensaje="Error de acceso: Correo Electrónico o Contraseña incorrectos")
    else:
        u = load_user(u.id)
        login_user(u,remember=True, duration=None, force=False, fresh=True)
        return redirect(url_for('dashboard'), code=303)

@app.route("/perfil", methods=['POST'])
@login_required
def perfil():
    return render_template("perfil.html")

@app.route("/materias", methods=['POST'])
@login_required
def materias():
    s_materias = False
    up = False
    if request.form.get('alta'):
        m = Materia(nombre=request.form.get('mnombre'), codigo=request.form.get('mcodigo'), curso=request.form.get('mcurso'), seccion=request.form.get('mseccion'), carrera=int(request.form.get('mcarrera')), docente=int(request.form.get('mdocente')), activo = True)
        db.session.add(m)
        db.session.commit()
        s_materias = True
    if request.form.get('mbaja'):
        m = Materia.query.get(int(request.form.get('mid')))
        m.activo = False
        db.session.commit()
        s_materias = True
    if request.form.get('a_modificar') != None:
        m = Materia.query.get(request.form.get('a_modificar'))
        m.nombre = request.form.get('mnombre')
        m.codigo = request.form.get('mcodigo')
        m.curso = request.form.get('mcurso')
        m.seccion = request.form.get('mseccion')
        m.carrera = int(request.form.get('mcarrera'))
        m.docente = int(request.form.get('mdocente'))
        db.session.commit()
        s_materias = True

    if request.form.get('modificacion'):
        m = Materia.query.get(int(request.form.get('mid')))
        carreras = Carrera.query.all()
        usuarios = Usuario.query.filter_by(activo=True).all()
        return render_template("materias.html", carreras=carreras, usuarios=usuarios,m=m,modMateria=True,s_materias=False)
    else:
        carreras = Carrera.query.all()
        materias = Materia.query.filter_by(activo=True).all()
        usuarios = Usuario.query.filter_by(activo=True).all()
        return render_template("materias.html", carreras=carreras, usuarios=usuarios, materias=materias, s_materias=s_materias, up=up)

@app.route("/miscelaneos", methods=['POST'])
@login_required
def miscelaneos():
    if request.form.get('minfo'):
        m = Materia.query.get(int(request.form.get('mid')))
        horarios = Horario.query.filter_by(activo=True).filter_by(materia=int(request.form.get('mid')))
        return render_template("miscelaneos.html", m=m, horarios=horarios, minfo=True)
    if request.form.get('halta'):
        h = Horario(dia=request.form.get('hdia'), desde=request.form.get('hhorad'), hasta=request.form.get('hhorah'), inicio=request.form.get('hfechad'), fin=request.form.get('hfechah'), sala=request.form.get('hsala'), materia=int(request.form.get('mhid')), activo=True)
        db.session.add(h)
        db.session.commit()
        horarios = Horario.query.filter_by(activo=True).filter_by(materia=int(request.form.get('mhid')))
        return render_template("miscelaneos.html",s_horarios=True,horarios=horarios)

@app.route("/salir")
def salir():
    logout_user()
    return redirect(url_for('ingresar'))


@app.route("/estado", methods=['POST','GET'])
@login_required
def estado():
    return render_template("estado.html")





"""ESTOS SON LOS MODELOS"""

app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

class TipoUsuario(db.Model):
    __tablename__ = "tipo_usuario"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(60), nullable=False)

    def __init__(self, descripcion):
        self.descripcion = descripcion

class Materia(db.Model):
    __tablename__ = "materias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    codigo = db.Column(db.String(20),nullable=False)
    curso = db.Column(db.String(10),nullable=False)
    seccion = db.Column(db.String(10),nullable=False)
    carrera = db.Column(db.Integer, db.ForeignKey("carreras.id"), nullable=False)
    docente = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    activo  = db.Column(db.Boolean(), default=True, nullable=False)

class Horario(db.Model):
    __tablename__ = "horarios"
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(10), nullable=False)
    desde = db.Column(db.String(10), nullable=False)
    hasta = db.Column(db.String(10), nullable=False)
    inicio = db.Column(db.String(10), nullable=False)
    fin = db.Column(db.String(10), nullable=False)
    sala = db.Column(db.String(10), nullable=False)
    materia = db.Column(db.Integer, db.ForeignKey("materias.id"), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)

class Carrera(db.Model):
    __tablename__ = "carreras"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    responsable = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    ci = db.Column(db.Integer, default=0,nullable=False)
    email = db.Column(db.String(128), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)
    con = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.Integer, db.ForeignKey("tipo_usuario.id"), nullable=False)

    def is_authenticated(self):
	    return True

    def is_active(self):
    	return True

    def is_anonymous(self):
    	return False

    def get_id(self):
    	return str(self.id)

    def is_admin(self):
    	return self.admin
