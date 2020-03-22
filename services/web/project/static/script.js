
document.addEventListener('DOMContentLoaded', function() {
  perfil();

});
// CLASES
class FormP {
  constructor (nombre_grupo) {
    this.nombre_grupo = nombre_grupo;
    this.bandera = true;
    this.btn = false;
    this.data = new FormData();
  }
  // Método
  formV () {
    var bandera = true;
     var opt = document.querySelectorAll(this.nombre_grupo);
     for (var i = 0; i < opt.length; i++) {
       if (opt[i].type == 'text' || opt[i].type == 'number' || opt[i].type == 'email' || opt[i].type == 'password' || opt[i].type == 'date') {
         if (opt[i].value == ""){
           this.bandera = false;
         } else {
           this.data.append(opt[i].id,opt[i].value);
         }
       } else if (opt[i].type == 'select-one'){
         let e = opt[i]
         if (e.selectedIndex == 0){
           this.bandera = false;
         } else {
           this.data.append(e.id, e.options[e.selectedIndex].value);
         }
       } else if (opt[i].type == 'button') {
         this.btn = opt[i];
       }
     }
   }
};
var vaciarform = function (nf) {
  var opt = document.querySelectorAll(nf);
  for (var i = 0; i < opt.length; i++) {
    if (opt[i].type == 'text' || opt[i].type == 'number' || opt[i].type == 'email' || opt[i].type == 'password' || opt[i].type == 'date') {
      opt[i].value = "";
    } else if (opt[i].type == 'select-one') {
      opt[i].firstElementChild.selected = true;
    }
  }
}
var cargadevistasimple = function(u,d,data,cancelar) {
  const request = new XMLHttpRequest();
  request.open('POST',u);
  request.onload = () => {
      document.getElementById(d).innerHTML = request.response;
      if (cancelar == 'p') {
        pcancelar();
      } else if ( cancelar == 'u') {
        ucancelar();
      } else if ( cancelar == 'c') {
        ccancelar();
      }
  };
  if ( data == false ) {
    request.send();
  } else {
    request.send(data);
  }
  return false;
};

var formV = function (nf) {
  var bandera = true;
   var data = new FormData();
   var opt = document.querySelectorAll(nf);
   for (var i = 0; i < opt.length; i++) {
     if (opt[i].type == 'text' || opt[i].type == 'number' || opt[i].type == 'email' || opt[i].type == 'password' || opt[i].type == 'date') {
       if (opt[i].value == ""){
         bandera = false;
       } else {
         data.append(opt[i].id,opt[i].value);
       }
     } else if (opt[i].type == 'select-one'){
       let e = opt[i]
       if (e.selectedIndex == 0){
         bandera = false;
       } else {
         data.append(e.id, e.options[e.selectedIndex].value);
       }
     } else {
       console.log(opt[i].id);
     }
   }
   if (bandera != false) {
     return data;
   } else {
     return false;
   }
 }

// Elementos cargados por el NAVBAR, perfil, materias, periodos
var perfil = function() { cargadevistasimple('/perfil','body',false);};
var misclases = function () { cargadevistasimple('/misclases','body',false);};
var usuario = function () { cargadevistasimple('/usuario','body',false);};
var consultas = function () { cargadevistasimple('/consultas','body',false);};
var administracion = function() {
  const request = new XMLHttpRequest();
  request.open('POST','/administracion');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
      cargadevistasimple('/listaperiodos','lista-periodos',false);
      cargadevistasimple('/listausuarios','lista-usuarios',false);
      cargadevistasimple('/listacarreras','lista-carreras',false);
  };
  request.send();
  return false;
};
var materias = function() {
  const request = new XMLHttpRequest();
  request.open('POST','/materias');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
      cargadevistasimple('/listamaterias','lista-materias',false);
  };
  request.send();
  return false;
};


function init() {
  gapi.load('auth2', function() {
    gapi.auth2.init();
    /* Ready. Make a call to gapi.auth2.init or some other API */
  });

}
var salir = function() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.grantOfflineAccess();
    auth2.signOut().then(function () {
      auth2.disconnect();
    });
  const request = new XMLHttpRequest();
  request.open('POST','/salir',false);
    request.onload = () => {
      location.reload();
    };
  request.send();
};

//FIN Elementos cargados por el NAVBAR, perfil, materias, periodos

