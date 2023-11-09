from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
import base64


app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

# Configuracion de la base de datos


@app.route('/') # funcion desde flask
def home(): #etiqueta para definir la funcion
    if 'nombres' in session:
        return render_template('home.html', nombres=session['nombres'])
    return render_template('home.html') #se redirecciona al archivo entre las comillas
#home (juan esteban)



#Login---------------------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('login.html')# aqui es donde esta para la direccion del html
# pene dentro de julian
@app.route('/datos-login', methods=['GET', 'POST'])
def datos():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
    cnx = mysql.connector.connect(**db_config)
    if request.method == 'POST':
        nombres = request.form['Usuario']
        contraseña = request.form['Contraseña']
        cursor = cnx.cursor()
        sql = "SELECT * FROM usuario WHERE NombresUsuario=%s AND ContraseñaUsuario=%s"
        data = (nombres, contraseña)
        cursor.execute(sql, data)
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['nombres'] = nombres
            return redirect(url_for('home'))
        else:
            return "Inicio de sesion fallido"
    return render_template('login.html')
#FORMULARIO EMPLEADO-------------------------------------# Ruta para mostrar el formulario
@app.route('/formulario/empleados')
def formulario():
    return render_template('/formulario.html')# aqui es donde esta para la direccion del html
# Ruta para procesar los datos del formulario de empleado (1)-------------------------------------------------



@app.route('/procesar-datos', methods=['GET','POST'])
def procesar_datos(): # Obtener los datos del formulario
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
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
    # Establecer la conexión a la base de datos   
    cursor = cnx.cursor()
    sql = "insert into usuario (NombresUsuario, PrimerApellidoUsuario, SegundoApellidoUsuario, GeneroUsuario, TipoDocumentoUsuario, NumeroDocumentoUsuario, FechaNacimiento, CelularUsuario, Celular2Usuario, DireccionUsuario, EstratoResidencia, CorreoUsuario, ContraseñaUsuario, EstadoCivil, PersonasACargo, Libreta, Contenido, FK_IdRol, ZonaResidencia, Estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" # Parámetros de la consulta SQL   
    data = (nombres, p_apellido, s_apellido, genero, tipo_documento, numero_documento, fecha_nacimiento, celular_u, celular_d, direccion, estrato, correo, contraseña, estadocivil, personasacargo, LibretaMilitar, Contenido, rol, Barrio, Estado)
    print(data)
    try:# intentar ejecutar la consulta con los datos (llenar los values de sql con data)                # Ejecutar la consulta SQL               
        cursor.execute(sql, data)
        cnx.commit()
        mensaje = "Datos insertados correctamente"#si todo sale bien dira este mensaje       
        men = data[0]
        print(data)
    except mysql.connector.Error as error: #esto es para el error        # En caso de error, imprimir el mensaje de error       
            print("Error al insertar los datos:", error)
            mensaje = "Error al insertar los datos" # Cerrar el cursor y la conexión a la base de datos   
    cursor.close()
    cnx.close()# Retornar el mensaje de resultado a mostrar en la página HTML (dependiento de si es cliente (rol 1) o empleado (rol 3) redireccionara a otro html)   
    if mensaje== "Datos insertados correctamente" and data[17] == '3':
        return render_template('/habilidades.html', men=men)
    elif mensaje== "Datos insertados correctamente":
        return render_template('/OfertaEmpleo.html', men=men)
    else:
        return render_template('/resultado.html', mensaje=mensaje)


#Fin login---------------------------------------------------------------------------

#Perfiles---------------------------------------------------------------------------
@app.route('/perfilcliente', methods=['GET'])   
def perfilcliente():
    if 'nombres' in session:
        return render_template('perfilcliente.html', nombres=session['nombres'])
    return redirect(url_for('login'))

@app.route('/guardar_imagen', methods=['POST'])
def guardar_imagen():
    db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'Labor_Lane'
            }
    cnx = mysql.connector.connect(**db_config)
    if request.method == 'POST':
        if 'nombres' in session:
            id_usuario = session['nombres']
            if 'imagen' in request.files:
                imagen = request.files['imagen'].read()
                cursor = cnx.cursor() 
                sql = "UPDATE usuario SET imagen = %s WHERE id = %s"
                data = (imagen, id_usuario)
                cursor.execute(sql, data)        
                cnx.commit()
                cursor.close()
                return redirect(url_for('mostrar_imagen'))
    return redirect(url_for('login'))  # Redireccionar al login si no hay sesión



