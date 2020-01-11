from flask import Flask, jsonify, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
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
    return render_template("ingresar.html")


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)

@app.route("/dashboard", methods=['POST','GET'])
def dashboard():
    email = request.form.get("correo")
    c = request.form.get('c')
    u = Usuario.query.filter(and_(Usuario.email == email, Usuario.con == c)).first()
    if not u or u is None:
        return render_template("dashboard.html",mensaje="Error de acceso: Correo Electrónico o Contraseña incorrectos")
    else:
        load_user(u.id)
        return render_template("dashboard.html")


@app.route("/salir")
@login_required
def salir():
    logout_user()
    return render_template("index.html")


@app.route("/estado")
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
