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
  document.getElementById('siguiente').appendChild(duplalumno);
  alert('ok');
});

//.dataset.id;

var comenzar = function () {

}

var siguiente = function () {
  if (indice_actual < alumnos.length - 1) {
    indice_actual++;
    duplalumno = alumnos[indice_actual-1].cloneNode(true);
    duplalumno.style.display = 'block';
    p = document.getElementById('anterior');
    if (indice_actual == 1) {
      p.appendChild(duplalumno);
    } else {
      p.replaceChild(duplalumno, p.childNodes[0]);
    }

    duplalumno = alumnos[indice_actual].cloneNode(true);
    duplalumno.style.display = 'block';
    p = document.getElementById('actual');
    p.replaceChild(duplalumno, p.childNodes[0]);
    if (indice_actual == alumnos.length - 1) {
      p = document.getElementById('siguiente');
      p.removeChild(p.childNodes[0]);
    } else {
      duplalumno = alumnos[indice_actual+1].cloneNode(true);
      duplalumno.style.display = 'block';
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
    p = document.getElementById('anterior');
    p.replaceChild(duplalumno, p.childNodes[0]);
  }
    duplalumno = alumnos[indice_actual].cloneNode(true);
    duplalumno.style.display = 'block';
    p = document.getElementById('actual');
    p.replaceChild(duplalumno, p.childNodes[0]);

    duplalumno = alumnos[indice_actual+1].cloneNode(true);
    duplalumno.style.display = 'block';
    p = document.getElementById('siguiente');
    if (indice_actual == alumnos.length-2) {
      p.appendChild(duplalumno);
    } else {
      p.replaceChild(duplalumno, p.childNodes[0]);
    }
  }
};

var presente = function () {
  siguiente();
}

var ausente = function () {
  siguiente();
}
