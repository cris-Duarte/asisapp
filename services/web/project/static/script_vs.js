document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('anombre').disabled = true;
  document.getElementById('aapellido').disabled = true;
  document.getElementById('atelefono').disabled = true;
  document.getElementById('aemail').disabled = true;
  document.getElementById('infoproceso').style.display = 'none'
});

var acon = function () {
  p = new FormP('.form-alumno');
  p.formV();
  if (p.bandera) {
    const request = new XMLHttpRequest();
    data = p.data;
    data.append('alta_alumno',true)
    request.open('POST', '/alumnos');
    request.onload = () => {
      const respuesta = JSON.parse(request.responseText);
      e = document.getElementById('infoproceso');
      e.className = '';
      e.classList.add('alert');
      e.classList.add(respuesta.clase);
      e.innerHTML = respuesta.mensaje;
      document.getElementById('infoproceso').style.display = 'inline-block'
    };
    request.send(data);
    return false;
  } else {
    start('danger','Por favor complete todos los campos');
  }
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
        const materiaInfo = `<p class="label label-info label-inline">Materia: ${data.Materia}</p>
                                  <p class="label label-info label-inline">Curso: ${data.Curso}, sección: ${data.Seccion}</p>
                                  <p class="label label-info label-inline">Carrera: ${data.Carrera}</p>
                                  <p class="label label-info label-inline">Docente: ${data.Docente}</p>`;
              document.getElementById('infomateria').innerHTML = materiaInfo;
              document.getElementById('btnAltaAlumno').disabled = false;
        }else{
            document.getElementById('infomateria').innerHTML = '<p class="label label-danger label-inline">'+data.mensaje+'</p>';
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
        document.getElementById('anombre').disabled = true;
        document.getElementById('aapellido').value = data.apellido;
        document.getElementById('aapellido').disabled = true;
        document.getElementById('aemail').value = data.email;
        document.getElementById('atelefono').value = data.telefono;
        document.getElementById('aemail').disabled = false;
        document.getElementById('atelefono').disabled = false;
        }else{
            document.getElementById('infoalumno').innerHTML = '<span class="label label-warning label-inline">Por favor completa los siguientes campos</span>';
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

class FormP {
  constructor (nombre_grupo) {
    this.nombre_grupo = nombre_grupo;
    this.bandera = true;
    this.btn = false;
    this.data = new FormData();
  }
  // Método
  formV () {
    var bandera = true;
     var opt = document.querySelectorAll(this.nombre_grupo);
     for (var i = 0; i < opt.length; i++) {
       if (opt[i].type == 'text' || opt[i].type == 'number' || opt[i].type == 'email' || opt[i].type == 'password' || opt[i].type == 'date') {
         if (opt[i].value == ""){
           this.bandera = false;
         } else {
           this.data.append(opt[i].id,opt[i].value);
           console.log(opt[i].id+" "+opt[i].value);
         }
       } else if (opt[i].type == 'select-one'){
         let e = opt[i]
         if (e.selectedIndex == 0){
           this.bandera = false;
         } else {
           this.data.append(e.id, e.options[e.selectedIndex].value);
         }
       } else if (opt[i].type == 'button') {
         this.btn = opt[i];
       }
     }
   }
};
