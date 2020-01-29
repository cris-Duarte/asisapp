from flask import Flask, jsonify, render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_login import LoginManager,login_user,logout_user,login_required, current_user
from flask_bootstrap import Bootstrap
from datetime import datetime, date, timedelta
import calendar


app = Flask(__name__)
Bootstrap(app)
app.secret_key = b'\x9f\xa5\xb3\xaa\xfa\x8f\xdc\xe4;\xdbf_\x9a\xd2\x1dP'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "ingresar"


@app.route("/")
def index():
    return render_template('registroalumnos.html')

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
    mh = db.session.query(Materia, Carrera, Horario)\
    .filter(Materia.docente == current_user.id)\
    .filter(Materia.carrera==Carrera.id)\
    .filter(Materia.id==Horario.materia)\
    .filter(Materia.activo==True)\
    .filter(Horario.activo==True)\
    .all()
    t = Tiempo()
    clase_hoy = []
    clase_semana = []

    for materia in mh:
        if t.interfecha(materia[2].inicio,materia[2].fin):
            if t.eshoy(materia[2].dia):
                clase_hoy.append(materia)
            else:
                clase_semana.append(materia)

    return render_template("perfil.html",clase_hoy=clase_hoy,clase_semana=clase_semana,ahora=t.fecha(),hora=t.hora())

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
        materias = db.session.query(Materia)\
            .join(Carrera)\
            .filter(Materia.activo == True)\
            .order_by(Materia.id.asc())\
            .all()
        """materias = Materia.query.filter_by(activo=True).all()"""
        usuarios = Usuario.query.filter_by(activo=True).all()
        return render_template("materias.html", carreras=carreras, usuarios=usuarios, materias=materias, s_materias=s_materias, up=up)

@app.route("/miscelaneos", methods=['POST'])
@login_required
def miscelaneos():
    if request.form.get('minfo'):
        m = Materia.query.get(int(request.form.get('mid')))
        materias = db.session.query(Materia)\
            .join(Carrera, Usuario)\
            .filter(Materia.activo == True)\
            .all()
        horarios = Horario.query.filter_by(activo=True).filter_by(materia=int(request.form.get('mid')))
        return render_template("miscelaneos.html", m=m, horarios=horarios, minfo=True)
    if request.form.get('halta'):
        h = Horario(dia=request.form.get('hdia'), desde=request.form.get('hhorad'), hasta=request.form.get('hhorah'), inicio=request.form.get('hfechad'), fin=request.form.get('hfechah'), sala=request.form.get('hsala'), materia=int(request.form.get('mhid')), activo=True)
        db.session.add(h)
        db.session.commit()
        horarios = Horario.query\
        .filter_by(activo=True)\
        .filter_by(materia=int(request.form.get('mhid')))\
        .order_by(Horario.id.asc())\
        .all()
        m = Materia.query.get(int(request.form.get('mhid')))
        return render_template("miscelaneos.html",s_horarios=True,horarios=horarios,m=m)

    if request.form.get('hbaja'):
        h = Horario.query.get(int(request.form.get('hid')))
        h.activo = False
        db.session.commit()
        horarios = Horario.query.filter_by(activo=True).filter_by(materia=int(request.form.get('mid')))
        s_horarios = True
        return render_template("miscelaneos.html",s_horarios=True,horarios=horarios)
    if request.form.get('hmodificacion'):
        h = Horario.query.get(int(request.form.get('hid')))
        m = Materia.query.get(int(request.form.get('mid')))
        return render_template("miscelaneos.html",h=h,m=m,hmod=True)

    if request.form.get('modHorario'):
        h = Horario.query.get(int(request.form.get('hid')))
        h.dia = request.form.get('hdia')
        h.inicio = request.form.get('hfechad')
        h.fin = request.form.get('hfechah')
        h.desde = request.form.get('hhorad')
        h.hasta = request.form.get('hhorah')
        h.sala = request.form.get('hsala')
        db.session.commit()
        s_horarios = True
        horarios = Horario.query\
        .filter_by(activo=True)\
        .filter_by(materia=h.materia)\
        .order_by(Horario.id.asc())\
        .all()
        return render_template("miscelaneos.html",s_horarios=True,horarios=horarios)

@app.route("/salir")
def salir():
    logout_user()
    return redirect(url_for('ingresar'))


