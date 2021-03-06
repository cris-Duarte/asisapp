from flask import Flask, jsonify, render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_login import LoginManager,login_user,logout_user,login_required, current_user
from flask_bootstrap import Bootstrap
from datetime import datetime, date, timedelta
import calendar
import json
import os
from FlaskGoogleLogin import GoogleLogin
from google.oauth2 import id_token
from google.auth.transport import requests
import string
import random
import pygal

app = Flask(__name__)
Bootstrap(app)
app.secret_key = b'\x9f\xa5\xb3\xaa\xfa\x8f\xdc\xe4;\xdbf_\x9a\xd2\x1dP'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "gLogin"

googlelogin = GoogleLogin(app)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
## 5432 - 1337 - 5000
## Google Login Try

@app.route("/gLogin")
def gLogin():
    if current_user.is_active:
        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html",g=GOOGLE_CLIENT_ID)

@app.route('/gCallback', methods=['POST'])
def create_or_update_user():
    token = request.form.get('idtoken')
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        mensaje = 'Wrong issuer.'
    user = Usuario.query.filter_by(email=idinfo['email']).first()
    if user:
        db.session.add(user)
        db.session.flush()
        u = load_user(user.id)
        login_user(user,remember=True, force=False, fresh=True)

        return redirect(url_for('dashboard'))
    else:
        return render_template('error.html')

## Login System LEGACY
@app.route("/ingresar")
def ingresar():
    if current_user.is_active:
        return redirect(url_for('dashboard'))
    else:
        return render_template("ingresar.html")

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

@app.route("/login", methods=['POST'])
def login():
    email = request.form.get("correo")
    c = request.form.get('c')
    u = Usuario.query.filter(and_(Usuario.email == email, Usuario.con == c)).first()
    if not u or u is None:
        return render_template("dashboard.html",mensaje="Error de acceso: Correo Electrónico o Contraseña incorrectos")
    else:
        u = load_user(u.id)
        login_user(u,remember=True, force=False, fresh=True)
        return redirect(url_for('dashboard'), code=303)

@app.route("/salir", methods=['POST'])
def salir():
    logout_user()
    return redirect(url_for('ingresar'))

## FIN LOGIN SYSTEM

@app.route("/listaclases", methods=['POST'])
def listaclases():
    if request.form.get('des'):
        d = Diadeclase.query.get(str(request.form.get('dia')))
        d.activo = False
        db.session.commit()
    if request.form.get('hab'):
        d = Diadeclase.query.get(str(request.form.get('dia')))
        d.activo = True
        db.session.commit()
    if request.form.get('fecha'):
        f = datetime.strptime(request.form.get('fecha'),"%Y-%m-%d")
        listas = Diadeclase.query\
        .filter(Diadeclase.fecha==str(f))\
        .order_by(Diadeclase.id.asc())\
        .all()
        for dia in listas:
            dia.fhr = fecha_hr(dia.fecha)
            dia.valido = fecha_valida(dia.fecha)
        b = 'f'
    if request.form.get('codigo'):
        listas = db.session.query(Materia)\
        .join(Horario,Diadeclase)\
        .filter(Materia.codigo==request.form.get('codigo'))\
        .order_by(Diadeclase.id.asc())\
        .first()
        b = 'c'
    return render_template('lista-clases.html',listas=listas,b=b)


@app.route("/")
def index():
    return render_template('consultaalumnos.html')

@app.route("/detalleasistencia", methods=['POST'])
def detalleasistencia():
    materia = request.form.get('materia')
    d = db.session.query(Diadeclase)\
    .join(Horario, Materia)\
    .filter(Diadeclase.activo==True)\
    .filter(Horario.activo==True)\
    .filter(Materia.activo==True)\
    .filter(Materia.id==materia)\
    .order_by(Diadeclase.fecha.asc())\
    .all()
    if request.form.get('alumno'):
        ci = request.form.get('alumno')
        a = Alumno.query.filter_by(ci=ci).first()
    else:
        id = request.form.get('ida')
        a = Alumno.query.get(id)
    for dia in d:
        f = fecha_simple(dia.fecha)
        dia.fecha_simple = f
        dia.valido = fecha_valida(dia.fecha)
        e = Asistencia.query\
        .filter(and_(Asistencia.alumno==a.id,Asistencia.diadeclase==dia.id))
        if e.all():
            if e.count() == 1:
                ea = e.first()
                if ea.tipo == 'Entrada':
                    dia.entrada = acron(ea.condicion)
                    dia.salida = 'A'
                else:
                    dia.entrada = 'A'
                    dia.salida = acron(ea.condicion)
            else:
                ea = e.all()
                if e[0].tipo == 'Entrada':
                    dia.entrada = acron(e[0].condicion)
                    dia.salida = acron(e[1].condicion)
                else:
                    dia.entrada = acron(e[1].condicion)
                    dia.salida = acron(e[0].condicion)
        else:
            t = Tiempo()
            c = datetime.strptime(dia.fecha,"%Y-%m-%d %H:%M:%S")
            if c < t.fecha_com():
                dia.entrada = 'A'
                dia.salida = 'A'
    if request.form.get('vistaAlumno'):
        return render_template('detalleAsistenciaAlumno.html',dias=d)
    else:
        return render_template('detalleasistencia.html',alumno=a,dias=d)

"""
@app.route("/registrodocentes")
def registrodocentes():
    return render_template('registrodocentes.html')

@app.route("/docentes", methods=['POST'])
def docentes():
    if request.form.get('altadocente'):
        d = Usuario(\
        nombre=request.form.get('dnombre'),\
        apellido=request.form.get('dapellido'),\
        ci=request.form.get('dci'),\
        email=request.form.get('demail'),\
        telefono=request.form.get('dtelefono'),\
        con=request.form.get('dcon'),
        tipo=3,\
        activo=True)
        db.session.add(d)
        db.session.commit()
        return jsonify({
            'nombre':d.nombre+' '+d.apellido
        })
    elif request.form.get('verificard'):
        d = Usuario.query.filter_by(ci=request.form.get('dci'))
        if d.count()>0:
            d = d.first()
            return jsonify({
                'estado':'ya',
                'nombre':d.nombre+' '+d.apellido
            })
        else:
            return jsonify({
            'estado':'aun_no'
            })
"""

@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    return render_template("dashboard.html",g=GOOGLE_CLIENT_ID)