@app.route('/mostrar_imagen')
def mostrar_imagen():
    if 'nombres' in session:
        id_usuario = session['nombres']
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'Labor_Lane'
        }
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        sql = "SELECT imagen FROM usuario WHERE id = %s"
        cursor.execute(sql, (id_usuario,))
        imagen = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        cursor.close()
        cnx.close()
        if imagen:
            imagen_codificada = base64.b64encode(imagen[0]).decode('utf-8')
        else:
            imagen_codificada = None
        return render_template('perfilcliente.html', imagen=imagen_codificada)
    return redirect(url_for('login'))  # Redireccionar al login si no hay sesión


@app.route('/logout')
def logout():
    session.pop('nombres', None)
    return redirect(url_for('home'))

#Fin perfiles---------------------------------------------------------------------------




@app.route('/consultas')##CONSULTA GENERAL DE LOS EMPLEADOS/CLIENTES (2)------------------------------------
def mostrar_empleados(): # Establecer la conexión a la base de datos   
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor() # Consulta SQL para obtener los datos de todos los empleados   
    sql = "SELECT * FROM usuario"
    try: # Ejecutar la consulta SQL       
        cursor.execute(sql) # Obtener todos los registros       
        empleados = cursor.fetchall()
    except mysql.connector.Error as error: # En caso de error, imprimir el mensaje de error       
        print("Error al obtener los empleados:", error)
        empleados = []# Cerrar el cursor y la conexión a la base de datos   
    cursor.close()
    cnx.close() # Retornar los empleados a la plantilla HTML para mostrarlos   
    return render_template('/consultas.html', empleados=empleados)



@app.route('/eliminar/<int:id>')#Eliminar datos del formulario de empleo (el (1)) solo admin
def eliminar_empleados(id): # Establecer la conexión a la base de datos   
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor() # Eliminar SQL para obtener los datos de todos los empleados         # Ejecutar la consulta SQL 
    sql = "DELETE FROM usuario WHERE IdUsuario = %s"
    cursor.execute(sql, (id,))
    cnx.commit()
    cursor.close()
    cnx.close() # Retornar los empleados a la plantilla HTML para mostrarlos   
    return redirect('/consultas')



@app.route('/editar/<int:id>')#Actualizar datos del formulario de empleo (el (1)) solo admin
def editar(id):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    # Consulta SQL para obtener los datos de todos los empleados
    sql = "SELECT * FROM usuario WHERE IdUsuario = %s"
    try:
        # Ejecutar la consulta SQL
        cursor.execute(sql, (id,))
        # Obtener todos los registros
        empleados = cursor.fetchall()
        cnx.commit()
    except mysql.connector.Error as error:
        # En caso de error, imprimir el mensaje de error
        print("Error al obtener los empleados:", error)
        empleados = []
    return render_template('/modificar.html',empleados=empleados)



@app.route('/actualizar', methods=['POST'])
#Actualizar datos del formulario de empleo (el (1)) solo admin
def actualizar():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
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
    Estado = request.form['Estado']
    id=request.form['id']
    cursor = cnx.cursor()
        # # Actualizacion SQL para insertar los datos en la tabla "empleados"
    sql = "UPDATE usuario SET NombresUsuario=%s, PrimerApellidoUsuario=%s, SegundoApellidoUsuario=%s, GeneroUsuario=%s, TipoDocumentoUsuario=%s, NumeroDocumentoUsuario=%s, FechaNacimiento=%s, CelularUsuario=%s, Celular2Usuario=%s, DireccionUsuario=%s, EstratoResidencia=%s, CorreoUsuario=%s, ContraseñaUsuario=%s, EstadoCivil=%s, PersonasACargo=%s, Libreta=%s, contenido=%s, FK_IdRol=%s, ZonaResidencia=%s, Estado=%s WHERE IdUsuario=%s"
    # Parámetros de la consulta SQL   
    data = (nombres, p_apellido, s_apellido, genero, tipo_documento, numero_documento, fecha_nacimiento, celular_u, celular_d, direccion, estrato, correo, contraseña, estadocivil, personasacargo, LibretaMilitar, Contenido, rol, Barrio, Estado, id)
    cursor.execute(sql, data)
    cnx.commit()
    cursor.close()
    cnx.close() # Retornar los empleados a la plantilla HTML para mostrarlos   
    return redirect('/consultas') # Cerrar el cursor y la conexión a la base de datos

#---------------------------------



@app.route('/catalogo') # funcion desde flask
def catalogo(): #etiqueta para definir la funcion
    return render_template("catalogo.html")






@app.route('/tc') # funcion desde flask
def tc(): #etiqueta para definir la funcion
    return render_template ("t_c.html") #se redirecciona al archivo entre las comillas
#terminos y condiciones (juan pablo)









