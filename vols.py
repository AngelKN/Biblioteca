from flask import render_template, request, redirect, session
from datetime import datetime
import os.path
import db
import CRUD

def init_views(app):

    @app.route('/vols', methods = ['GET','POST'])
    def vols():

        id = ""

        if request.method == 'POST':
            id = request.form['idlibro']
            vols = CRUD.getVolumen(id)
        else:
            vols = CRUD.getVolumenes()

        return render_template('sitio/vols.html', vols = vols)
    
    @app.route('/admin/vols')
    def admin_vols():

        if not 'login' in session:
            return redirect("/admin/login")
        
        libros = CRUD.getLibros()
        vols = CRUD.getVolumenes()

        return render_template('admin/vols.html', libros = libros, vols = vols)
    
    @app.route('/admin/vols/guardar', methods = ['POST'])
    def admin_vols_guardar():

        if not 'login' in session:
            return redirect("/admin/login")
        
        nombre = request.form.get('txtNombre')
        file = request.files['txtImagen']
        vol = nombre+" "+request.form['txtVol']
        url = request.form['txtUrl']

        tiempo = datetime.now()
        horaActual = tiempo.strftime('%Y%H%M%S')

        if file.filename != "":
            nuevoNombre = horaActual+"_"+file.filename
            file.save("templates/img/"+nuevoNombre)
            db.PostImgDrive(nuevoNombre)
        
        os.unlink("templates/img/"+nuevoNombre)

        idimg = db.getImg(nuevoNombre)

        idlibro = ""

        if nombre:
            idlibro = CRUD.getLibro(nombre)

        CRUD.postVolumenes(vol, idimg, url, idlibro)
        print(idimg)

        return redirect('/admin/vols')

    @app.route('/admin/vols/borrar', methods=['POST'])
    def admin_vols_borrar():

        if not 'login' in session:
            return redirect("/admin/login")
        
        id = request.form['txtId']

        img = CRUD.getImgVol(id)

        if img:
            db.deleteImg(img[0][0])

        CRUD.deleteVol(id)

        return redirect('/admin/vols')
