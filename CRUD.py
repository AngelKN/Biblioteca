from db import obtener_conexion

def getCategorias():
    con = obtener_conexion()
    cursor = con.cursor()
    sql2 = "SELECT * FROM `categorias`"
    cursor.execute(sql2)
    cat = cursor.fetchall()
    con.commit()
    con.close()
    return cat

def getLibros():
    con = obtener_conexion()
    cursor = con.cursor()
    sql1 = "SELECT * FROM `libros`"
    cursor.execute(sql1)
    libros = cursor.fetchall()
    con.commit()
    con.close()
    return libros

def getLibro(nombre):
    con = obtener_conexion()
    cursor = con.cursor()
    sql1 = "SELECT id FROM `libros` WHERE `libros`.`nombre` = '{}'".format(nombre)
    cursor.execute(sql1)
    libro = cursor.fetchall()
    con.commit()
    con.close()

    lib = ""

    for libro in libro:
        lib = libro[0]

    return lib

def getVolumenes():
    con = obtener_conexion()
    cursor = con.cursor()
    sql1 = "SELECT * FROM `volumenes`"
    cursor.execute(sql1)
    vols = cursor.fetchall()
    con.commit()
    con.close()
    return vols

def getVolumen(idlib):
    con = obtener_conexion()
    cursor = con.cursor()
    sql1 = "SELECT * FROM `volumenes` WHERE `volumenes`.`idlibro` = '{}'".format(idlib)
    cursor.execute(sql1)
    vols = cursor.fetchall()
    con.commit()
    con.close()
    return vols

def postLibros(nombre, nuevoNombre):
    con = obtener_conexion()
    cursor = con.cursor()
    sql = "INSERT INTO libros (id, nombre, imagen) VALUES (NULL, '{}', '{}');"
    cursor.execute(sql.format(nombre, nuevoNombre))
    con.commit()
    con.close()

def postVolumenes(vol, nuevoNombre, url, idnombre):
    con = obtener_conexion()
    cursor = con.cursor()
    sql = "INSERT INTO `volumenes` (`id`, `volumen`, `imagen`, `url`, `idlibro`) VALUES (NULL, '{}', '{}', '{}', '{}');".format( vol, nuevoNombre, url, idnombre)
    cursor.execute(sql)
    con.commit()
    con.close()

def postLibCat(nombreL, cartegorias):

    if cartegorias:

        con = obtener_conexion()
        cursor = con.cursor()

        sql = "SELECT id FROM `libros` WHERE `libros`.`nombre` = '{}'".format(nombreL)
        cursor.execute(sql)
        idlibro = cursor.fetchall()

        idlib = ""
        for idlibro in idlibro:
            idlib = idlibro[0]
            sql = "SELECT id FROM `categorias` WHERE `categorias`.`categoria` = '{}'".format(cartegorias)
            cursor.execute(sql)
            idcategoria = cursor.fetchall()

        idcat = ""
        for idcategoria in idcategoria:
            idcat = idcategoria[0]

        idlib = str(idlib)
        idcat = str(idcat)

        sql = "INSERT INTO lib_cat (id, idlibro, idcategoria) VALUES (NULL, {}, {});".format(idlib, idcat)
        cursor.execute(sql)

        con.commit()
        con.close()

def getImgLib(idlibro):
    con = obtener_conexion()
    cursor = con.cursor()
    sql1 = "SELECT imagen FROM `libros` WHERE `libros`.`id` = {}".format(idlibro)
    cursor.execute(sql1)
    img = cursor.fetchall()
    con.commit()
    con.close()
    return img

def getImgLibVol(idlibro):
    con = obtener_conexion()
    cursor = con.cursor()
    sql3 = "SELECT id, imagen FROM `volumenes` WHERE `volumenes`.`idlibro` = {}".format(idlibro)
    cursor.execute(sql3)
    vols = cursor.fetchall()
    con.commit()
    con.close()
    return vols

def getImgVol(idvol):
    con = obtener_conexion()
    cursor = con.cursor()
    sql3 = "SELECT imagen FROM `volumenes` WHERE `volumenes`.`id` = {}".format(idvol)
    cursor.execute(sql3)
    vol = cursor.fetchall()
    con.commit()
    con.close()
    return vol
    
def deleteLibro(idlibro):
    con = obtener_conexion()
    cursor = con.cursor()
    sql2 = "DELETE FROM `libros` WHERE `libros`.`id` = {};".format(idlibro)
    cursor.execute(sql2)
    con.commit()
    con.close()

def deleteVol(idvol):
    con = obtener_conexion()
    cursor = con.cursor()
    sql4 = "DELETE FROM `volumenes` WHERE `volumenes`.`id` = {};".format(idvol)
    cursor.execute(sql4)
    con.commit()
    con.close()

def deleteLibCat(idlibro):
    con = obtener_conexion()
    cursor = con.cursor()
    sql4 = "DELETE FROM `lib_cat` WHERE `lib_cat`.`idlibro` = {};".format(idlibro)
    cursor.execute(sql4)
    con.commit()
    con.close()

def buscador(categoria):
    con = obtener_conexion()
    cursor = con.cursor()
    idcat = []
    ids1 = []
    ids2 = []
    libs = []

    for categoria in categoria:
        sql = "SELECT id FROM `categorias` WHERE `categorias`.`categoria` = '{}'".format(categoria)
        cursor.execute(sql)
        categoria = cursor.fetchall()
        
        for categoria in categoria:
            idcat.append(categoria[0])
        
    for idcat in idcat:
        sql = "SELECT idlibro FROM `lib_cat` WHERE `lib_cat`.`idcategoria` = {}".format(idcat)
        cursor.execute(sql)
        
        ids = cursor.fetchall()
        ids1 = []

        for ids in ids:
            ids1.append(ids[0])
            
        if not ids1:
            ids2 = []
            break
        else:
            if not ids2:
                ids2 = ids1[:]
            else:
                if ids1 == ids2:
                    ids1 = ids2
                else: 
                    for elemento in ids2:
                        if elemento not in ids1:
                            ids2.remove(elemento)
    
    if ids2:
        for ids2 in ids2:
            sql = "SELECT * FROM `libros` WHERE `libros`.`id` = {}".format(ids2)
            cursor.execute(sql)
            libros1 = cursor.fetchall()
            for libro1 in libros1:
                libs.append(libro1)

    con.commit()
    con.close()

    return libs