@app.route("/listasistencia", methods=['POST'])
@login_required
def listasistencia():
    m = db.session.query(Materia)\
    .join(Inscripcion,Alumno)\
    .filter(Materia.id==request.form.get('materia'))\
    .filter(Materia.activo==True)\
    .first()
    if m:
        d = calculardias(m.id)
        for alumno in m.inscriptos:
            if d>0 :
                alumno.asistencia = calcularasistencia(alumno.alumno,d,m.id)
            else:
                alumno.asistencia = 0
    else:
        d = 0
    return render_template('lista-asistencia.html',m=m)

@app.route("/detasistencia", methods=['POST'])
def detasistencia():
    ci = request.form.get('ci')
    a = Alumno.query.filter_by(ci=ci).first()
    materias = db.session.query(Materia)\
    .join(Inscripcion)\
    .filter(Inscripcion.activo==True)\
    .filter(Inscripcion.alumno==a.id)\
    .filter(Materia.activo==True)\
    .all()
    t = Tiempo()
    for materia in materias:
        d = calculardias(materia.id)
        if d > 0:
            materia.asistencia = calcularasistencia(a.id,d,materia.id)
        if materia.periodo:
            materia.actual = t.interfecha(materia.materiasperiodo.inicio,materia.materiasperiodo.fin)

    return render_template('vistaMateriasAlumno.html',materias=materias,a=a.id)

@app.route("/misclases", methods=['POST'])
@login_required
def misclases():
    clases = db.session.query(Carrera)\
    .join(Materia, Periodo)\
    .filter(Materia.docente==current_user.id)\
    .filter(Materia.activo==True)\
    .all()
    t = Tiempo()
    for carrera in clases:
        for materia in carrera.materias:
            if materia.periodo:
                materia.actual = t.interfecha(materia.materiasperiodo.inicio,materia.materiasperiodo.fin)
    return render_template('misclases.html',clases=clases)

@app.route("/perfil", methods=['POST'])
@login_required
def perfil():
    mh = db.session.query(Materia, Carrera, Horario, Periodo)\
    .filter(Materia.docente == current_user.id)\
    .filter(Materia.carrera==Carrera.id)\
    .filter(Materia.id==Horario.materia)\
    .filter(Materia.periodo==Periodo.id)\
    .filter(Materia.activo==True)\
    .filter(Horario.activo==True)\
    .all()
    t = Tiempo()
    clase_hoy = []
    clase_semana = []

    for materia in mh:
        if t.interfecha(materia.Periodo.inicio,materia.Periodo.fin):
            d = db.session.query(Diadeclase)\
            .join(Horario)\
            .filter(Horario.activo==True)\
            .filter(Horario.id==Diadeclase.horario)\
            .filter(Diadeclase.horario==materia.Horario.id)\
            .filter(Diadeclase.fecha==str(t.s_fecha()))

            if t.eshoy(materia.Horario.dia):
                if d.count() == 1:
                    materia.Horario.diadeclase=d[0].id
                    dia = d.first()
                else:
                    materia.Horario.diadeclase='Error con el id de clase'
                if dia.activo:
                    clase_hoy.append(materia)
            else:
                clase_semana.append(materia)

    return render_template("perfil.html",clase_hoy=clase_hoy,clase_semana=clase_semana,ahora=t.fecha(),hora=t.hora())

@app.route("/consultaintervalo", methods=['POST'])
@login_required
def consultaintervalo():
    dt = datetime.strptime(request.form.get('cdesde'),"%Y-%m-%d")
    ht = datetime.strptime(request.form.get('chasta'),"%Y-%m-%d")
    if ht > dt:
        graph = pygal.Line(height=400)
        if request.form.get('porcentaje'):
            g = Grafico(dt,ht,True)
        else:
            g = Grafico(dt,ht,False)
        graph.x_labels = g.lx()
        general = True
        ca = Carrera.query.all()
        cacount = 0
        for c in ca:
            if request.form.get("carrera"+str(c.id)):
                caid = c.id
                general = False
                cacount += 1
        cu = Curso.query.all()
        cucount = 0
        for cr in cu:
            if request.form.get("curso"+str(cr.id)):
                crid = cr.id
                general = False
                cucount += 1
        if cucount==1 and cacount==1:
            ca = Carrera.query.get(caid)
            cu = Curso.query.get(crid)
            if request.form.get('consultadetmaterias'):
                graph = pygal.Bar(height=400)
                graph.x_labels = g.lx()
                titulo = 'Presencia: '+cu.descripcion+' - '+ca.nombre_carrera+', del '+fecha_hr(str(dt))+" al "+fecha_hr(str(ht))
                mcon = Materia.query\
                .filter(Materia.carrera==caid)\
                .filter(Materia.curso==crid)\
                .all()
                for m in mcon:
                    cd = db.session.query(Diadeclase)\
                    .join(Horario, Materia)\
                    .filter(Materia.id == m.id)\
                    .count()
                    if cd > 0:
                        graph.add(m.nombre, g.lym(m.id))
            else:
                graph.add(cr.descripcion, g.ly(caid,crid))
                titulo = 'Presencia: '+cu.descripcion+' - '+ca.nombre_carrera+', del '+fecha_hr(str(dt))+" al "+fecha_hr(str(ht))
        else:
            if cucount > 1 and cacount == 1:
                for cr in cu:
                    if request.form.get("curso"+str(cr.id)):
                        graph.add(cr.descripcion, g.ly(caid,cr.id))
                caux2 = Carrera.query.get(caid)
                titulo = 'Presencia: '+caux2.nombre_carrera+', del '+fecha_hr(str(dt))+" al "+fecha_hr(str(ht))

            if cucount == 1 and cacount > 1:
                for c in ca:
                    if request.form.get("carrera"+str(c.id)):
                        graph.add(c.nombre_carrera, g.ly(c.id,crid))
                caux2 = Curso.query.get(crid)
                titulo = 'Presencia: '+caux2.descripcion+', del '+fecha_hr(str(dt))+" al "+fecha_hr(str(ht))

            if cucount == 0 and cacount > 0:
                for c in ca:
                    if request.form.get("carrera"+str(c.id)):
                        graph.add(c.nombre_carrera, g.ly(c.id,False))
                titulo = 'Presencia General de Carreras: del '+fecha_hr(str(dt))+" al "+fecha_hr(str(ht))

            if cucount > 0 and cacount == 0:
                for cr in cu:
                    if request.form.get("curso"+str(cr.id)):
                        graph.add(cr.descripcion, g.ly(False,cr.id))
                titulo = 'Presencia General de Cursos: del '+fecha_hr(str(dt))+" al "+fecha_hr(str(ht))

            if general:
                graph.add("General", g.ly('g',False))
                titulo = 'Presencia desde '+fecha_hr(str(dt))+" hasta "+fecha_hr(str(ht))
        if request.form.get('porcentaje'):
            graph.title = "( % ) "+titulo
        else:
            graph.title = "Cant. "+titulo
        graph_data = graph.render_data_uri()
        return render_template('consultaintervalo.html',graph_data=graph_data)
    else:
        return render_template('consultaintervalo.html',mensaje="Intervalo invalido")

