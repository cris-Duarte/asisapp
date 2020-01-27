document.addEventListener('DOMContentLoaded', () => {
  fa = document.querySelectorAll('.form-alumno')
  for (var i = 0; i < fa.length; i++) {
  fa[i].disabled = true;
}
  document.getElementById('infoproceso').style.display = 'none'
});


var acon = function () {
  const data = new FormData();
  const request = new XMLHttpRequest();
  data.append('cmateria',document.getElementById('mcodigo').value);
  data.append('anombre',document.getElementById('anombre').value);
  data.append('aapellido',document.getElementById('aapellido').value);
  data.append('aci',document.getElementById('aci').value);
  data.append('aemail',document.getElementById('aemail').value);
  data.append('atelefono',document.getElementById('atelefono').value);
  data.append('alta_alumno',true);
  request.open('POST', '/alumnos');

  request.onload = () => {
    const data = JSON.parse(request.responseText);
    e = document.getElementById('infoproceso');
    e.className = '';
    e.classList.add('alert');
    e.classList.add(data.clase);
    e.innerHTML = data.mensaje;
    document.getElementById('infoproceso').style.display = 'inline-block'

  };
  request.send(data);
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
        const materiaInfo = `<h4><span class="label label-info">Materia: ${data.Materia}</span></h4>
                                  <h4><span class="label label-info">Curso: ${data.Curso}, sección: ${data.Seccion}</span></h4>
                                  <h4><span class="label label-info">Carrera: ${data.Carrera}</span></h4>
                                  <h4><span class="label label-info">Docente: ${data.Docente}</span></h4>`;
              document.getElementById('infomateria').innerHTML = materiaInfo;
              document.getElementById('btnAltaAlumno').disabled = false;
        }else{
            document.getElementById('infomateria').innerHTML = '<h4><span class="label label-danger">'+data.mensaje+'</span></h4>';
            document.getElementById('btnAltaAlumno').disabled = true;
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
        document.getElementById('anombre').value = data.nombre;
        document.getElementById('aapellido').value = data.apellido;
        document.getElementById('aemail').value = data.email;
        document.getElementById('atelefono').value = data.telefono;
        fa = document.querySelectorAll('.form-alumno');
        for (var i = 0; i < fa.length; i++) {
          fa[i].disabled = true;
        }
        }else{
            document.getElementById('infoalumno').innerHTML = '<h4><span class="label label-warning ">Por favor completa los siguientes campos</span></h4>';
            fa = document.querySelectorAll('.form-alumno');
            for (var i = 0; i < fa.length; i++) {
              fa[i].disabled = false;
            }
        }
    };
    request.send(data1);

    return false;
  }
};