@app.route("/alumnos", methods=['POST'])
def alumnos():
    if request.form.get('verificarMateria'):
        m = db.session.query(Materia, Carrera, Usuario)\
        .filter(Materia.carrera == Carrera.id)\
        .filter(Materia.docente == Usuario.id)\
        .filter(Materia.codigo == request.form.get('v'))\
        .filter(Materia.activo == True).first()
        if m:
            return jsonify({
              "Materia": m.Materia.nombre,
              "Curso": m.Materia.curso,
              "Seccion": m.Materia.seccion,
              "Carrera": m.Carrera.nombre_carrera,
              "Docente": m.Usuario.nombre + " " + m.Usuario.apellido,
              "mensaje":"Ok"
          })
        else:
            return jsonify({"mensaje":"El código de clase no es válido "})
    if request.form.get('verificarAlumno'):
        a = Alumno.query\
        .filter(Alumno.ci == request.form.get('v'))\
        .first()
        if a:
            return ({
              "registro":"listo",
              "nombre":a.nombre,
              "apellido":a.apellido,
              "email":a.email,
              "telefono":a.telefono
          })
        else:
            return jsonify({
              "registro":"falta"
          })

    if request.form.get('alta_alumno'):
        a = Alumno.query.filter_by(ci=request.form.get('aci')).first()
        if a:
            m = Materia.query.filter_by(codigo=request.form.get('cmateria')).first()
            c = Inscripcion.query\
            .filter(Inscripcion.materia == m.id)\
            .filter(Inscripcion.alumno ==a.id)\
            .all()
            if c:
                return jsonify({
                    'clase':'alert-danger',
                    'mensaje':'Ya te has registrado a '+m.nombre
                })
            else:
                i = Inscripcion(materia=m.id,alumno=a.id)
                q = db.session.add(i)
                db.session.commit()
                return jsonify({
                    "clase":'alert-success',
                    "mensaje": "Bien hecho "+a.nombre+' '+a.apellido+'!!, te has registrado a '+m.nombre
                    })
        else:
            a = Alumno(\
            nombre=request.form.get('anombre'),\
            apellido=request.form.get('aapellido'),\
            ci=request.form.get('aci'),\
            con=request.form.get('aci'),\
            email=request.form.get('aemail'),\
            telefono=request.form.get('atelefono'),\
            activo=True)
            db.session.add(a)
            db.session.commit()
            m = Materia.query.filter_by(codigo=request.form.get('cmateria')).first()
            i = Inscripcion(materia=m.id,alumno=a.id)
            q = db.session.add(i)
            db.session.commit()
            return jsonify({
                "clase":'alert-success',
                "mensaje": "Bien hecho "+a.nombre+' '+a.apellido+'!!, te has registrado a '+m.nombre
                })


class Tiempo():
    def __init__(self):
        self.date = datetime.now()
    def hora(self):
        h = "{}:{}:{}".format(self.date.hour, self.date.minute, self.date.second)
        return h
    def fecha(self):
        meses = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        dias = ("Lunes", "Martes","Miercoles","Jueves","Viernes","Sabado","Domingo")
        numero_dia = self.date.day
        mes = meses[self.date.month - 1]
        dia = dias[self.date.isoweekday() - 1]
        anho = self.date.year
        f = "{}, {} de {} del {}".format(dia, numero_dia, mes, anho)
        return f

    def eshoy(self,d):
        dias = ("Lunes", "Martes","Miercoles","Jueves","Viernes","Sabado","Domingo")
        numero_dia = self.date.day
        dia = dias[self.date.isoweekday() - 1]
        if dia == d:
            return True
        else:
            return False

    def interfecha(self,i,f):
        inicio = datetime.strptime(i,"%Y-%m-%d")
        fin = datetime.strptime(f,"%Y-%m-%d")
        if self.date > inicio and self.date < fin:
            return True
        else:
            return False
    def esahora(self,d,h):
        desde = datetime.strptime(d, "%H:%M")
        hasta = datetime.strptime(h, "%H:%M")
        strahora = str(self.date.hour)+":"+str(self.date.minute)
        ahora = datetime.strptime(strahora, "%H:%M")
        if ahora < hasta and ahora > desde:
            i = hasta - ahora
            return i.seconds
        else:
            return False


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
    carrera = db.Column(db.Integer, db.ForeignKey("carreras.id"))
    docente = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    activo  = db.Column(db.Boolean(), default=True, nullable=False)
    inscriptos = db.relationship('Inscripcion', backref='inscripcion_materia', lazy=True)

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
    nombre_carrera = db.Column(db.String(30), nullable=False)
    materias = db.relationship('Materia', backref='carreras', lazy=True)
    responsable = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    ci = db.Column(db.Integer, default=0,nullable=False)
    email = db.Column(db.String(128), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)
    con = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.Integer, db.ForeignKey("tipo_usuario.id"), nullable=False)
    docentes = db.relationship('Materia', backref='docentes', lazy=True)

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

class Inscripcion(db.Model):
    __tablename__="inscripciones"
    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.Integer, db.ForeignKey("materias.id"), nullable=False)
    alumno = db.Column(db.Integer, db.ForeignKey("alumnos.id"), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)


class Alumno(db.Model):
    __tablename__ = "alumnos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    ci = db.Column(db.Integer, default=0,nullable=False)
    email = db.Column(db.String(128), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)
    con = db.Column(db.String(200), nullable=False)
    inscriptos = db.relationship('Inscripcion', backref='inscripcion_alumnos', lazy=True)
