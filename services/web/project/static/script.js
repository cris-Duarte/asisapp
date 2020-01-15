document.addEventListener('DOMContentLoaded', function() {
  const request = new XMLHttpRequest();
  request.open('POST', '/perfil');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;

});

var materias = function() {
  const request = new XMLHttpRequest();
  request.open('POST', '/materias');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;
};

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
