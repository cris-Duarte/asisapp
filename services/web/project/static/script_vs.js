document.addEventListener('DOMContentLoaded', () => {
  fa = document.querySelectorAll('.form-alumno')
  for (var i = 0; i < fa.length; i++) {
  fa[i].disabled = true;
}
});

const data = new FormData();
var acon = function () {
  const request = new XMLHttpRequest();
  v = document.getElementById('mcodigo').value;
  const data1 = new FormData();
  data1.append('v',v);
  data.append('cmateria',v);
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
    $('#infoAlumnoModal').modal('show');
  };
  request.send(data1);

  return false;
};

var verificarm = function () {
  v = document.getElementById('mcodigo').value;
  if (v != '' ) {
    const request = new XMLHttpRequest();
    const data1 = new FormData()
    data1.append('v',v);
    data1.append('verificarMateria',true);
    request.open('POST', '/alumnos');
    request.onload = () => {
      const data = JSON.parse(request.responseText);
      if (data.mensaje == "Ok") {
        const materiaInfo = `<h4><span class="label label-warning ">Materia: ${data.Materia}</span></h4>
                                  <h4><span class="label label-warning ">Curso: ${data.Curso}, sección: ${data.Seccion}</span></h4>
                                  <h4><span class="label label-warning ">Carrera: ${data.Carrera}</span></h4>
                                  <h4><span class="label label-warning ">Docente: ${data.Docente}</span></h4>`;
              document.getElementById('infomateria').innerHTML = materiaInfo;
        }else{
            document.getElementById('infomateria').innerHTML = data.mensaje;
        }
    };
    request.send(data1);

    return false;
  }
};

var verificara = function () {
  v = document.getElementById('aci').value;
  if (v != '' ) {
    const request = new XMLHttpRequest();
    const data1 = new FormData()
    data1.append('v',v);
    data1.append('verificarAlumno',true);
    request.open('POST', '/alumnos');
    request.onload = () => {
      const data = JSON.parse(request.responseText);
      if (data.registro == "listo") {

        }else{
            document.getElementById('infoalumno').innerHTML = "Por favor completa los siguientes campos";
            fa = document.querySelectorAll('.form-alumno')
            for (var i = 0; i < fa.length; i++) {
            fa[i].disabled = false;
}
        }
    };
    request.send(data1);

    return false;
  }
};