// UTILITARIOS
var cantidad_alumnos = function(m) {
  const request = new XMLHttpRequest();
  request.open('POST', '/alumnos');
  const data = new FormData();
  data.append('m',m);
  data.append('rca',true);
  request.open('POST', '/alumnos');
  request.onload = () => {
  ca = document.querySelectorAll('.cant_a'+m);
  for (var i = 0; i < ca.length; i++) {
    ca[i].innerHTML = request.response;;
  }
  };
  request.send(data);
  return false;
};
var editarinfo = function() {
  info = document.querySelectorAll('.form-info');
  for (i=0 ; i < info.length ; i++ ){
    info[i].disabled = false;
  }
  b = document.getElementById('btneditarinfo');
  b.innerHTML = "<span class='glyphicon glyphicon-save' aria-hidden='true'></span> Guardar Información";
  b.removeAttribute("onclick");
  b.setAttribute("onclick",'guardarinfo()');
}
var guardarinfo = function() {
  p = new FormP('.form-info');
  p.formV();
  if (p.bandera) {
    data = p.data;
    data.append('mod',true);
    cargadevistasimple('/usuario','body',data,false);
  } else {
    start('danger','Por favor complete todos los campos');
  }
}
// FIN UTILITARIOS
// INICIO DE ALTA DE DOCENTES
var dcon = function () {
  f = formV('.form-docente');
  if (f != false){
    const request = new XMLHttpRequest();
    request.open('POST', '/docentes');
    data = f;
    data.append('altadocente',true);
    request.onload = () => {
      const respuesta = JSON.parse(request.responseText);
      start('success',`Bien hecho ${respuesta.nombre}, tus datos fueron registrados exitoxamente`);
    };
    request.send(data);
    return false;
  } else {
    start('danger','Por favor complete todos los campos');
  }
};
var verificard = function (v) {
  const data = new FormData();
  data.append('dci',v);
  data.append('verificard',true);
  const request = new XMLHttpRequest();
  request.open('POST', '/docentes');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    if(respuesta.estado == 'ya') {
      start('danger',`Ya te has resistrado previamente ${respuesta.nombre}`);
      document.getElementById('btndocente').disabled = true;
    } else {
      document.getElementById('btndocente').disabled = false;
    }
  };
  request.send(data);

  return false;
}
//FIN DE ALTA DE DOCENTES

// INICIO DE ADMINISTRACION DE USUARIOS
var ausuario = function (id) {
  p = new FormP('.form-usuario');
  p.formV();
  if (p.bandera) {
    data = p.data;
    if (id != null){
      data.append('uid',id);
      data.append('mod',true);
      cargadevistasimple('/listausuarios','lista-usuarios',data,'u');
    } else {

      data.append('alta',true);
      cargadevistasimple('/listausuarios','lista-usuarios',data,false);
    }

  } else {
    start('danger','Por favor complete todos los campos');
  }
};
var ueliminar = function (uid) {
  const data = new FormData();
  data.append('uid',uid);
  data.append('baja',true);
  cargadevistasimple('/listausuarios','lista-usuarios',data);
};
var umodificar = function (uid) {
  const data = new FormData();
  data.append('uid',uid);
  data.append('modificacion',true);
  const request = new XMLHttpRequest();
  request.open('POST', '/listausuarios');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    document.getElementById('unombre').value = respuesta.nombre;
    document.getElementById('uapellido').value = respuesta.apellido;
    document.getElementById('uci').value = respuesta.ci;
    document.getElementById('uemail').value = respuesta.email;
    document.getElementById('utelefono').value = respuesta.telefono;
    document.getElementById(`usuario${respuesta.tipo}`).selected = true;
    b = document.getElementById('btnusuario');
    b.innerHTML = "<span class='glyphicon glyphicon-save' aria-hidden='true'></span> Guardar modificacion";
    b.removeAttribute("onclick");
    b.setAttribute("onclick",`ausuario(${respuesta.id})`);
  };
  request.send(data);

  return false;
};
var ucancelar = function () {
  vaciarform('.form-usuario');
  btn = document.getElementById('btnusuario');
  btn.removeAttribute("onclick");
  btn.setAttribute("onclick","ausuario()");
  btn.innerHTML = '<span class="glyphicon glyphicon-save" aria-hidden="true"></span> Guardar Usuario Nuevo';
};
// FIN DE ADMINISTRACION DE USUARIOS