@app.route("/consultas", methods=['POST'])
@login_required
def consultas():
    g = [0,0,0,0,0,0,'']
    t = Tiempo()
    query = db.session.query(Diadeclase)\
    .join(Horario, Materia)

    if request.form.get('cfecha'):
        fecha =  str(request.form.get('cfecha'))+" 00:00:00"
        g[6] = str(fecha_hr(fecha))
    else:
        fecha = str(t.s_fecha())
        g[6] = 'Hoy'
    ccarrera = request.form.get('ccarrera')
    if ccarrera:
        query = query.filter(Materia.carrera==ccarrera)
        carrera = Carrera.query.get(ccarrera)
        g[6] = g[6]+' '+str(carrera.nombre_carrera)
    ccurso =request.form.get('ccurso')
    if ccurso:
        query = query.filter(Materia.curso==ccurso)
        curso = Curso.query.get(ccurso).descripcion
        g[6] = g[6]+' '+curso
    if request.form.get('cseccion'):
        query = query.filter(Materia.seccion==request.form.get('cseccion'))
        g[6] = g[6]+' '+request.form.get('cseccion')

    d = query.all()
    for dias in d:
        if dias.fecha == fecha:
            g[0] = g[0] + 1
            i = Inscripcion.query\
            .filter(Inscripcion.materia==dias.diasdeclases.horariosmateria.id)\
            .count()
            g[1] = g[1] + i
            a = Asistencia.query\
            .filter(Asistencia.diadeclase==dias.id)\
            .filter(Asistencia.tipo=='Entrada')\
            .filter(Asistencia.condicion=='Presente')\
            .count()
            g[2] = g[2] + a
            a = Asistencia.query\
            .filter(Asistencia.diadeclase==dias.id)\
            .filter(Asistencia.tipo=='Salida')\
            .filter(Asistencia.condicion=='Presente')\
            .count()
            g[4] = g[4] + a
    if g[1] == 0:
        g[3] = 0
        g[5] = 0
    else:
        g[3] = round(g[2]*100/g[1],0)
        g[5] = round(g[4]*100/g[1],0)

    graph = pygal.Pie(width=250,height=150, explicit_size=True)
    p = g[2]+g[4]
    a = (2*g[1])-g[2]-g[4]
    graph.add('Presente',p)
    graph.add('Ausente',a)
    graph_data = graph.render_data_uri()

    carreras = Carrera.query\
    .filter_by(activo=True)\
    .all()
    cursos = Curso.query.all()
    if request.form.get('consulta'):
        return render_template('detconsultamin.html',g=g,graph_data=graph_data)
    else:
        return render_template('consultas.html',g=g,carreras=carreras,cursos=cursos,graph_data=graph_data)

@app.route("/usuario", methods=['POST'])
@login_required
def usuario():
    if request.form.get('mod'):
        ui = Usuario.query.get(current_user.id)
        ui.nombre = request.form.get('inombre')
        ui.apellido = request.form.get('iapellido')
        ui.ci = request.form.get('ici')
        ui.email = request.form.get('iemail')
        ui.telefono = request.form.get('itelefono')
        db.session.commit()
    u = db.session.query(Usuario)\
    .join(TipoUsuario)\
    .filter(Usuario.id==current_user.id)\
    .first()
    return render_template('usuario.html',u=u)

@app.route("/materias", methods=['POST'])
@login_required
def materias():
    cursos = Curso.query.all()
    carreras = Carrera.query.filter_by(activo=True).all()
    usuarios = Usuario.query.filter_by(activo=True).all()
    periodos = Periodo.query.filter_by(activo=True).all()
    return render_template("materias.html", carreras=carreras, usuarios=usuarios,cursos=cursos,periodos=periodos)

@app.route("/listamaterias", methods=['POST'])
@login_required
def listamaterias():
    if request.form.get('alta'):
        m = Materia(\
        nombre=request.form.get('mnombre'),\
        codigo=codigo(),\
        curso=request.form.get('mcurso'),\
        seccion=request.form.get('mseccion'),\
        carrera=int(request.form.get('mcarrera')),\
        docente=int(request.form.get('mdocente')),\
        periodo=request.form.get('mperiodo'),\
        activo = True)
        db.session.add(m)
        db.session.commit()
    if request.form.get('baja'):
        m = Materia.query.get(int(request.form.get('mid')))
        m.activo = False
        db.session.commit()
    if request.form.get('modificar'):
        m = Materia.query.get(request.form.get('mid'))
        m.nombre = request.form.get('mnombre')
        m.curso = request.form.get('mcurso')
        m.seccion = request.form.get('mseccion')
        m.carrera = int(request.form.get('mcarrera'))
        m.docente = int(request.form.get('mdocente'))
        m.periodo = request.form.get('mperiodo')
        db.session.commit()
    if request.form.get('mod'):
        m = Materia.query.get(int(request.form.get('mid')))
        if not m.docente:
            d = 0
        else:
            d = m.docente
        if not m.periodo:
            p = 0
        else:
            p = m.periodo
        return jsonify({
        "id":m.id,
        "nombre":m.nombre,
        "curso":m.curso,
        "seccion":m.seccion,
        "carrera":m.carrera,
        "docente":d,
        "periodo":p
        })
    else:
        materias = db.session.query(Materia)\
            .join(Carrera, Curso)\
            .filter(Materia.activo == True)\
            .order_by(Materia.periodo.asc())\
            .order_by(Materia.id.asc())\
            .all()
        return render_template('lista-materias.html',materias=materias)