@app.route('/habilidad', methods=['POST'])#Habilidad de los empleados (datos)------------------------------------------------
def habilidad():
    Nombre = request.form['Nombre']
    nombre_h = request.form['nombre_h']
    Descripcion = request.form['Descripcion']
    Nivel = request.form['Nivel']
    categoria = request.form['categoria'] # Establecer la conexión a la base de datos   
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    sql = "select IdUsuario from usuario where NombresUsuario=%s"# Parámetros de SQL   
    data = (Nombre,)
    print (data)
    try:# intentar ejecutar la consulta con los datos (llenar los values de sql con data)                # Ejecutar la consulta SQL               
        cursor.execute(sql, data)
        resultado = cursor.fetchone()
        if resultado:
            usuario_id = resultado[0]
            s= "insert into habilidades(NombreHabilidad, DescipcionHabilidad, current_Nivel, FK_IdCategoria, FK_IdUsuario) values (%s, %s, %s, %s, %s)"
            dato= (nombre_h,Descripcion,Nivel,categoria, usuario_id)
            cursor.execute(s, dato)
        else:
            mensaje = "Usuario no encontrado"
            cnx.commit()
            mensaje = "correctamente"#si todo sale bien dira este mensaje   
    except mysql.connector.Error as error: #esto es para el error        # En caso de error, imprimir el mensaje de error       
        print("Error al insertar los datos:", error)
        mensaje = "Error al insertar"# Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        cnx.close()
        if mensaje == "correctamente":
            return render_template('/educacion.html', usuario_id=usuario_id)
    else:
        return render_template('/resultado.html', mensaje=mensaje)



@app.route('/Educacion', methods=['POST'])#Educacion de los empleados------------------------------------------------
def Educacion():
    NombreInstitucion = request.form['NombreInstitucion']
    TituloEducacion = request.form['TituloEducacion']
    NivelAcademico = request.form['NivelAcademico']
    FechaInicio = request.form['FechaInicio']
    Fechafinal = request.form['Fechafinal']
    ID = request.form['ID'] # Establecer la conexión a la base de datos
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    sql = "insert into educacion (NombreInstitucion, TituloEducacion, NivelAcademico, FechaInicio, FechaFin, FK_IdUsuario) values (%s,%s,%s,%s,%s,%s)"
    data = (NombreInstitucion, TituloEducacion, NivelAcademico, FechaInicio, Fechafinal, ID)
    print (data)
    try:# intentar ejecutar la consulta con los datos (llenar los values de sql con data)                # Ejecutar la consulta SQL             
        cursor.execute(sql, data)
        mensaje = "Datos insertados correctamente"#si todo sale bien dira este mensaje       
        print(data)
    except mysql.connector.Error as error: #esto es para el error        # En caso de error, imprimir el mensaje de error       
        print("Error al insertar los datos:", error)
        mensaje = "Error al insertar los datos"# Cerrar el cursor y la conexión a la base de datos   
        cursor.close()
        cnx.close() # Retornar el mensaje de resultado a mostrar en la página HTML (dependiento de si es cliente (rol 1) o empleado (rol 3) redireccionara a otro html)   
    if mensaje== "Datos insertados correctamente":
        return render_template('/experiencia.html', ID=ID)
    else:
        return render_template('/resultado.html', mensaje=mensaje)



@app.route('/Experiencia', methods=['POST'])#Experiencia de los empleados------------------------------------------------
def Experiencia():
    NombreEmpleador = request.form['NombreEmpleador']
    Cargo = request.form['Cargo']
    Funciones = request.form['Funciones']
    Logros = request.form['Logros']
    FechaInicio = request.form['FechaInicio']
    Fechafinal = request.form['Fechafinal']
    ID = request.form['ID'] # Establecer la conexión a la base de datos   
    cursor = cnx.cursor()
    sql = "insert into experiencia (NombreEmpleador, Cargo, Funciones, Logros, FechaInicio, FechaFin, FK_IdUsuario) values (%s,%s,%s,%s,%s,%s,%s)" # Parámetros de SQL   
    data = (NombreEmpleador, Cargo, Funciones, Logros, FechaInicio, Fechafinal, ID)
    print (data)
    try:# intentar ejecutar la consulta con los datos (llenar los values de sql con data) 
        # Ejecutar la consulta SQL     
        db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
        cnx = mysql.connector.connect(**db_config)          
        cursor.execute(sql, data)
        cnx.commit()
        mensaje = "Datos insertados correctamente"#si todo sale bien dira este mensaje       
        print(data)
    except mysql.connector.Error as error: #esto es para el error        # En caso de error, imprimir el mensaje de error       
        print("Error al insertar los datos:", error)
        mensaje = "Error al insertar los datos" # Cerrar el cursor y la conexión a la base de datos   
        cursor.close()
        cnx.close() # Retornar el mensaje de resultado a mostrar en la página HTML (dependiento de si es cliente (rol 1) o empleado (rol 3) redireccionara a otro html)   
        if mensaje== "Datos insertados correctamente":
            return render_template('/referencias.html', ID=ID)
        else:
            return render_template('/resultado.html', mensaje=mensaje)
    



