document.addEventListener('DOMContentLoaded', function() {
  perfil();
});
var perfil = function() {
  const request = new XMLHttpRequest();
  request.open('POST', '/perfil');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;
};

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

var materias = function() {
  const request = new XMLHttpRequest();
  request.open('POST', '/materias');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;
};
var periodos = function() {
  const request = new XMLHttpRequest();
  request.open('POST', '/periodos');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;
};

var addPeriodo = function () {
  const data = new FormData();
  data.append('pnombre',document.getElementById('pnombre').value);
  data.append('pfechad',document.getElementById('pfechad').value);
  data.append('pfechah',document.getElementById('pfechah').value);
  data.append('altaperiodo',true);
  const request = new XMLHttpRequest();
  request.open('POST', '/periodos');
  request.onload = () => {
    document.getElementById('tablaperiodos').innerHTML = request.response;
  };
  request.send(data);

  return false;

};

var peliminar = function (pid) {
  const data = new FormData();
  data.append('pid',pid);
  data.append('bajaperiodo');
  const request = new XMLHttpRequest();
  request.open('POST', '/periodos');
  request.onload = () => {
    document.getElementById('tablaperiodos').innerHTML = request.response;
  };
  request.send(data);

  return false;
}

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
      data.append('a_modificar',id);
    }
    request.open('POST', '/materias');
    request.onload = () => {
      if (id != null){
        document.getElementById('body').innerHTML = request.response;

      } else {
        document.getElementById('tablaconsulta').innerHTML = request.response;
      }
    };
    request.send(data);

    return false;

};
var mmod = function(id) {
    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('mnombre', document.getElementById('mmnombre').value);
    data.append('mcodigo', document.getElementById('mmcodigo').value);
    let e = document.getElementById('mmcurso');
    data.append('mcurso', e.options[e.selectedIndex].value);

    let f = document.getElementById('mmseccion');
    data.append('mseccion', f.options[f.selectedIndex].value);

    let g = document.getElementById('mmcarrera');
    data.append('mcarrera', g.options[g.selectedIndex].value);

    let h = document.getElementById('mmdocente');
    data.append('mdocente', h.options[h.selectedIndex].value);
    data.append('a_modificar',id);
    request.open('POST', '/materias');
    request.onload = () => {
    document.getElementById('tablaconsulta').innerHTML = request.response;
    $('#modModal').modal('hide');
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



var minfo = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('minfo', true);
  data.append('mid',id);
  request.open('POST', '/miscelaneos');

  request.onload = () => {
    document.getElementById('mensaje').innerHTML = request.response;
    $('#minfoModal').modal('show');
  };
  request.send(data);

  return false;

};

var cerrarModModal = function() {
  $('#modModal').modal('hide');
};

var mmodificar = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('modificacion', true);
  data.append('mid',id);
  request.open('POST', '/materias');

  request.onload = () => {
    document.getElementById('mensaje').innerHTML = request.response;
    $('#modModal').modal('show');
  };
  request.send(data);

  return false;
};

var addHorario = function(mhid) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('mhid',mhid);
  let e = document.getElementById('hdia');
  data.append('hdia', e.options[e.selectedIndex].value);
  data.append('hfechad', document.getElementById('hfechad').value);
  data.append('hfechah', document.getElementById('hfechah').value);
  data.append('hhorad', document.getElementById('hhorad').value);
  data.append('hhorah', document.getElementById('hhorah').value);
  data.append('hsala', document.getElementById('hsala').value);
  data.append('halta',true);
  request.open('POST', '/miscelaneos');
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
  request.open('POST', '/miscelaneos');

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
  let e = document.getElementById('mhdia');
  data.append('hdia', e.options[e.selectedIndex].value);
  data.append('hfechad', document.getElementById('mhfechad').value);
  data.append('hfechah', document.getElementById('mhfechah').value);
  data.append('hhorad', document.getElementById('mhhorad').value);
  data.append('hhorah', document.getElementById('mhhorah').value);
  data.append('hsala', document.getElementById('mhsala').value);
  data.append('modHorario',true);
  request.open('POST', '/miscelaneos');
  request.onload = () => {
    document.getElementById('mhorario').innerHTML = request.response;
    $('#modHorarioModal').modal('hide');
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
  request.open('POST', '/miscelaneos');

  request.onload = () => {
    document.getElementById('auxBox1').innerHTML = request.response;
    $('#modHorarioModal').modal('show');
  };
  request.send(data);

  return false;
};