// INICIO ADMINISTRACION DE CARRERAS
var calta = function (id) {
  p = new FormP('.form-carrera');
  p.formV();
  if (p.bandera) {
    data = p.data;
    if (id != null){
      data.append('cid',id);
      data.append('mod',true);
      cargadevistasimple('/listacarreras','lista-carreras',data,'c');
    } else {

      data.append('alta',true);
      cargadevistasimple('/listacarreras','lista-carreras',data,false);
    }

  } else {
    start('danger','Por favor complete todos los campos');
  }
};
var celiminar = function (uid) {
  const data = new FormData();
  data.append('cid',uid);
  data.append('baja',true);
  cargadevistasimple('/listacarreras','lista-carreras',data);
};
var cmodificar = function (uid) {
  const data = new FormData();
  data.append('cid',uid);
  data.append('modificacion',true);
  const request = new XMLHttpRequest();
  request.open('POST', '/listacarreras');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    document.getElementById('cnombre').value = respuesta.nombre;
    if (respuesta.coordinador != 0){
    document.getElementById(`coord${respuesta.coordinador}`).selected = true;
    }
    b = document.getElementById('btncarrera');
    b.innerHTML = "<span class='glyphicon glyphicon-save' aria-hidden='true'></span> Guardar modificacion";
    b.removeAttribute("onclick");
    b.setAttribute("onclick",`calta(${respuesta.id})`);
  };
  request.send(data);

  return false;
};
var ccancelar = function () {
  vaciarform('.form-carrera');
  btn = document.getElementById('btncarrera');
  btn.removeAttribute("onclick");
  btn.setAttribute("onclick","calta()");
  btn.innerHTML = '<span class="glyphicon glyphicon-save" aria-hidden="true"></span> Guardar Carrera Nueva';
};
// FIN DE ADMINISTRACION DE CARRERAS

// INICIO DE ADMINISTRACION DE PERIODOS
var addPeriodo = function (id) {
  p = new FormP('.form-periodo');
  p.formV();
  if (p.bandera) {
    data = p.data;
    if (id != null){
      data.append('pid',id);
      data.append('mod',true);
      cargadevistasimple('/listaperiodos','lista-periodos',data,'p');
    } else {

      data.append('alta',true);
      cargadevistasimple('/listaperiodos','lista-periodos',data,false);
    }

  } else {
    start('danger','Por favor complete todos los campos');
  }
};
var peliminar = function (pid) {
  const data = new FormData();
  data.append('admin-periodos',true);
  data.append('pid',pid);
  data.append('baja',true);
  cargadevistasimple('/listaperiodos','lista-periodos',data);
};
var pmodificar = function (pid) {
  const data = new FormData();
  data.append('admin-periodos',true);
  data.append('pid',pid);
  data.append('modificacion',true);
  const request = new XMLHttpRequest();
  request.open('POST', '/listaperiodos');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    document.getElementById('pnombre').value = respuesta.nombre;
    document.getElementById('pfechad').value = respuesta.inicio;
    document.getElementById('pfechah').value = respuesta.fin;
    b = document.getElementById('btnPeriodo');
    b.innerHTML = "<span class='glyphicon glyphicon-save' aria-hidden='true'></span> Guardar modificacion";
    b.removeAttribute("onclick");
    b.setAttribute("onclick",`addPeriodo(${respuesta.id})`);
  };
  request.send(data);

  return false;
};
var pcancelar = function () {
  vaciarform('.form-periodo');
  btn = document.getElementById('btnPeriodo');
  btn.removeAttribute("onclick");
  btn.setAttribute("onclick","addPeriodo()");
  btn.innerHTML = '<span class="glyphicon glyphicon-save" aria-hidden="true"></span> Guardar Periodo Nuevo';
};