@app.route("/detallemateria", methods=['POST'])
@login_required
def detallemateria():
    s_horarios = False
    if request.form.get('halta'):
        h = Horario(\
        dia=request.form.get('hdia'),\
        desde=request.form.get('hhorad'),\
        hasta=request.form.get('hhorah'),\
        sala=request.form.get('hsala'),\
        materia=int(request.form.get('mid')))
        db.session.add(h)
        db.session.commit()
        s_horarios = True
        pm = Materia.query.get(request.form.get('mid'))
        p = Periodo.query.get(pm.periodo)
        dias_clases('alta',h.id,h.dia,p.inicio,p.fin)
    if request.form.get('hbaja'):
        h = Horario.query.get(int(request.form.get('hid')))
        h.activo = False
        db.session.commit()
        s_horarios = True

    if request.form.get('modHorario'):
        h = Horario.query.get(int(request.form.get('hid')))
        h.dia = request.form.get('hdia')
        h.desde = request.form.get('hhorad')
        h.hasta = request.form.get('hhorah')
        h.sala = request.form.get('hsala')
        db.session.commit()
        s_horarios = True
        m = Materia.query.get(h.horariosmateria.id)
        p = Periodo.query.get(m.periodo)
        dias_clases('mod',h.id,request.form.get('hdia'),p.inicio,p.fin)

    if request.form.get('hmodificacion'):
        h = Horario.query.get(int(request.form.get('hid')))
        return jsonify({
        "id":h.id,
        "dia":h.dia,
        "desde":h.desde,
        "hasta":h.hasta,
        "sala":h.sala
        })
    else:
        m = Materia.query.get(int(request.form.get('mid')))
        periodos = Periodo.query\
        .filter(Periodo.activo==True)\
        .all()
        horarios = Horario.query\
        .filter_by(activo=True)\
        .filter_by(materia=int(request.form.get('mid')))
        return render_template("detallemateria.html",s_horarios=s_horarios, m=m,periodos=periodos, horarios=horarios, minfo=True)

@app.route("/administracion", methods=['POST'])
@login_required
def administracion():
    coord = Usuario.query\
    .filter(or_(Usuario.tipo == 2, Usuario.tipo == 1))\
    .filter(Usuario.activo == True)\
    .all()
    return render_template('administracion.html',coord=coord)

@app.route("/listacarreras", methods=['POST'])
@login_required
def listacarreras():
    if request.form.get('alta'):
        c = Carrera(\
        nombre_carrera=request.form.get('cnombre'),\
        responsable=request.form.get('ccoordinador'))
        db.session.add(c)
        db.session.commit()
    if request.form.get('baja'):
        c = Carrera.query.get(int(request.form.get('cid')))
        c.activo = False
        db.session.commit()
    if request.form.get('mod'):
        u = Carrera.query.get(int(request.form.get('cid')))
        u.nombre_carrera=request.form.get('cnombre')
        u.responsable=request.form.get('ccoordinador')
        db.session.commit()
    if request.form.get('modificacion'):
        u = Carrera.query.get(int(request.form.get('cid')))
        if not u.responsable:
            coord = 0
        else:
            coord = u.responsable
        return jsonify({
        "id":u.id,
        "nombre":u.nombre_carrera,
        "coordinador":coord
        })
    else:
        carreras = Carrera.query\
        .filter(Carrera.activo == True)\
        .order_by(Carrera.id.asc())\
        .all()
        return render_template('lista-carreras.html',carreras=carreras)

@app.route("/listaperiodos", methods=['POST'])
@login_required
def listaperiodos():
    if request.form.get('alta'):
        p = Periodo(\
        nombre_periodo=request.form.get('pnombre'),\
        inicio=request.form.get('pfechad'),\
        fin=request.form.get('pfechah'))
        db.session.add(p)
        db.session.commit()
    if request.form.get('baja'):
        p = Periodo.query.get(int(request.form.get('pid')))
        p.activo = False
        db.session.commit()
    if request.form.get('mod'):
        p = Periodo.query.get(int(request.form.get('pid')))
        p.nombre_periodo=request.form.get('pnombre')
        p.inicio=request.form.get('pfechad')
        p.fin=request.form.get('pfechah')
        db.session.commit()
    if request.form.get('modificacion'):
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
        .order_by(Periodo.id.asc())\
        .all()
        return render_template('lista-periodos.html',periodos=periodos)

@app.route("/listausuarios", methods=['POST'])
@login_required
def listausuarios():
    if request.form.get('alta'):
        u = Usuario(\
        nombre=request.form.get('unombre'),\
        apellido=request.form.get('uapellido'),\
        ci=request.form.get('uci'),\
        email=request.form.get('uemail'),\
        tipo=request.form.get('utipo'),\
        telefono=request.form.get('utelefono'))
        db.session.add(u)
        db.session.commit()
    if request.form.get('baja'):
        u = Usuario.query.get(int(request.form.get('uid')))
        u.activo = False
        db.session.commit()
    if request.form.get('mod'):
        u = Usuario.query.get(int(request.form.get('uid')))
        u.nombre=request.form.get('unombre')
        u.apellido=request.form.get('uapellido')
        u.ci=request.form.get('uci')
        u.tipo=request.form.get('utipo')
        u.email=request.form.get('uemail')
        u.telefono=request.form.get('utelefono')
        db.session.commit()
    if request.form.get('modificacion'):
        u = Usuario.query.get(int(request.form.get('uid')))
        return jsonify({
        "id":u.id,
        "nombre":u.nombre,
        "apellido":u.apellido,
        "ci":u.ci,
        "tipo":u.tipo,
        "telefono":u.telefono,
        "email":u.email
        })
    else:
        usuarios = db.session.query(Usuario)\
        .join(TipoUsuario)\
        .filter(Usuario.activo == True)\
        .order_by(Usuario.id.asc())\
        .all()
        return render_template('lista-usuarios.html',usuarios=usuarios)

