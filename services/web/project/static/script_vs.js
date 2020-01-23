const data = new FormData();
var acon = function () {
  const request = new XMLHttpRequest();
  v = document.getElementById('mcodigo').value;
  data.append('cmateria',e);
  document.getElementById('cmateria').innerHTML = v
  e = document.getElementById('anombre').value;
  data.append('anombre',e);
  document.getElementById('aanombre').innerHTML = e
  e = document.getElementById('aapellido').value;
  data.append('aapellido',e);
  document.getElementById('aaapellido').innerHTML = e
  e = document.getElementById('aci').value;
  data.append('aci',e);
  document.getElementById('aaci').innerHTML = e
  e = document.getElementById('aemail').value;
  data.append('aemail',e);
  document.getElementById('aaemail').innerHTML = e
  e = document.getElementById('atelefono').value;
  data.append('atelefono',e);
  document.getElementById('aatelefono').innerHTML = e
  request.open('POST', '/alumnos');

  request.onload = () => {
    document.getElementById('nmateria').innerHTML = request.response;
    $('#infoAlumnoModal').modal('hide');
  };
  request.send(v);

  return false;
};