@app.route('/Referencias', methods=['POST'])#Referencias de los empleados------------------------------------------------
def Referencias():
    NombreReferencia = request.form['NombreReferencia']
    EmpresaReferencia = request.form['EmpresaReferencia']
    CargoReferencia = request.form['CargoReferencia']
    CorreoReferencia = request.form['CorreoReferencia']
    CelularReferencia = request.form['CelularReferencia']
    ID = request.form['ID'] # Establecer la conexión a la base de datos   
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    sql = "insert into referencias (NombreReferencia, EmpresaReferencia, CargoReferencia, CorreoReferencia, CelularReferencia, FK_IdUsuario) values (%s,%s,%s,%s,%s,%s)" # Parámetros de SQL 
    data = (NombreReferencia, EmpresaReferencia, CargoReferencia, CorreoReferencia, CelularReferencia, ID)
    print (data)
    try:# intentar ejecutar la consulta con los datos (llenar los values de sql con data)                # Ejecutar la consulta SQL               
        cursor.execute(sql, data)
        cnx.commit()
        mensaje = "Datos insertados correctamente"#si todo sale bien dira este mensaje       
        print(data)
    except mysql.connector.Error as error: #esto es para el error        # En caso de error, imprimir el mensaje de error       
        print("Error al insertar los datos:", error)
        mensaje = "Error al insertar los datos" # Cerrar el cursor y la conexión a la base de datos   
        cursor.close()
        cnx.close() # Retornar el mensaje de resultado a mostrar en la página HTML (dependiento de si es cliente (rol 1) o empleado (rol 3) redireccionara a otro html)   
    if mensaje== "Datos insertados correctamente":
        return redirect('/consulta-ofertas',ID=ID)
    else:
        return render_template('resultado.html', mensaje=mensaje)
    


@app.route('/Oferta', methods=['POST'])#Ofetar para los empleados de clientes------------------------------------------------
def Oferta():
    Nombre = request.form['Nombre']
    TituloEmpleo = request.form['TituloEmpleo']
    DescripcionEmpleo = request.form['DescripcionEmpleo']
    RequisitosEmpleo = request.form['RequisitosEmpleo']
    HabilidadesEmpleo = request.form['HabilidadesEmpleo']
    FechaPublicacion = request.form['FechaPublicacion']
    FechaVencimiento = request.form['FechaVencimiento']
    Estado = 'ACTIVO'
    categoria = request.form['categoria']
    # Establecer la conexión a la base de datos 
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'Labor_Lane'
    }
    cnx = mysql.connector.connect(**db_config)  
    cursor = cnx.cursor()
    sql = "select IdUsuario from usuario where NombresUsuario=%s" # Parámetros de SQL   
    data = (Nombre,)
    print (data)
    try:# intentar ejecutar la consulta con los datos (llenar los values de sql con data)                # Ejecutar la consulta SQL               
        cursor.execute(sql, data)
        resultado = cursor.fetchone()
        if resultado:
            usuario_id = resultado[0]
            s= "insert into OfertaEmpleo (TituloEmpleo, DescripcionEmpleo, RequisitosEmpleo, HabilidadesEmpleo, FechaPublicacion, FechaVencimiento, current_Estado, FK_IdCategoria, FK_IdUsuario) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dato = (TituloEmpleo, DescripcionEmpleo, RequisitosEmpleo, HabilidadesEmpleo, FechaPublicacion, FechaVencimiento, Estado, categoria, usuario_id)
            cursor.execute(s, dato)
            mensaje = "correctamente"#si todo sale bien dira este mensaje
        else:
            mensaje = "Usuario no encontrado"
            cnx.commit()
    except mysql.connector.Error as error: #esto es para el error        # En caso de error, imprimir el mensaje de error
            print("Error al insertar los datos:", error)
            mensaje = "Error al insertar"
            # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    cnx.close()
    if mensaje == "correctamente":
        return render_template('botones.html', usuario_id=usuario_id)
    else:
        return render_template('resultado.html', mensaje=mensaje)
    



if __name__ == '__main__':
    app.run(debug=True)
    