@app.route("/alumnos", methods=['POST'])
@login_required
def alumnos():
    if request.form.get('rca'):
        c = Materia.query.filter_by(id = int(request.form.get('m'))).first()
        c = c.cantidad
        return str(c)

    if request.form.get('verificarMateria'):
        m = db.session.query(Materia, Carrera, Usuario, Curso)\
        .filter(Materia.carrera == Carrera.id)\
        .filter(Materia.docente == Usuario.id)\
        .filter(Materia.codigo == request.form.get('v'))\
        .filter(Materia.activo == True).first()
        if m:
            return jsonify({
              "Materia": m.Materia.nombre,
              "Curso": m.Materia.cursomateria.descripcion,
              "Seccion": m.Materia.seccion,
              "Carrera": m.Carrera.nombre_carrera,
              "Docente": m.Usuario.nombre + " " + m.Usuario.apellido,
              "Periodo": m.Materia.materiasperiodo.nombre_periodo,
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
              "apellido":a.apellido
          })
        else:
            return jsonify({
              "registro":"falta"
          })

    if request.form.get('alta_alumno'):
        a = Alumno.query.filter_by(ci=request.form.get('aci')).first()
        if a:
            m = db.session.query(Materia)\
            .join(Horario)\
            .filter(Materia.codigo==request.form.get('mcodigo'))\
            .filter(Materia.activo==True)\
            .filter(Horario.activo==True)\
            .first()
            c = Inscripcion.query\
            .filter(Inscripcion.materia == m.id)\
            .filter(Inscripcion.alumno == a.id)\
            .filter(Inscripcion.periodo == m.periodo)\
            .all()
            if c:
                return jsonify({
                    'clase':'alert-danger',
                    'mensaje':'Ya te has registrado a '+m.nombre
                })
            else:
                t = Tiempo()
                i = Inscripcion(\
                materia=m.id,\
                alumno=a.id,\
                fecha=t.fecha(),\
                periodo=m.periodo)
                m.cantidad += 1
                q = db.session.add(i)
                db.session.commit()
                return jsonify({
                    "clase":'alert-success',
                    "mensaje": a.nombre+' '+a.apellido+' se ha registrado a '+m.nombre
                    })

        else:
            a = Alumno(\
            nombre=request.form.get('anombre'),\
            apellido=request.form.get('aapellido'),\
            ci=request.form.get('aci'),\
            con=request.form.get('aci'),\
            activo=True)
            db.session.add(a)
            db.session.commit()
            a = Alumno.query.filter_by(ci=request.form.get('aci')).first()
            m = Materia.query.filter_by(codigo=request.form.get('mcodigo')).first()
            t = Tiempo()
            i = Inscripcion(materia=m.id,alumno=a.id, fecha=t.fecha(),periodo=m.periodo)
            m.cantidad += 1
            q = db.session.add(i)
            db.session.commit()
            return jsonify({
                "clase":'alert-success',
                "mensaje": "Bien hecho "+a.nombre+' '+a.apellido+'!!, te has registrado a '+m.nombre
                })

@app.route("/listacompleta/<int:d>", methods=['GET'])
@login_required
def listacompleta(d):
    materia = Materia.query.get(d)
    return render_template("listacompleta.html",materia=materia)


@app.route("/totalista", methods=['POST'])
@login_required
def totalista():
    d = request.form.get('m')
    materia = Materia.query.get(d)
    inscripciones = db.session.query(Inscripcion)\
    .join(Alumno)\
    .filter(Inscripcion.activo==True)\
    .filter(Inscripcion.materia==materia.id)\
    .order_by(Alumno.apellido.asc())\
    .all()
    dias = db.session.query(Diadeclase)\
    .join(Horario, Materia)\
    .filter(Materia.id==materia.id)\
    .order_by(Diadeclase.fecha.asc())\
    .all()
    jdias = []
    cd = 0
    for dia in dias:
        if dia.diasdeclases.activo and dia.activo:
            dm = fecha_dia_mes(dia.fecha)
            dia.fecha_dia_mes = dm
            jdias.append(str(dm))
            if fecha_valida(dia.fecha):
                cd += 1
    jdias = json.dumps(jdias)
    jasistencias = []
    indice = 0
    for i in inscripciones:
        diasdeasistencia = []
        indice += 1
        diasdeasistencia.append(indice)
        diasdeasistencia.append(i.inscripcion_alumnos.ci)
        diasdeasistencia.append(i.inscripcion_alumnos.apellido+", "+i.inscripcion_alumnos.nombre)
        cp = 0
        for dia in dias:
            if dia.diasdeclases.activo and dia.activo:
                detdia = []
                asis = Asistencia.query\
                .filter(Asistencia.alumno==i.alumno)\
                .filter(Asistencia.diadeclase==dia.id)
                for aux in asis:
                    if aux.condicion=='Presente':
                        cp += 1
                if asis.count()==2:
                    if asis[0].tipo=='Entrada':
                        detdia.append(acron(asis[0].condicion))
                        detdia.append(acron(asis[1].condicion))
                    else:
                        detdia.append(acron(asis[1].condicion))
                        detdia.append(acron(asis[0].condicion))
                elif asis.count()==1:
                    if asis[0].tipo=='Entrada':
                        detdia.append(acron(asis[0].condicion))
                        detdia.append('A')
                    else:
                        detdia.append('A')
                        detdia.append(acron(asis[0].condicion))
                else:
                    if fecha_valida(dia.fecha) and asis.count()==0:
                        detdia.append('A')
                        detdia.append('A')
                    else:
                        detdia.append(' ')

                diasdeasistencia.append(detdia)
        diasdeasistencia.append(round(cp*50/cd,0))
        i.diasdeasistencias = diasdeasistencia
        jasistencias.append(diasdeasistencia)
    jasistencias = json.dumps(jasistencias)
    #return render_template("totalista.html",dias=dias,inscripciones=inscripciones,jdias=jdias)
    return jsonify({
    'dias':jdias,
    'asistencias':jasistencias
    })

@app.route("/lista/<int:d>", methods=['GET','POST'])
@login_required
def lista(d):
    s = False
    if d==0:
        d = request.form.get('l')

    diadeclase = Diadeclase.query.get(d)
    diadeclase.hr = fecha_hr(diadeclase.fecha)
    alumnos = db.session.query(Inscripcion)\
    .join(Alumno)\
    .filter(Inscripcion.materia==diadeclase.diasdeclases.horariosmateria.id)\
    .filter(Inscripcion.periodo==diadeclase.diasdeclases.horariosmateria.periodo)\
    .filter(Inscripcion.activo==True)\
    .order_by(Alumno.apellido.asc())\
    .all()
    for a in alumnos:
        asistencia = Asistencia.query\
        .filter(Asistencia.alumno==a.alumno)\
        .filter(Asistencia.diadeclase==diadeclase.id)\
        .filter(Asistencia.tipo=='Entrada')\
        .first()
        if asistencia:
            s = True
            a.estadoentrada = acron(asistencia.condicion)
    t = Tiempo()
    if request.form.get('listanterior'):
        ahora = True
        hora = False
        return render_template('listanterior.html',dc=diadeclase,alumnos=alumnos, ahora=ahora,hora=hora,s=s)

    else:
        ahora = t.esahora(diadeclase.diasdeclases.desde,diadeclase.diasdeclases.hasta,diadeclase.fecha)
        hora = t.hora()
        return render_template('lista.html',dc=diadeclase,alumnos=alumnos, ahora=ahora,hora=hora,s=s)