// FIN DE ADMINISTRACION DE PERIODOS
// INICIO DE ADMINISTRACION DE MATERIAS
var malta = function(id) {
    m = formV('.form-materia');
    if ( m != false ) {
      data = m;
      const request = new XMLHttpRequest();
      if (id == null){
        data.append('alta',true);
      } else {
        data.append('modificar',true);
        data.append('mid',id);
      }
      request.open('POST', '/listamaterias');
      request.onload = () => {
        if (id != null){
          mcancelar();
        }
        mcancelar();
        document.getElementById('lista-materias').innerHTML = request.response;
      };
      request.send(data);
      return false;
    } else {
      start('danger','Por favor complete todos los campos');
    }

};
var meliminar = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('baja', true);
  data.append('mid',id);
  request.open('POST', '/listamaterias');

  request.onload = () => {
    document.getElementById('lista-materias').innerHTML = request.response;
  };
  request.send(data);

  return false;

};
var mmodificar = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('mod', true);
  data.append('mid',id);
  request.open('POST', '/listamaterias');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    document.getElementById('mnombre').value = respuesta.nombre;
    document.getElementById(`curso${respuesta.curso}`).selected = true;
    document.getElementById(`${respuesta.seccion}`).selected = true;
    document.getElementById(`carrera${respuesta.carrera}`).selected = true;
    if (respuesta.docente != 0){
      document.getElementById(`docente${respuesta.docente}`).selected = true;
    }
    if (respuesta.periodo != 0){
      document.getElementById(`periodo${respuesta.periodo}`).selected = true;
    }
    b = document.getElementById('btnmateria');
    b.innerHTML = "<span class='glyphicon glyphicon-save' aria-hidden='true'></span> Guardar modificacion";
    b.removeAttribute("onclick");
    b.setAttribute("onclick",`malta(${respuesta.id})`);
  };
  request.send(data);

  return false;
};
var mcancelar = function () {
  vaciarform('.form-materia');
  b = document.getElementById('btnmateria');
  b.innerHTML = "<span class='glyphicon glyphicon-save' aria-hidden='true'></span> Guardar Materia Nueva";
  b.removeAttribute("onclick");
  b.setAttribute("onclick","malta()");
};
// INICIO DE ADMINISTRACION DE PERIODOS
var minfo = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('minfo', true);
  data.append('mid',id);
  request.open('POST', '/detallemateria');

  request.onload = () => {
    document.getElementById('mensaje').innerHTML = request.response;
    $('#minfoModal').modal('show');
  };
  request.send(data);

  return false;

};
// FIN DE ADMINISTRACION DE MATERIAS
// INICIO DE ADMINISTRACION DE HORARIOS
var addHorario = function(mhid) {
  p = new FormP('.form-horario');
  p.formV();
  if (p.bandera) {
    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('mid',mhid);
    e = document.getElementById('hdia');
    data.append('hdia', e.options[e.selectedIndex].value);
    data.append('hhorad', document.getElementById('hhorad').value);
    data.append('hhorah', document.getElementById('hhorah').value);
    data.append('hsala', document.getElementById('hsala').value);
    data.append('halta',true);
    request.open('POST', '/detallemateria');
    request.onload = () => {
      document.getElementById('mhorario').innerHTML = request.response;
    };
    request.send(data);

    return false;
  } else {
    start('danger','Por favor complete todos los campos');
  }
};
var heliminar = function(hid , mid) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('hbaja', true);
  data.append('hid',hid);
  data.append('mid',mid);
  request.open('POST', '/detallemateria');

  request.onload = () => {
    document.getElementById('mhorario').innerHTML = request.response;
  };
  request.send(data);

  return false;

};
var modHorario = function(hid) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('hid',hid);
  data.append('mid',document.getElementById('btnhorario').dataset.id);
  e = document.getElementById('hdia');
  data.append('hdia',e.options[e.selectedIndex].value);
  data.append('hhorad', document.getElementById('hhorad').value);
  data.append('hhorah', document.getElementById('hhorah').value);
  data.append('hsala', document.getElementById('hsala').value);
  data.append('modHorario',true);
  request.open('POST', '/detallemateria');
  request.onload = () => {
    document.getElementById('mhorario').innerHTML = request.response;
    hcancelar();
  };
  request.send(data);

  return false;
};
var hmodificar = function(hid, mid) {

  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('hmodificacion', true);
  data.append('hid',hid);
  data.append('mid',mid);
  request.open('POST', '/detallemateria');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    document.getElementById('hhorad').value = respuesta.desde;
    document.getElementById('hhorah').value = respuesta.hasta;
    document.getElementById('hsala').value = respuesta.sala;
    document.getElementById(`${respuesta.dia}`).selected = true;


    btn = document.getElementById('btnhorario');
    btn.innerHTML = '<span class="glyphicon glyphicon-save" aria-hidden="true"></span> Modificar Horario';
    btn.removeAttribute('onclick');
    btn.setAttribute('onclick',`modHorario(${respuesta.id})`);
  };
  request.send(data);

  return false;
};
var hcancelar = function (idm) {
  o = document.querySelectorAll('option');
  for (var i = 0; i < o.length; i++) {
    o[i].removeAttribute("selected");
  }
  document.getElementById('hhorad').value = "";
  document.getElementById('hhorah').value = "";
  document.getElementById('hsala').value = "";
  document.getElementById('hdia').firstElementChild.selected = true;

  b = document.getElementById('btnhorario');
  b.innerHTML = "<span class='glyphicon glyphicon-save' aria-hidden='true'></span> Guardar Horario Nueva";
  b.removeAttribute("onclick");
  b.setAttribute("onclick","malta("+b.dataset.id+")");
};

