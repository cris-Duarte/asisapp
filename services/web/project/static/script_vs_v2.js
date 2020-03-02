var balumno = function() {
  ci = document.getElementById('balumno').value;
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

var detalle = function(a,m){
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('vistaAlumno',true);
  data.append('ida',a);
  data.append('materia',m);
  request.open('POST', '/detalleasistencia');
  request.onload = () => {
    document.getElementById('lista'+m).innerHTML = request.response;
  };
  request.send(data);
  return false;
};
