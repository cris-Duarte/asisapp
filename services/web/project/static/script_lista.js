function cerrar() {
   window.open('','_parent','');
   window.close();
}
var alumnos = []
var indice_actual = 0
document.addEventListener('DOMContentLoaded', () => {
  alumnos = document.querySelectorAll('.alumno');
  duplalumno = alumnos[0].cloneNode(true);
  duplalumno.style.display = 'block';
  document.getElementById('actual').appendChild(duplalumno);
  duplalumno = alumnos[1].cloneNode(true);
  duplalumno.style.display = 'block';
  duplalumno.style.opacity = 0.2;
  document.getElementById('siguiente').appendChild(duplalumno);

});

//.dataset.id;



var siguiente = function () {
  if (indice_actual < alumnos.length) {
    indice_actual++;
    duplalumno = alumnos[indice_actual-1].cloneNode(true);
    duplalumno.style.display = 'block';
    duplalumno.style.opacity = 0.2;
    p = document.getElementById('anterior');
    if (indice_actual == 1) {
      p.appendChild(duplalumno);
    } else {
      p.replaceChild(duplalumno, p.childNodes[0]);
    }
    if (indice_actual == alumnos.length) {
      p = document.getElementById('actual');
      p.innerHTML = '<p class="alumno label label-info label-alumno">Ya haz llamado toda la lista</p>';
    } else {
    duplalumno = alumnos[indice_actual].cloneNode(true);
    duplalumno.style.display = 'block';
    p = document.getElementById('actual');
    p.replaceChild(duplalumno, p.childNodes[0]);
    }
    if (indice_actual == alumnos.length - 1 ) {
      p = document.getElementById('siguiente');
      p.removeChild(p.childNodes[0]);
    } else if(indice_actual == alumnos.length){} else{
      duplalumno = alumnos[indice_actual+1].cloneNode(true);
      duplalumno.style.display = 'block';
      duplalumno.style.opacity = 0.2;
      p = document.getElementById('siguiente');
      p.replaceChild(duplalumno, p.childNodes[0]);
  }
  }

};

var atras = function () {
  if (indice_actual > 0) {
    indice_actual--;
    if (indice_actual == 0) {
      p = document.getElementById('anterior');
      p.removeChild(p.childNodes[0]);
    } else {
    duplalumno = alumnos[indice_actual-1].cloneNode(true);
    duplalumno.style.display = 'block';
    duplalumno.style.opacity = 0.2;
    p = document.getElementById('anterior');
    p.replaceChild(duplalumno, p.childNodes[0]);
  }
    duplalumno = alumnos[indice_actual].cloneNode(true);
    duplalumno.style.display = 'block';
    p = document.getElementById('actual');
    p.replaceChild(duplalumno, p.childNodes[0]);

    if (indice_actual != alumnos.length - 1){
      duplalumno = alumnos[indice_actual+1].cloneNode(true);
      duplalumno.style.display = 'block';
      duplalumno.style.opacity = 0.2;
      p = document.getElementById('siguiente');
      if (indice_actual == alumnos.length - 2) {
        p.appendChild(duplalumno);
      } else {
        p.replaceChild(duplalumno, p.childNodes[0]);
      }
    }
  }
};

var listar = function (idc,condicion) {
  a = document.getElementById('actual');
  ida = a.childNodes[0].dataset.id;
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('ida',ida);
  data.append('idc',idc);
  data.append('condicion',condicion);
  request.open('POST', '/listar');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    if (respuesta.condicion == 'Ausente'){
      start('danger','<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span> ',`${respuesta.nombre} - ${respuesta.condicion}`);
      alumnos[indice_actual].className = 'alumno label label-danger label-alumno';
    } else if (condicion == 'Presente') {
      start('success','<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> ',`${respuesta.nombre} - ${respuesta.condicion}`);
      alumnos[indice_actual].className = 'alumno label label-success label-alumno';
    }
    siguiente();
  };
  request.send(data);
  return false;

}