document.addEventListener('DOMContentLoaded', function() {
  const request = new XMLHttpRequest();
  request.open('POST', '/perfil');
  request.onload = () => {
      document.getElementById('body').innerHTML = request.response;
  };
  request.send();
  return false;

});



var form1 = function(id) {
    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('nombre', document.getElementById('fnombre').value);
    data.append('apellido', document.getElementById('fapellido').value);
    data.append('ci', document.getElementById('fci').value);
    data.append('email', document.getElementById('femail').value);
    data.append('con', document.getElementById('fc').value);

    let e = document.getElementById('ftipo');

    data.append('tipo', e.options[e.selectedIndex].value);
    if (id == null){
      data.append('alta',true);
    } else {
      data.append('a_modificar',id);
    }
    request.open('POST', '/');
    request.onload = () => {
      if (id != null){
        document.getElementById('body').innerHTML = request.response;

      } else {
        document.getElementById('mensaje').innerHTML = request.response;
      }
    };
    request.send(data);

    return false;

};
var eliminar = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('baja', true);
  data.append('id',id);
  request.open('POST', '/');

  request.onload = () => {
    document.getElementById('mensaje').innerHTML = request.response;
  };
  request.send(data);

  return false;

};

var modificar = function(id) {
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('modificacion', true);
  data.append('id',id);
  request.open('POST', '/');

  request.onload = () => {
    document.getElementById('body').innerHTML = request.response;
  };
  request.send(data);

  return false;
};