// FIN DE ADMINISTRACION DE HORARIOS
// INICIO DE VISTA PARA REGISTRO DE USUARIOS
var registroAlumnos = function (cm) {
  document.getElementById('anombre').disabled = true;
  document.getElementById('aapellido').disabled = true;
  document.getElementById('infoproceso').style.display = 'none'
  document.getElementById('mcodigo').value = cm;
  document.getElementById('mcodigo').disabled = true;
  verificarm();
  $('#regAlumno').modal('show');
};

var acon = function () {
  p = new FormP('.form-alumno');
  p.formV();
  document.getElementById('aapellido').value = '';
  document.getElementById('anombre').value = '';
  if (p.bandera) {
    const request = new XMLHttpRequest();
    data = p.data;
    data.append('alta_alumno',true)
    request.open('POST', '/alumnos');
    request.onload = () => {
      const respuesta = JSON.parse(request.responseText);
      e = document.getElementById('infoproceso');
      e.className = '';
      e.classList.add('alert');
      e.classList.add(respuesta.clase);
      e.innerHTML = respuesta.mensaje;
      document.getElementById('infoproceso').style.display = 'inline-block'
    };
    document.getElementById('anombre').value = '';
    document.getElementById('aapellido').value = '';
    request.send(data);
    return false;
  } else {
    start('danger','Por favor complete todos los campos');
  }
};

var verificarm = function () {
  v = document.getElementById('mcodigo').value;
  if (v != '' ) {
    const request = new XMLHttpRequest();
    const data1 = new FormData()
    data1.append('v',v);
    data1.append('verificarMateria',true);
    request.open('POST', '/alumnos');
    request.onload = () => {
      const data = JSON.parse(request.responseText);
      if (data.mensaje == "Ok") {
        const materiaInfo = `<p class="label label-info label-inline">Materia: ${data.Materia}</p>
                                  <p class="label label-info label-inline">Curso: ${data.Curso}, sección: ${data.Seccion}</p>
                                  <p class="label label-info label-inline">Periodo: ${data.Periodo}</p>
                                  <p class="label label-info label-inline">Carrera: ${data.Carrera}</p>
                                  <p class="label label-info label-inline">Docente: ${data.Docente}</p>`;
              document.getElementById('infomateria').innerHTML = materiaInfo;
              document.getElementById('btnAltaAlumno').disabled = false;
        }else{
            document.getElementById('infomateria').innerHTML = '<p class="label label-danger label-inline">'+data.mensaje+'</p>';
            document.getElementById('btnAltaAlumno').disabled = true;
        }
    };
    request.send(data1);

    return false;
  }
};

var verificara = function () {
  v = document.getElementById('aci').value;
  if (v != '' ) {
    const request = new XMLHttpRequest();
    const data1 = new FormData()
    data1.append('v',v);
    data1.append('verificarAlumno',true);
    request.open('POST', '/alumnos');
    request.onload = () => {
      const data = JSON.parse(request.responseText);
      if (data.registro == "listo") {
        document.getElementById('anombre').value = data.nombre;
        document.getElementById('anombre').disabled = true;
        document.getElementById('aapellido').value = data.apellido;
        document.getElementById('aapellido').disabled = true;
        }else{
            document.getElementById('infoalumno').innerHTML = '<span class="label label-warning label-inline">Por favor completa los siguientes campos</span>';
            fa = document.querySelectorAll('.form-alumno');
            for (var i = 0; i < fa.length; i++) {
              fa[i].disabled = false;
            }
        }
    };
    request.send(data1);

    return false;
  }
};


