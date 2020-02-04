var indice_actual = 1
var alumnos = []
document.addEventListener('DOMContentLoaded', () => {
  alumnos = document.querySelectorAll('.alumno');

  duplalumno = alumnos[0].cloneNode(true);
  duplalumno.style.display = 'block';
  document.getElementById('anterior').appendChild(duplalumno);

  duplalumno = alumnos[1].cloneNode(true);
  duplalumno.style.display = 'block';
  document.getElementById('actual').appendChild(duplalumno);

  duplalumno = alumnos[2].cloneNode(true);
  duplalumno.style.display = 'block';
  duplalumno.style.opacity = 0.2;
  document.getElementById('siguiente').appendChild(duplalumno);

});

//.dataset.id;

var s = function () {

};

var a = function () {

};



var siguiente = function () {
  if (indice_actual < alumnos.length - 2  ) {
    indice_actual++;

    duplalumno = alumnos[indice_actual-1].cloneNode(true);
    duplalumno.style.display = 'block';
    duplalumno.style.opacity = 0.2;
    p = document.getElementById('anterior');
    p.replaceChild(duplalumno, p.childNodes[0]);

    duplalumno = alumnos[indice_actual].cloneNode(true);
    duplalumno.style.display = 'block';
    p = document.getElementById('actual');
    p.replaceChild(duplalumno, p.childNodes[0]);

    duplalumno = alumnos[indice_actual+1].cloneNode(true);
    duplalumno.style.display = 'block';
    duplalumno.style.opacity = 0.2;
    p = document.getElementById('siguiente');
    p.replaceChild(duplalumno, p.childNodes[0]);
  }

};

var atras = function () {
  if (indice_actual > 1) {
    indice_actual--;

    duplalumno = alumnos[indice_actual-1].cloneNode(true);
    duplalumno.style.display = 'block';
    duplalumno.style.opacity = 0.2;
    p = document.getElementById('anterior');
    p.replaceChild(duplalumno, p.childNodes[0]);

    duplalumno = alumnos[indice_actual].cloneNode(true);
    duplalumno.style.display = 'block';
    p = document.getElementById('actual');
    p.replaceChild(duplalumno, p.childNodes[0]);

    duplalumno = alumnos[indice_actual+1].cloneNode(true);
    duplalumno.style.display = 'block';
    duplalumno.style.opacity = 0.2;
    p = document.getElementById('siguiente');
    p.replaceChild(duplalumno, p.childNodes[0]);

    }
};

var listar = function (idc,condicion) {
  if (indice_actual > 1 && indice_actual < alumnos.length-2) {
  a = document.getElementById('actual');
  ida = a.firstElementChild.dataset.id;
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('ida',ida);
  data.append('idc',idc);
  data.append('condicion',condicion);
  request.open('POST', '/listar');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    if (respuesta.condicion == 'Ausente'){
      start('danger','<span class="glyphicon glyphicon-remove" aria-hidden="true"></span> ',`${respuesta.nombre} - ${respuesta.condicion}`);
      alumnos[indice_actual].className = 'alumno label label-danger label-alumno';
    } else if (condicion == 'Presente') {
      start('success','<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> ',`${respuesta.nombre} - ${respuesta.condicion}`);
      alumnos[indice_actual].className = 'alumno label label-success label-alumno';
    } else{
      start('default','<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> ',`${respuesta.nombre} - ${respuesta.condicion}`);
      alumnos[indice_actual].className = 'alumno label label-default label-alumno';
    }
    siguiente();
  };
  request.send(data);
  return false;
} else {
  siguiente();
}
}
