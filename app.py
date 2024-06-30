from flask import Flask
from flask import render_template, request, redirect, session
from flask_mysqldb import MySQL
from datetime import datetime
from flask import send_from_directory
import os.path
import vols
import db
import CRUD

app = Flask(__name__)
app.secret_key = "develoteca"

@app.route('/drive')
def drive():
    
    #db.PostImgDrive()
    db.getImg()

    return redirect('/admin/libros')

vols.init_views(app)
    
@app.route('/')
def inicio():
    return redirect('/libros')

@app.route('/img/<imagen>')
def imagenes(imagen):
    return send_from_directory(os.path.join('templates/img'),imagen)

@app.route("/css/<archivocss>")
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/css'),archivocss)

@app.route('/libros', methods = ['GET','POST'])
def libros():
    
    if request.method == 'POST':
        filtros = []

        filtros = request.form.getlist('filtros')[0].split(',')

        libros = []

        libros = CRUD.buscador(filtros)
    else:
        libros = CRUD.getLibros()

    categorias = CRUD.getCategorias()

    return render_template('sitio/libros.html', libros = libros, categorias = categorias)

@app.route('/admin/login')
def login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods = ['POST'])
def admin_login_post():

    usuario = request.form['txtUsuario']
    password = request.form['txtContraseña']

    if usuario == "admin" and password == "123":
        session["login"] = True
        session["usuario"] = "Administrador"
        return redirect("/admin/libros")

    return render_template('admin/login.html', mensaje = "Acceso denegado")

@app.route('/admin/cerrar')
def admin_login_cerrar():

    session.clear()
    return redirect('/admin/login')

@app.route('/admin/')
def admin_index():

    if not 'login' in session:
        return redirect("/admin/login")
    
    return render_template('admin/libros.html')

@app.route('/admin/libros')
def admin_libros():

    if not 'login' in session:
        return redirect("/admin/login")
    
    libros = CRUD.getLibros()
    categorias = CRUD.getCategorias()  
    
    return render_template('admin/libros.html', libros = libros, categorias = categorias)

@app.route('/admin/libros/guardar', methods = ['POST'])
def admin_libros_guardar():

    if not 'login' in session:
        return redirect("/admin/login")
    
    nombre = request.form['txtNombre']
    file = request.files['txtImagen']
    nuevoNombre = ""
    filtros = request.form.getlist('filtros')[0].split(',')

    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')

    val = False

    for fil in filtros:
        if fil:
            val = True
        else:
            val = False

    if val:
        if file.filename != "":
            nuevoNombre = horaActual+"_"+file.filename
            file.save("templates/img/"+nuevoNombre)
            db.PostImgDrive(nuevoNombre)

        os.unlink("templates/img/"+nuevoNombre)

        id = db.getImg(nuevoNombre)
    
        CRUD.postLibros(nombre, id)

        for fil in filtros:
            CRUD.postLibCat(nombre, fil)

    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():

    if not 'login' in session:
        return redirect("/admin/login")
    
    id = request.form['txtId']

    img = CRUD.getImgLib(id)

    print(img)

    if img:
        db.deleteImg(img[0][0])
    
    CRUD.deleteLibCat(id)

    CRUD.deleteLibro(id)

    vols = CRUD.getImgLibVol(id)

    for vol in vols:

        if img:
            db.deleteImg(vol[1])

        CRUD.deleteVol(vol[0])

    return redirect('/admin/libros')

if __name__ == '__main__':
    app.run(debug=True)