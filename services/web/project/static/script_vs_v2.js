var buscar = function() {
  ci = document.getElementById('cia').value;
  if (ci == ''){
    start('danger','Ingresa tu número de C.I.');
  } else {
    const request = new XMLHttpRequest();
    request.open('POST','/detasistencia');
    request.onload = () => {
        document.getElementById('detasistencia').innerHTML = request.response;
    };
    var data = new FormData();
    data.append('ci',ci)
    request.send(data);
    return false;
  }
};
