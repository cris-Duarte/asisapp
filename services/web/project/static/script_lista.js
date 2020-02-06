var indice_actual = 1;
var alumnos = [];
  document.addEventListener('DOMContentLoaded', () => {
    if (!sin_alumnos){
      estado_inicial(false);
    }

});

var estado_inicial = function (i) {
  if (i) {
    v = document.getElementById('anterior');
    v.removeChild(v.childNodes[0]);
    v = document.getElementById('actual');
    v.removeChild(v.childNodes[0]);
    v = document.getElementById('siguiente');
    v.removeChild(v.childNodes[0]);
  }
  indice_actual = 1;
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
  actualizarcantidad(0)
}

var actualizarcantidad = function (vi) {
  c = document.getElementById('cantidadalumnos');
  i = vi;
  a = alumnos.length - 4;
  c.innerHTML = i+" de "+a+" Alumnos llamados"
}

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
  t = document.getElementById('asistipo');
  ida = a.firstElementChild.dataset.id;
  const request = new XMLHttpRequest();
  const data = new FormData();
  data.append('ida',ida);
  data.append('idc',idc);
  data.append('condicion',condicion);
  data.append('tipo', t.options[t.selectedIndex].value)
  request.open('POST', '/listar');
  request.onload = () => {
    const respuesta = JSON.parse(request.responseText);
    if(respuesta.resultado=='ok'){
      if (respuesta.condicion == 'Ausente'){
        start('danger','<span class="glyphicon glyphicon-remove" aria-hidden="true"></span> ',`${respuesta.nombre} - ${respuesta.tipo}: ${respuesta.condicion}`);
        alumnos[indice_actual].className = 'alumno label label-danger label-alumno';
      } else if (condicion == 'Presente') {
        start('success','<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> ',`${respuesta.nombre} - ${respuesta.tipo}: ${respuesta.condicion}`);
        alumnos[indice_actual].className = 'alumno label label-success label-alumno';
      } else{
        start('default','<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> ',`${respuesta.nombre} - ${respuesta.tipo}: ${respuesta.condicion}`);
        alumnos[indice_actual].className = 'alumno label label-default label-alumno';
      }
      actualizarcantidad(indice_actual - 1)
      siguiente();
    } else {
      document.getElementById('mensajeError').innerHTML = respuesta.mensaje;
      $('#errorModal').modal('show');
    }
    };
  request.send(data);
  return false;
} else {
  siguiente();
}
}