@app.route("/listar", methods=['POST'])
@login_required
def listar():
    alumno = int(request.form.get('ida'))
    diadeclase = int(request.form.get('idc'))
    condicion = request.form.get('condicion')
    tipo = request.form.get('tipo')
    d = Diadeclase.query.get(diadeclase)
    t = Tiempo()
    if t.esahora(d.diasdeclases.desde,d.diasdeclases.hasta,d.fecha) or current_user.tipo==1 or request.form.get('ad'):
        if (tipo == 'ES'):
            basis = Asistencia.query\
            .filter(and_(Asistencia.alumno==alumno,Asistencia.diadeclase==diadeclase))
            asis = basis.all()
            d = Diadeclase.query.get(diadeclase)
            if basis.count()==0:
                asistencia = Asistencia(diadeclase=diadeclase,alumno=alumno,hora=t.hora(),condicion=condicion,tipo='Entrada')
                db.session.add(asistencia)
                db.session.commit()
                asistencia = Asistencia(diadeclase=diadeclase,alumno=alumno,hora=t.hora(),condicion=condicion,tipo='Salida')
                db.session.add(asistencia)
                db.session.commit()
            elif basis.count()==2:
                asis[0].condicion = condicion
                asis[1].condicion = condicion
                db.session.commit()
            elif basis.count()==1:
                asis[0].tipo = 'Entrada'
                asis[0].condicion = condicion
                db.session.commit()
                asistencia = Asistencia(diadeclase=diadeclase,alumno=alumno,hora=t.hora(),condicion=condicion,tipo='Salida')
                db.session.add(asistencia)
                db.session.commit()
            a = db.session.query(Alumno,Asistencia)\
            .filter(Alumno.id==alumno)\
            .filter(Asistencia.alumno==Alumno.id)\
            .filter(Asistencia.diadeclase==diadeclase)\
            .first()
        else:
            basis = Asistencia.query\
            .filter(and_(Asistencia.alumno==alumno,Asistencia.diadeclase==diadeclase))\
            .filter(Asistencia.tipo==tipo)
            asis = basis.first()
            d = Diadeclase.query.get(diadeclase)
            if basis.count()==0:
                asistencia = Asistencia(diadeclase=diadeclase,alumno=alumno,hora=t.hora(),condicion=condicion,tipo=tipo)
                db.session.add(asistencia)
                db.session.commit()
            else:
                asis.condicion = condicion
                db.session.commit()
            a = db.session.query(Alumno,Asistencia)\
            .filter(Alumno.id==alumno)\
            .filter(Asistencia.alumno==Alumno.id)\
            .filter(Asistencia.diadeclase==diadeclase)\
            .filter(Asistencia.tipo==tipo)\
            .first()
        if tipo=='ES':
            return jsonify({
              "nombre": a[0].apellido+", "+a[0].nombre,
              "condicion": a[1].condicion,
              "tipo": "Entrada y Salida",
              "resultado":"ok"
              })
        else:
            return jsonify({
              "nombre": a[0].apellido+", "+a[0].nombre,
              "condicion": a[1].condicion,
              "tipo": a[1].tipo,
              "resultado":"ok"
              })
    else:
        return jsonify({
            "mensaje":"Las clases de "+d.diasdeclases.horariosmateria.nombre+" de los "+d.diasdeclases.dia+" son de "+d.diasdeclases.desde+" a "+d.diasdeclases.hasta+" horas.",
            "resultado":"error"
        })

@app.route("/adminInscripcion", methods=['POST'])
@login_required
def adminInscripcion():
    i = Inscripcion.query.get(request.form.get('i'))
    if request.form.get('des'):
        i.activo = False
        clase = 'danger'
        mensaje = 'Se ha excluido a '+i.inscripcion_alumnos.nombre+' '+i.inscripcion_alumnos.apellido+' de la lista'
    if request.form.get('hab'):
        i.activo = True
        clase = 'success'
        mensaje = 'Se ha incluido a '+i.inscripcion_alumnos.nombre+' '+i.inscripcion_alumnos.apellido+' de la lista'
    db.session.commit()
    return jsonify({
    'clase':clase,
    'mensaje':mensaje
    })

"""
@app.route("/detalumno/<int:d>", methods=['GET'])
@login_required
def detalumno(a):
"""


## CLASES Y FUNCIONES
def acron(a):
    if (a=='Presente'):
        v = 'P'
    elif (a=='Ausente'):
        v = 'A'
    elif (a=='Justificado - Trabajo'):
        v = 'JT'
    elif (a=='Justificado - Salud'):
        v = 'JS'
    elif (a=='Justificado - Otro'):
        v = 'JO'
    return v

def codigo():
    b = True
    while(b):
        c = ''.join(random.sample((string.ascii_uppercase+string.digits),4))
        m = Materia.query.filter_by(codigo=c).count()
        if m == 0:
            b = False
    return c

def dias_clases(c,h,dia_clase,fi,ff):
    sgt = datetime.strptime(fi,"%Y-%m-%d")
    fin = datetime.strptime(ff,"%Y-%m-%d")
    dia = ("Lunes", "Martes","Miercoles","Jueves","Viernes","Sabado","Domingo")
    if c == 'alta':
        b = True
        while b:
            if dia[sgt.isoweekday() - 1] == dia_clase:
                fecha_clase = sgt
                b = False
            sgt = sgt + timedelta(days=1)
        while fecha_clase <= fin:
            d = Diadeclase(horario=h,fecha=fecha_clase)
            db.session.add(d)
            db.session.commit()
            fecha_clase = fecha_clase + timedelta(days=7)
    else:
        t = Tiempo()
        d = Diadeclase.query.filter_by(horario=h)
        dias_mod = []
        for dc in d:
            fecha_lista = datetime.strptime(dc.fecha,"%Y-%m-%d %H:%M:%S")
            if fecha_lista >= t.s_fecha():
                db.session.delete(dc)
                db.session.commit()
        sgt = t.s_fecha()
        b = True
        while b:
            if dia[sgt.isoweekday() - 1] == dia_clase:
                fecha_clase = sgt
                b = False
            sgt = sgt + timedelta(days=1)
        while fecha_clase <= fin:
            d = Diadeclase(horario=h,fecha=fecha_clase)
            db.session.add(d)
            db.session.commit()
            fecha_clase = fecha_clase + timedelta(days=7)
    return True

def fecha_dia_mes(fecha):
    f = datetime.strptime(fecha,"%Y-%m-%d %H:%M:%S")
    dia = f.day
    mes = f.month
    resultado = "{}/{}".format(dia, mes)
    return resultado