// FIN DE VISTA DE REGISTRO DE USUArIOS

// INICIO VISTAS DE DIAS DE CLASES
var bfecha = function() {
  f = document.getElementById('bfecha').value
  if (f == ''){
    start('danger','Espesifíque alguna fecha');
  } else {
    data = new FormData();
    data.append('fecha',f);
    cargadevistasimple('/listaclases','lista-clases',data,false);
  }
};

var bcodigo = function() {
  c = document.getElementById('bcodigo').value;
  if (c == ''){
    start('danger','Ingrese algún código de materia');
  } else {
    data = new FormData();
    data.append('codigo',c);
    cargadevistasimple('/listaclases','lista-clases',data,false);
  }
};

var desdia = function(d) {
  data = new FormData();
  c = document.getElementById('bcodigo').value;
  if (c == ''){
    c = document.getElementById('bfecha').value;
    if (c == ''){
      start('danger','Especifique una fecha on un código');
    } else {
      data.append('fecha',c);
    }
  } else {
    data.append('codigo',c);
  }
  data.append('des',true);
  data.append('dia',d);
  cargadevistasimple('/listaclases','lista-clases',data,false);
};

var habdia = function(d) {
  data = new FormData();
  c = document.getElementById('bcodigo').value;
  if (c == ''){
    c = document.getElementById('bfecha').value;
    if (c == ''){
      start('danger','Especifique una fecha on un código');
    } else {
      data.append('fecha',c);
    }
  } else {
    data.append('codigo',c);
  }
  data.append('hab',true);
  data.append('dia',d);
  cargadevistasimple('/listaclases','lista-clases',data,false);
};

// INICIO VISTAS DE DIAS DE CLASES
// INICIO DE ADMINISTRACION DE INSCRIPCIONES
var adminInscripcion = function(i,con) {
  data = new FormData();
  data.append('i',i);
  b = document.getElementById('i'+i);
  const request = new XMLHttpRequest();
  if (con == 'ok'){
    data.append('hab',true);
    t = document.getElementById('ti'+i)
    t.children[0].className = '';
    t.children[1].className = '';
    t.children[2].className = '';
    b.className = 'btn btn-danger btn-xs';
    b.innerHTML = "<span class='glyphicon glyphicon-remove-sign' aria-hidden='true'></span>";
    b.removeAttribute("onclick");
    b.setAttribute("onclick","adminInscripcion("+i+",'rm')");
  } else if(con == 'rm'){
    data.append('des',true);
    t = document.getElementById('ti'+i)
    t.children[0].className = 'noactivo';
    t.children[1].className = 'noactivo';
    t.children[2].className = 'noactivo';
    b.className = 'btn btn-primary btn-xs';
    b.innerHTML = "<span class='glyphicon glyphicon-ok-sign' aria-hidden='true'></span>";
    b.removeAttribute("onclick");
    b.setAttribute("onclick","adminInscripcion("+i+",'ok')");
  }
  request.open('POST','/adminInscripcion');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    start(`${respuesta.clase}`,`${respuesta.mensaje}`);
  };
  request.send(data);
  return false;
};
// FIN DE ADMINISTRACION DE INSCRIPCIONES
// LISTAS DE ASISTENCIA`
var mostrarLista = function(m) {
  data = new FormData()
  data.append('materia',m);
  cargadevistasimple('/listasistencia','lista'+m,data,false);
};
// FIN LISTAS DE ASISTENCIA

// CONSULTA DETALLADA DE ASISTENCIA
var consultaDetallada = function (alumno,materia) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('alumno',alumno);
  data.append('materia',materia);
  request.open('POST', '/detalleasistencia');
  request.onload = () => {
    document.getElementById('respuestaDetalle').innerHTML = request.response;
    $('#detAlumno').modal('show');
  };
  request.send(data);

  return false;
};
// FIN CONSULTA DETALLADA DE ASISTENCIA
// CONSULTA POR INTERVALOS DE FECHAS


