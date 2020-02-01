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
                dc = Diadeclase.query.filter(and_(Diadeclase.horario==materia[2].id,Diadeclase.fecha==t.fecha()))
                if dc.count() == 0:
                    dc = Diadeclase(horario=materia[2].id,fecha=t.fecha())
                    db.session.add(dc)
                    db.session.commit()
                dc = Diadeclase.query.filter(and_(Diadeclase.horario==materia[2].id,Diadeclase.fecha==t.fecha())).first()
                materia[2].diadeclase = dc.id
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

    if request.form.get('a_modificar'):
        m = Materia.query.get(request.form.get('mid'))
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
        return jsonify({
        "id":m.id,
        "nombre":m.nombre,
        "codigo":m.codigo,
        "curso":m.curso,
        "seccion":m.seccion,
        "carrera":m.carrera,
        "docente":m.docente
        })
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

@app.route("/detallemateria", methods=['POST'])
@login_required
def detallemateria():
    s_horarios = False
    if request.form.get('halta'):
        h = Horario(\
        dia=request.form.get('hdia'),\
        desde=request.form.get('hhorad'),\
        hasta=request.form.get('hhorah'),\
        periodo=request.form.get('hperiodo'),\
        sala=request.form.get('hsala'),\
        materia=int(request.form.get('mid')))
        db.session.add(h)
        db.session.commit()
        s_horarios = True
    if request.form.get('hbaja'):
        h = Horario.query.get(int(request.form.get('hid')))
        h.activo = False
        db.session.commit()
        s_horarios = True

    if request.form.get('modHorario'):
        h = Horario.query.get(int(request.form.get('hid')))
        h.dia = request.form.get('hdia')
        h.periodo = request.form.get('hperiodo')
        h.desde = request.form.get('hhorad')
        h.hasta = request.form.get('hhorah')
        h.sala = request.form.get('hsala')
        db.session.commit()
        s_horarios = True

    if request.form.get('hmodificacion'):
        h = Horario.query.get(int(request.form.get('hid')))
        return jsonify({
        "id":h.id,
        "dia":h.dia,
        "periodo":h.periodo,
        "desde":h.desde,
        "hasta":h.hasta,
        "sala":h.sala
        })
    else:
        m = Materia.query.get(int(request.form.get('mid')))
        periodos = Periodo.query\
        .filter(Periodo.activo==True)\
        .all()
        horarios = Horario.query.filter_by(activo=True).filter_by(materia=int(request.form.get('mid')))
        return render_template("detallemateria.html",s_horarios=s_horarios, m=m,periodos=periodos, horarios=horarios, minfo=True)

@app.route("/periodos", methods=['POST'])
@login_required
def periodos():
    s_periodos = False
    if request.form.get('altaperiodo'):
        p = Periodo(\
        nombre_periodo=request.form.get('pnombre'),\
        inicio=request.form.get('pfechad'),\
        fin=request.form.get('pfechah'))
        db.session.add(p)
        db.session.commit()
        s_periodos = True

    if request.form.get('bajaperiodo'):
        p = Periodo.query.get(int(request.form.get('pid')))
        p.activo = False
        db.session.commit()
        s_periodos = True
    if request.form.get('guardarmodperiodo'):
        p = Periodo.query.get(int(request.form.get('pid')))
        p.nombre_periodo=request.form.get('pnombre')
        p.inicio=request.form.get('pfechad')
        p.fin=request.form.get('pfechah')
        db.session.commit()
        s_periodos = True

    if request.form.get('modperiodo'):
        p = Periodo.query.get(int(request.form.get('pid')))
        return jsonify({
        "id":p.id,
        "nombre":p.nombre_periodo,
        "inicio":p.inicio,
        "fin":p.fin
        })
    else:
        periodos = Periodo.query\
        .filter(Periodo.activo==True)\
        .all()
        return render_template('periodos.html',s_periodos=s_periodos,periodos=periodos)


@app.route("/salir")
def salir():
    logout_user()
    return redirect(url_for('ingresar'))