def fecha_hr(fecha):
    f = datetime.strptime(fecha,"%Y-%m-%d %H:%M:%S")
    meses = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    dias = ("Lunes", "Martes","Miercoles","Jueves","Viernes","Sabado","Domingo")
    numero_dia = f.day
    mes = meses[f.month - 1]
    dia = dias[f.isoweekday() - 1]
    anho = f.year
    resultado = "{}, {} de {} del {}".format(dia, numero_dia, mes, anho)
    return resultado

def fecha_valida(fecha):
    t = Tiempo()
    f = datetime.strptime(fecha,"%Y-%m-%d %H:%M:%S")
    if f <= t.fecha_com():
        return True
    else:
        return False
def fecha_simple(fecha):
    f = datetime.strptime(fecha,"%Y-%m-%d %H:%M:%S")
    numero_dia = f.day
    mes = f.month
    anho = f.year
    resultado = "{} - {} - {}".format(numero_dia, mes, anho)
    return resultado

def calculardias(m):
    d = db.session.query(Diadeclase)\
    .join(Horario, Materia)\
    .filter(Diadeclase.activo==True)\
    .filter(Materia.id==m)\
    .filter(Materia.activo==True)\
    .filter(Horario.activo==True)\
    .all()
    t = Tiempo()
    b = 0
    for dia in d:
        clase = datetime.strptime(dia.fecha,"%Y-%m-%d %H:%M:%S")
        h = datetime.strptime(dia.diasdeclases.desde, "%H:%M")
        clase = clase + timedelta(hours=h.hour)
        if clase < t.fecha_com():
            b = b+1
    return b

def calcularasistencia(a,tc,m):
    alumno = db.session.query(Asistencia)\
    .join(Diadeclase, Horario, Materia, Alumno)\
    .filter(Diadeclase.activo==True)\
    .filter(Horario.activo==True)\
    .filter(Materia.id==m)\
    .filter(Alumno.id==a)\
    .filter(Asistencia.condicion=='Presente')\
    .count()
    resultado = round((alumno*50)/tc,2)
    return resultado


class Grafico():
    def __init__(self,d,h,p):
        self.desde = d
        self.hasta = h
        self.p = p

    def lx(self):
        l = []
        d = self.desde
        h = self.hasta
        while(d<=h):
            if(d.isoweekday()<6):
                l.append(fecha_dia_mes(str(d)))
            d = d + timedelta(days=1)
        return l
    def lym(self,m):
        valores = []
        dt = self.desde
        ht = self.hasta
        while(dt<=ht):
            if(dt.isoweekday()<6):
                vd = db.session.query(Asistencia)\
                .join(Diadeclase, Horario, Materia)\
                .filter(Diadeclase.fecha==str(dt))\
                .filter(Asistencia.condicion=='Presente')\
                .filter(Materia.id==m)\
                .count()
                if self.p:
                    ins = db.session.query(Inscripcion)\
                    .join(Materia, Horario, Diadeclase)\
                    .filter(Diadeclase.fecha==str(dt))\
                    .filter(Materia.id==m)\
                    .count()
                    if ins>0 and vd>0:
                        r = round(vd*50/ins,2)
                        valores.append(r)
                    else:
                        valores.append(None)
                else:
                    if vd>0:
                        valores.append(vd)
                    else:
                        valores.append(None)
            dt = dt + timedelta(days=1)
        return valores

    def ly(self,valor,valor2):
        valores = []
        dt = self.desde
        ht = self.hasta
        if valor=='g':
            while(dt<=ht):
                if(dt.isoweekday()<6):
                    vd = db.session.query(Asistencia)\
                    .join(Diadeclase)\
                    .filter(Diadeclase.fecha==str(dt))\
                    .filter(Asistencia.condicion=='Presente')\
                    .count()
                    if self.p:
                        ins = db.session.query(Inscripcion)\
                        .join(Materia, Horario, Diadeclase)\
                        .filter(Diadeclase.fecha==str(dt))\
                        .count()
                        if ins>0:
                            r = round(vd*50/ins,2)
                            valores.append(r)
                        else:
                            valores.append(0)
                    else:
                        valores.append(vd)
                dt = dt + timedelta(days=1)
            return valores

        else:
            if valor!=False and valor>0:
                if valor2!=False and valor2>0:
                    while(dt<=ht):
                        if(dt.isoweekday()<6):
                            vd = db.session.query(Asistencia)\
                            .join(Diadeclase, Horario, Materia)\
                            .filter(Diadeclase.fecha==str(dt))\
                            .filter(Asistencia.condicion=='Presente')\
                            .filter(Materia.carrera==valor)\
                            .filter(Materia.curso==valor2)\
                            .count()
                            if self.p:
                                ins = db.session.query(Inscripcion)\
                                .join(Materia, Horario, Diadeclase)\
                                .filter(Diadeclase.fecha==str(dt))\
                                .filter(Materia.carrera==valor)\
                                .filter(Materia.curso==valor2)\
                                .count()
                                if ins>0:
                                    r = round(vd*50/ins,2)
                                    valores.append(r)
                                else:
                                    valores.append(0)
                            else:
                                valores.append(vd)
                        dt = dt + timedelta(days=1)
                    return valores
                else:
                    while(dt<=ht):
                        if(dt.isoweekday()<6):
                            vd = db.session.query(Asistencia)\
                            .join(Diadeclase, Horario, Materia, Carrera)\
                            .filter(Diadeclase.fecha==str(dt))\
                            .filter(Asistencia.condicion=='Presente')\
                            .filter(Materia.carrera==valor)\
                            .count()
                            if self.p:
                                ins = db.session.query(Inscripcion)\
                                .join(Materia, Horario, Diadeclase)\
                                .filter(Diadeclase.fecha==str(dt))\
                                .filter(Materia.carrera==valor)\
                                .count()
                                if ins>0:
                                    r = round(vd*50/ins,2)
                                    valores.append(r)
                                else:
                                    valores.append(0)
                            else:
                                valores.append(vd)
                        dt = dt + timedelta(days=1)
                    return valores
            else:
                while(dt<=ht):
                    if(dt.isoweekday()<6):
                        vd = db.session.query(Asistencia)\
                        .join(Diadeclase, Horario, Materia)\
                        .filter(Diadeclase.fecha==str(dt))\
                        .filter(Asistencia.condicion=='Presente')\
                        .filter(Materia.curso==valor2)\
                        .count()
                        if self.p:
                            ins = db.session.query(Inscripcion)\
                            .join(Materia, Horario, Diadeclase)\
                            .filter(Diadeclase.fecha==str(dt))\
                            .filter(Materia.curso==valor2)\
                            .count()
                            if ins>0:
                                r = round(vd*50/ins,2)
                                valores.append(r)
                            else:
                                valores.append(0)
                        else:
                            valores.append(vd)
                    dt = dt + timedelta(days=1)
                return valores