var consultaIntervalo = function () {
  desde = document.getElementById('cdesde').value;
  hasta = document.getElementById('chasta').value;
  if (desde != '' && hasta != ''){
    const request = new XMLHttpRequest();
    const data = new FormData();;
    data.append('cdesde',desde);
    data.append('chasta',hasta);

    porcentaje = document.getElementById('consultaporcentaje').value;
    if (!porcentaje){
      data.append('porcentaje',porcentaje);
    }

    caCampos = document.querySelectorAll(".ccarreras");
    caconteo = 0;
    for (i = 0; i < caCampos.length; i++ ){
      if (caCampos[i].checked){
        data.append("carrera"+caCampos[i].value,caCampos[i].value);
        caconteo++;
      }
    }

    cuCampos = document.querySelectorAll(".ccursos");
    cuconteo = 0;
    for (i = 0; i < cuCampos.length; i++ ){
      if (cuCampos[i].checked){
        data.append("curso"+cuCampos[i].value,cuCampos[i].value);
        cuconteo++;
      }
    }


    cCampos = document.querySelectorAll(".csecciones");
    for (i = 0; i < cCampos.length; i++ ){
      if (cCampos[i].checked){
        data.append("seccion"+cCampos[i].value,cCampos[i].value)
      }
    }
    if (cuconteo > 1 && caconteo > 1){
      start('danger','Elija una sola carrera o elija un solo curso');
    } else {
      if (document.getElementById('consultadetmaterias').checked){
        if (cuconteo == 1 && caconteo == 1){
          data.append('consultadetmaterias',true);
          request.open('POST', '/consultaintervalo');
          request.onload = () => {
            var contenedor = document.createElement('div');
            contenedor.className = 'col-sm-12 col-md-12';
            contenedor.innerHTML = request.response;

            arbol = document.getElementById('listaintervalos');
            arbol.insertBefore(contenedor, arbol.firstChild);
          };
          request.send(data);
          return false;
        } else {
          start('danger', 'Si desea el detalle por materia, elija solo una materia y solo un curso');
        }
      } else {
        request.open('POST', '/consultaintervalo');
        request.onload = () => {
          var contenedor = document.createElement('div');
          contenedor.className = 'col-sm-12 col-md-12';
          contenedor.innerHTML = request.response;

          arbol = document.getElementById('listaintervalos');
          arbol.insertBefore(contenedor, arbol.firstChild);
        };
        request.send(data);
        return false;
      }
    }
  } else {
    start('danger','Ingrese un intervalo de fecha');
  }

};


// FIN DE CONSULTA POR INTERVALOS DE FECHA


// CONSULTA GENERAL
var consultadetgral = function () {
  const request = new XMLHttpRequest();
  const data = new FormData();
  f = document.getElementById('cfecha').value;
  s = document.getElementById('ccarrera');
  ca = s.options[s.selectedIndex].value;
  s = document.getElementById('ccurso');
  cu = s.options[s.selectedIndex].value;
  s = document.getElementById('cseccion');
  se = s.options[s.selectedIndex].value;
  if (f=='' && ca=='falta' && cu=='falta' && se=='falta') {
    start('danger','Elija al menos una opción para filtar la información sobre la asistencia');
  } else {
    if ( f!=''){
      data.append('cfecha',f);
    }
    if (ca!='falta') {
      data.append('ccarrera',ca);
    }
    if (cu!='falta') {
      data.append('ccurso',cu);
    }
    if (se!='falta') {
      data.append('cseccion',se);
    }
    data.append('consulta',true);
    request.open('POST', '/consultas');
    request.onload = () => {
      var contenedor = document.createElement('div');
      contenedor.className = 'col-sm-6 col-md-6';
      contenedor.innerHTML = request.response;

      arbol = document.getElementById('listaconsulta');
      arbol.insertBefore(contenedor, arbol.firstChild);
    };
    request.send(data);
    return false;


  }

};


// INICIO LLAMADO DE LISTAS

var listanterior = function (l) {
  var data = new FormData();
  data.append('listanterior',true);
  data.append('l',l);
  const request = new XMLHttpRequest();
  request.open('POST','/lista/0');
  request.onload = () => {
    document.getElementById('listanterior').innerHTML = request.response;
    $('#modalListanterior').modal('show');
    estado_inicial(false);
  };
  request.send(data);

  return false;
};


// FIN LLAMADO DE LISTAS