@app.route("/alumnos", methods=['POST'])
@login_required
def alumnos():
    if request.form.get('rca'):
        c = Materia.query.filter_by(id = int(request.form.get('m'))).first()
        c = c.cantidad
        return str(c)

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
                t = Tiempo()
                i = Inscripcion(materia=m.id,alumno=a.id,fecha=t.fecha())
                m.cantidad += 1
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
            t = Tiempo()
            i = Inscripcion(materia=m.id,alumno=a.id, fecha=t.fecha())
            m.cantidad += 1
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
            return True
        else:
            return False

@app.route("/lista/<int:d>", methods=['GET'])
@login_required
def lista(d):
    diadeclase = db.session.query(Carrera, Materia, Horario, Diadeclase)\
    .filter(Diadeclase.id==d)\
    .first()

    alumnos = i = db.session.query(Inscripcion)\
    .join(Alumno)\
    .filter(Inscripcion.materia==diadeclase[1].id)\
    .all()
    t = Tiempo()
    ahora = t.esahora(diadeclase.Horario.desde,diadeclase.Horario.hasta)

    return render_template('lista.html',dc=diadeclase,alumnos=alumnos, ahora=ahora,hora=t.hora())



@app.route("/listar", methods=['POST'])
@login_required
def listar():
    alumno = request.form.get('ida')
    diadeclase = request.form.get('idc')
    condicion = request.form.get('condicion')
    t = Tiempo()

    asis = Asistencia.query\
    .filter(and_(Asistencia.alumno==alumno,Asistencia.diadeclase==diadeclase)).first()

    if not asis:
        asistencia = Asistencia(diadeclase=diadeclase,alumno=alumno,hora=t.hora(),condicion=condicion,tipo='Entrada')
        db.session.add(asistencia)
        db.session.commit()
    else:
        asis.condicion = condicion
        db.session.commit()

    a = db.session.query(Alumno)\
    .join(Asistencia)\
    .filter(Asistencia.diadeclase==diadeclase)\
    .filter(Asistencia.alumno==Alumno.id)\
    .filter(Alumno.id==alumno)\
    .first()

    return jsonify({
      "nombre": a.apellido+", "+a.nombre,
      "condicion": a.asistencias[0].condicion
  })

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
    cantidad = db.Column(db.Integer, default=0, nullable=False)
    carrera = db.Column(db.Integer, db.ForeignKey("carreras.id"))
    docente = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    activo  = db.Column(db.Boolean(), default=True, nullable=False)
    inscriptos = db.relationship('Inscripcion', backref='inscripcion_materia', lazy=True)
    horariosmateria = db.relationship('Horario', backref='horariosmateria', lazy=True)

class Horario(db.Model):
    __tablename__ = "horarios"
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(10), nullable=False)
    desde = db.Column(db.String(10), nullable=False)
    hasta = db.Column(db.String(10), nullable=False)
    sala = db.Column(db.String(10), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)
    diasdeclases = db.relationship('Diadeclase', backref='diasdeclases', lazy=True)
    materia = db.Column(db.Integer, db.ForeignKey("materias.id"), nullable=False)
    periodo = db.Column(db.Integer, db.ForeignKey("periodos.id"), nullable=False)



class Periodo(db.Model):
    __tablename__ = "periodos"
    id = db.Column(db.Integer, primary_key=True)
    nombre_periodo = db.Column(db.String(100), nullable=False)
    inicio = db.Column(db.String(20), nullable=False)
    fin = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)
    horariosperiodo = db.relationship('Horario', backref='horariosperiodo', lazy=True)


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
    fecha = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)

class Diadeclase(db.Model):
    __tablename__ = "diasdeclases"
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.Integer, db.ForeignKey("horarios.id"), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)
    llamados = db.Column(db.Integer, default=0,nullable=False)
    asistentes = db.Column(db.Integer, default=0,nullable=False)

class Asistencia(db.Model):
    __tablename__= "asistencias"
    id = db.Column(db.Integer, primary_key=True)
    diadeclase = db.Column(db.Integer, db.ForeignKey("diasdeclases.id"), nullable=False)
    alumno = db.Column(db.Integer, db.ForeignKey("alumnos.id"), nullable=False)
    hora = db.Column(db.String(15), nullable=False)
    condicion = db.Column(db.String(25), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)

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
    asistencias = db.relationship('Asistencia', backref='asistencias', lazy=True)