class Tiempo():
    def __init__(self):
        fecha_sistema = datetime.now()
        retraso = timedelta(hours=4)
        self.date = fecha_sistema - retraso
    def paso10min(self,h):
        ha = datetime.strptime(h, "%H:%M")
        ahora = datetime.strptime(self.hora(), "%H:%M")

        if ahora - ha > timedelta(seconds=60):
            return True
        else:
            return False

    def hora(self):
        h = "{}:{}".format(self.date.hour, self.date.minute)
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
    def fecha_com(self):
        return self.date

    def s_fecha(self):
        sf = self.date
        sf = sf.replace(hour=0, minute=0, second=0, microsecond=0)
        return sf

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
    def esahora(self,d,h,f):
        desde = datetime.strptime(d, "%H:%M")
        hasta = datetime.strptime(h, "%H:%M")
        ahora = datetime.strptime(self.hora(), "%H:%M")
        fecha = datetime.strptime(f,"%Y-%m-%d %H:%M:%S")
        if ahora < hasta and ahora > desde and fecha == self.s_fecha():
            return True
        else:
            return False

"""ESTOS SON LOS MODELOS"""

app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

class TipoUsuario(db.Model):
    __tablename__ = "tipo_usuario"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(60), nullable=False)
    tipos = db.relationship('Usuario', backref='tipos', lazy=True)

class Curso(db.Model):
    __tablename__ = "cursos"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(60), nullable=False)
    materias = db.relationship('Materia', backref='cursomateria', lazy=True)

class Materia(db.Model):
    __tablename__ = "materias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    codigo = db.Column(db.String(20),nullable=False)
    seccion = db.Column(db.String(10),nullable=False)
    cantidad = db.Column(db.Integer, default=0, nullable=False)
    curso = db.Column(db.Integer, db.ForeignKey("cursos.id"))
    carrera = db.Column(db.Integer, db.ForeignKey("carreras.id"))
    docente = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    activo  = db.Column(db.Boolean(), default=True, nullable=False)
    periodo = db.Column(db.Integer, db.ForeignKey("periodos.id"))
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

class Periodo(db.Model):
    __tablename__ = "periodos"
    id = db.Column(db.Integer, primary_key=True)
    nombre_periodo = db.Column(db.String(100), nullable=False)
    inicio = db.Column(db.String(20), nullable=False)
    fin = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)
    inscripcionesperiodo = db.relationship('Inscripcion', backref='inscripcionesperiodo', lazy=True)
    matierasperiodo = db.relationship('Materia', backref='materiasperiodo', lazy=True)

class Carrera(db.Model):
    __tablename__ = "carreras"
    id = db.Column(db.Integer, primary_key=True)
    nombre_carrera = db.Column(db.String(30), nullable=False)
    materias = db.relationship('Materia', backref='carreras', lazy=True)
    responsable = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    activo = db.Column(db.Boolean(), default=True, nullable=False)

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(80))
    avatar = db.Column(db.String(200))
    tokens = db.Column(db.Text)
    ci = db.Column(db.Integer, default=0,nullable=False)
    email = db.Column(db.String(128), nullable=False)
    telefono = db.Column(db.String(15), default='****', nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)
    con = db.Column(db.String(200), default='****', nullable=False)
    tipo = db.Column(db.Integer, db.ForeignKey("tipo_usuario.id"), nullable=False)
    responsables = db.relationship('Carrera', backref='responsables', lazy=True)
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
    periodo = db.Column(db.Integer, db.ForeignKey("periodos.id"), nullable=False)
    activo = db.Column(db.Boolean(), default=True, nullable=False)

class Diadeclase(db.Model):
    __tablename__ = "diasdeclases"
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.Integer, db.ForeignKey("horarios.id"), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)
    llamados = db.Column(db.Integer, default=0,nullable=False)
    asistentes = db.Column(db.Float(), default=0,nullable=False)
    activo = db.Column(db.Boolean(), default=True)
    diasasistencias = db.relationship('Asistencia', backref='diasasistencias', lazy=True)

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
    activo = db.Column(db.Boolean(), default=True, nullable=False)
    con = db.Column(db.String(200), nullable=False)
    inscriptos = db.relationship('Inscripcion', backref='inscripcion_alumnos', lazy=True)
    asistencias = db.relationship('Asistencia', backref='asistencias', lazy=True)


def consultarAsistencia(m):
    m = Materia.query.get(m)
    h = Horario.query.filter(Horario.materia==m.id).all()

    for ho in h:
        dia = Diadeclase.query.filter(Diadeclase.horario==ho.id).all()

        for d in dia:
            asis = Asistencia.query.filter(Asistencia.diadeclase==d.id).all()
            if asis:
                for a in asis:
                    i = Inscripcion.query.filter(Inscripcion.alumno==a.alumno).filter(Inscripcion.materia==m.id)
                    if i.count()==1:
                        i = i.first()
                        print(m.nombre+","+i.fecha+","+d.fecha+","+a.asistencias.apellido+","+a.asistencias.nombre+","+","+a.tipo+","+a.condicion)
                    else:
                        print("Inscripcion doblee")

def eliminarAsistencia(m):
    m = Materia.query.get(m)
    h = Horario.query.filter(Horario.materia==m.id).all()

    for ho in h:
        dia = Diadeclase.query.filter(Diadeclase.horario==ho.id).all()
        for d in dia:
            asis = Asistencia.query.filter(Asistencia.diadeclase==d.id).all()
            if asis:
                for a in asis:
                    db.session.delete(a)
                    db.session.commit()

def consultarDias(m):
    m = Materia.query.get(m)
    h = Horario.query.filter(Horario.materia==m.id).all()

    for ho in h:
        dia = Diadeclase.query.filter(Diadeclase.horario==ho.id).all()
        if dia:
            for d in dia:
                print(m.nombre+","+d.fecha)

def eliminarDias(m):
    m = Materia.query.get(m)
    h = Horario.query.filter(Horario.materia==m.id).all()

    for ho in h:
        dia = Diadeclase.query.filter(Diadeclase.horario==ho.id).all()
        if dia:
            for d in dia:
                db.session.delete(d)
                db.session.commit()
