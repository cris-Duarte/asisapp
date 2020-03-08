def eliminarAsistencia(m):
    m = Materia.query.get(m)
    h = Horario.query.filter(Horario.materia=m.id).all()

    for ho in h:
        dia = Diadeclase.query.filter(Diadeclase.horario=ho.id).all()

        for d in dia:
            as = Asistencia.query.filter(Asistencia.diadeclase==d.id).all()
            if as:
                for a in as:
                    i = Inscripcion.query.filter(Inscripcion.alumno=a.alumno).filter(Inscripcion.materia=m.id)
                    if i.count()==1:
                        i = i.first()
                        print(m.nombre+","+i.fecha+","+a.asistencias.nombre+","+a.asistencia.apellido+","+","+a.tipo+","+a.condicion)
                    else:
                        print("Inscripcion doblee")
                    #db.session.delete(a)
                    #db.session.commit()
