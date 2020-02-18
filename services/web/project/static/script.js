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
           console.log(opt[i].id+" "+opt[i].value);
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

var salir = function() {

  /*var ga = gapi.auth2.getAuthInstance();
  ga.grantOfflineAccess();
    ga.signOut().then(function () {
      console.log('User signed out.');
    });*/
  const request = new XMLHttpRequest();
  request.open('POST','/salir');
  request.onload = () => {

  };
  request.send();
  return false;
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
    document.getElementById('mcodigo').value = respuesta.codigo;
    document.getElementById(`curso${respuesta.curso}`).selected = true;
    document.getElementById(`${respuesta.seccion}`).selected = true;
    document.getElementById(`carrera${respuesta.carrera}`).selected = true;
    document.getElementById(`docente${respuesta.docente}`).selected = true;

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
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('mid',mhid);
  e = document.getElementById('hdia');
  data.append('hdia', e.options[e.selectedIndex].value);
  e = document.getElementById('hperiodo');
  data.append('hperiodo', e.options[e.selectedIndex].value);
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
  e = document.getElementById('hperiodo');
  data.append('hperiodo', e.options[e.selectedIndex].value);
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
    document.getElementById(`periodo${respuesta.periodo}`).selected = true;
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
  document.getElementById('hperiodo').firstElementChild.selected = true;

  b = document.getElementById('btnhorario');
  b.innerHTML = "<span class='glyphicon glyphicon-save' aria-hidden='true'></span> Guardar Horario Nueva";
  b.removeAttribute("onclick");
  b.setAttribute("onclick","malta("+b.dataset.id+")");
};

// FIN DE ADMINISTRACION DE HORARIOS
