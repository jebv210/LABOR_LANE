from flask import Blueprint, render_template, request
import mysql.connector
from app.db_config import db_config

formulario_bp = Blueprint('formulario', __name__)


@formulario_bp.route('/formulario/empleados')
def formulario():
    return render_template('/formulario.html')


@formulario_bp.route('/procesar-datos', methods=['GET','POST'])
def procesar_datos(): 
    cnx = mysql.connector.connect(**db_config)
    nombres = request.form['nombres']
    p_apellido = request.form['p_apellido']
    s_apellido = request.form['s_apellido']
    genero = request.form['genero']
    tipo_documento = request.form['tipo_documento']
    numero_documento = int(request.form['numero_documento'])
    fecha_nacimiento = request.form['fecha_nacimiento']
    celular_u = int(request.form['celular_u'])
    celular_d = int(request.form['celular_d'])
    direccion = request.form['direccion']
    estrato = request.form['estrato']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    estadocivil = request.form['estado_civil']
    personasacargo = request.form['personasacargo']
    LibretaMilitar = request.form['LibretaMilitar']
    Contenido = request.form['Contenido']
    rol = request.form['rol']
    Barrio = request.form['Barrio']
    Estado = 'ACTIVO'
    cursor = cnx.cursor()
    sql = "insert into usuario (NombresUsuario, PrimerApellidoUsuario, SegundoApellidoUsuario, GeneroUsuario, TipoDocumentoUsuario, NumeroDocumentoUsuario, FechaNacimiento, CelularUsuario, Celular2Usuario, DireccionUsuario, EstratoResidencia, CorreoUsuario, ContraseñaUsuario, EstadoCivil, PersonasACargo, Libreta, Contenido, FK_IdRol, ZonaResidencia, Estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" # Parámetros de la consulta SQL   
    data = (nombres, p_apellido, s_apellido, genero, tipo_documento, numero_documento, fecha_nacimiento, celular_u, celular_d, direccion, estrato, correo, contraseña, estadocivil, personasacargo, LibretaMilitar, Contenido, rol, Barrio, Estado)
    print(data)
    try:                          
        cursor.execute(sql, data)
        cnx.commit()
        mensaje = "Datos insertados correctamente"      
        men = data[0]
        print(data)
    except mysql.connector.Error as error:       
            print("Error al insertar los datos:", error)
            mensaje = "Error al insertar los datos"   
    cursor.close()
    cnx.close()  
    if mensaje== "Datos insertados correctamente" and data[17] == '3':
        return render_template('/habilidades.html', men=men)
    elif mensaje== "Datos insertados correctamente":
        return render_template('/OfertaEmpleo.html', men=men)
    else:
        return render_template('/resultado.html', mensaje=mensaje)