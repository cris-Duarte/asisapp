document.addEventListener('DOMContentLoaded', function() {
  perfil();
});
// CLASES
class FormP {
  constructor (nombre_grupo) {
    this.nombre_grupo = nombre_grupo;
    this.bandera = true;
  }
  // Método
  formV () {
    var data = new FormData();
    var opt = document.querySelectorAll(this.nombre_grupo);
    for (var i = 0; i < opt.length - 1; i++) {
      if (opt[i].type == 'text'){
        if (opt[i].value == ''){
          this.bandera = false;
        } else {
          data.append(opt[i].id,opt[i].value);
        }
      } else if (opt[i].type == 'select-one'){
        let e = opt[i]
        if (e.selectedIndex == 0){
          this.bandera = false;
        } else {
          data.append(e.id, e.options[e.selectedIndex].value);
        }
      }
    }
    return data;
  }
};

// Elementos cargados por el NAVBAR, perfil, materias, periodos
var perfil = function() {
  const request = new XMLHttpRequest();
  request.open('POST', '/perfil');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;
};
var materias = function() {
  const request = new XMLHttpRequest();
  request.open('POST', '/materias');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;
};
var administracion = function() {
  const request = new XMLHttpRequest();
  request.open('POST', 'administracion');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;
};
var misclases = function () {
  const request = new XMLHttpRequest();
  request.open('POST', '/misclases');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
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
  f = new FormP('.form-docentes');
  if (f.bandera){
    const request = new XMLHttpRequest();
    request.open('POST', '/docentes');
    data = f.formV();
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
    }
  };
  request.send(data);

  return false;
}
//FIN DE ALTA DE DOCENTES
// INICIO DE ADMINISTRACION DE PERIODOS
var addPeriodo = function (id) {
  const data = new FormData();
  data.append('admin-periodos',true);
  data.append('pnombre',document.getElementById('pnombre').value);
  data.append('pfechad',document.getElementById('pfechad').value);
  data.append('pfechah',document.getElementById('pfechah').value);
  if (id != null){
    data.append('pid',id);
    data.append('guardarmodperiodo',true);
  } else {
    data.append('altaperiodo',true);
  }
  const request = new XMLHttpRequest();
  request.open('POST', 'administracion');
  request.onload = () => {
  document.getElementById('admin-periodos').innerHTML = request.response;
  };
  request.send(data);

  return false;

};
var peliminar = function (pid) {
  const data = new FormData();
  data.append('admin-periodos',true);
  data.append('pid',pid);
  data.append('bajaperiodo',true);
  const request = new XMLHttpRequest();
  request.open('POST', 'administracion');
  request.onload = () => {
    document.getElementById('admin-periodos').innerHTML = request.response;
  };
  request.send(data);

  return false;
};
var pmodificar = function (pid) {
  const data = new FormData();
  data.append('admin-periodos',true);
  data.append('pid',pid);
  data.append('modperiodo',true);
  const request = new XMLHttpRequest();
  request.open('POST', 'administracion');
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
  document.getElementById('pnombre').value = "";
  document.getElementById('pfechad').value = "";
  document.getElementById('pfechah').value = "";
  btn = document.getElementById('btnPeriodo');
  btn.removeAttribute("onclick");
  btn.setAttribute("onclick","addPeriodo()");
  btn.innerHTML = '<span class="glyphicon glyphicon-save" aria-hidden="true"></span> Guardar Periodo Nuevo';
};
// FIN DE ADMINISTRACION DE PERIODOS
// INICIO DE ADMINISTRACION DE MATERIAS
var malta = function(id) {
    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('mnombre', document.getElementById('mnombre').value);
    data.append('mcodigo', document.getElementById('mcodigo').value);

    let e = document.getElementById('mcurso');
    data.append('mcurso', e.options[e.selectedIndex].value);

    let f = document.getElementById('mseccion');
    data.append('mseccion', f.options[f.selectedIndex].value);

    let g = document.getElementById('mcarrera');
    data.append('mcarrera', g.options[g.selectedIndex].value);

    let h = document.getElementById('mdocente');
    data.append('mdocente', h.options[h.selectedIndex].value);

    if (id == null){
      data.append('alta',true);
    } else {
      data.append('a_modificar',true);
      data.append('mid',id);
    }
    request.open('POST', '/materias');
    request.onload = () => {
      if (id != null){
        mcancelar();
      }
      document.getElementById('tablaconsulta').innerHTML = request.response;
    };
    request.send(data);

    return false;

};
var meliminar = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('mbaja', true);
  data.append('mid',id);
  request.open('POST', '/materias');

  request.onload = () => {
    document.getElementById('tablaconsulta').innerHTML = request.response;
  };
  request.send(data);

  return false;

};
var mmodificar = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('modificacion', true);
  data.append('mid',id);
  request.open('POST', '/materias');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    document.getElementById('mnombre').value = respuesta.nombre;
    document.getElementById('mcodigo').value = respuesta.codigo;
    document.getElementById(`${respuesta.curso}`).selected = true;
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

  document.getElementById('mnombre').value = "";
  document.getElementById('mcodigo').value = "";
  document.getElementById('mcurso').firstElementChild.selected = true;
  document.getElementById('mseccion').firstElementChild.selected = true;
  document.getElementById('mcarrera').firstElementChild.selected = true;
  document.getElementById('mdocente').firstElementChild.selected = true;

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
