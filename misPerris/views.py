
from django.shortcuts import render
# importamos la tabla
from .models import Categoria, Mascota, Galeria

# importar la tabla USER (Usuarios) desde el administrador
from django.contrib.auth.models import User
# importar las librerias de validacio  de login
from django.contrib.auth import authenticate, logout, login as login_aut
# agregar la libreria de 'decoradores' (limitar el ingreso)
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
@login_required(login_url='/login/')
def devolver(request,id):
    mensaje=""
    try:
        mas = Mascota.objects.filter(publicar=False).get(nombre=id)
        mas.dueno='--'
        mas.comentario ='--'
        mas.save()
        mensaje="Mascota devuelta"
    except:
        mensaje="No pudo devolver mascota"

    mascotas = Mascota.objects.filter(dueno=request.user.username)
    datos = {"mascotas":mascotas,"mensaje":mensaje}
    return render(request,"admin_usuario.html",datos)
   

@login_required(login_url='/login/')
def admin_usuario(request):
    mascotas = Mascota.objects.filter(dueno=request.user.username)
    datos = {"mascotas":mascotas}
    return render(request,"admin_usuario.html",datos)

@login_required(login_url='/login/')
def adoptar(request,id):
    try:
        mas = Mascota.objects.filter(publicar=True).get(nombre= id)
        mas.dueno = request.user.username
        mas.publicar = False
        mas.comentario = "Adoptada"
        mas.save()
        mensaje = "Adoptada"
    except:
        mensaje="Mascota no ubicada"

    mascota = Mascota.objects.get(nombre=id)
    datos = {"mascota":mascota}
    galeria = Galeria.objects.filter(mascota= mascota)
    datos["galeria"]= galeria
    datos["mensaje"]= mensaje
    return render(request,"ficha.html",datos)
    
def crear_usuario(request):
    mensaje=''
    if request.POST:
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        email = request.POST.get("txtEmail")
        usuario = request.POST.get("txtUsuario")
        pass1 = request.POST.get("txtPass1")

        try:
            usu = User()
            usu.first_name = nombre
            usu.last_name = apellido
            usu.email = email
            usu.username = usuario
            usu.set_password(pass1)

            usu.save()
            mensaje =" usuario almacenado"
        except:
            mensaje =" no pudo almacenar el usuario"
            
    datos = {"mensaje":mensaje}        
    return render(request,"crear_usuario.html",datos)

def cerrar_sesion(request):
    logout(request)
    categorias = Categoria.objects.all()
    datos = {"categorias":categorias}
    return render(request, "index.html",datos)

def login(request):
    mensaje=''
    if request.POST:
        usuario = request.POST.get("txtUsuario")
        contra = request.POST.get("txtPass")
        us = authenticate(request,username=usuario,password=contra)
        if us is not None and us.is_active:
            login_aut(request,us)
            # ir al index
            categorias = Categoria.objects.all()
            datos = {"categorias":categorias}
            return render(request, "index.html",datos)
        else:
            mensaje="usuario o contraseña incorrecta"

    datos = {"mensaje":mensaje}
    return render(request,"login.html",datos)

def filtro_nombre(request):
    mascotas = Mascota.objects.all()
    cant = Mascota.objects.all().count()
    if request.POST:
        nombre = request.POST.get("txtNombre")
        # el metodo 'filter' permite generar el filtro de los objetos WHERE
        mascotas = Mascota.objects.filter(nombre=nombre).filter(publicar=True)
        # el metodo 'count' efectua el conteo de los registros recuperados por
        # la condicion
        cant = Mascota.objects.filter(nombre=nombre).filter(publicar=True).count()

    categorias = Categoria.objects.all()
    datos = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",datos)

def filtro_pd(request):
    mascotas = Mascota.objects.all()
    cant = Mascota.objects.all().count()
    if request.POST:
        desc = request.POST.get("txtDesc")
        # agregando '__contains' efectuo in LIKE sobre el campo
        mascotas = Mascota.objects.filter(descripcion__contains=desc).filter(publicar=True) # like ''
        cant = Mascota.objects.filter(descripcion__contains=desc).filter(publicar=True).count()

    categorias = Categoria.objects.all()
    datos = {"mascotas":mascotas,"categorias":categorias}
    return render(request, "galeria.html",datos)

def filtro_categoria(request):
    mascotas = Mascota.objects.all()
    cant = Mascota.objects.all().count()
    if request.POST:
        cate = request.POST.get("cboCategoria")
        # buscar el objeto asociado al campo clave
        obj_cate = Categoria.objects.get(nombre=cate)
        # filtramos por dicha entidad encontrada
        mascotas = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True)
        cant = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True).count()

    categorias = Categoria.objects.all()
    datos = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",datos)

def filtro_cate(request,id):
    # buscar el objeto asociado al campo clave
    obj_cate = Categoria.objects.get(nombre=id)
    # filtramos por dicha entidad encontrada
    mascotas = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True)
    cant = Mascota.objects.filter(categoria=obj_cate).filter(publicar=True).count()

    categorias = Categoria.objects.all()
    datos = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",datos)

def ficha(request, id):
    mascota = Mascota.objects.filter(publicar=True).get(nombre=id)
    datos = {"mascota":mascota}
    galeria = Galeria.objects.filter(mascota= mascota)
    datos["galeria"]= galeria
    return render(request,"ficha.html",datos)

def index(request):
    categorias = Categoria.objects.all()
    mascotas = Mascota.objects.filter(publicar=True).order_by('-nombre')[:3]
    datos = {"categorias":categorias,"mascotas":mascotas}
    return render(request, "index.html",datos)

def galeria(request):
    mascotas = Mascota.objects.filter(publicar=True)
    cant = Mascota.objects.filter(publicar=True).count()
    categorias = Categoria.objects.all()
    datos = {"mascotas":mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria.html",datos)

def formulario(request):
    return render(request, "formulario.html")

def quienes(request):
    return render(request, "quienes_somos.html")

@login_required(login_url='/login/')
@permission_required('misPerris.add_mascota',login_url='/login/')
@permission_required('misPerris.view_mascota',login_url='/login/')
def registro(request):
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        imagen = request.FILES.get("txtImg")
        cate = request.POST.get("cboCategoria") # nombres: Perro, Gato, Pajaro
        obj_cate = Categoria.objects.get(nombre=cate) # buscando el objeto categoria
        mas = Mascota()
        mas.nombre = nombre
        mas.edad = edad
        mas.descripcion = desc
        mas.categoria = obj_cate
        mas.usuario = request.user.username
        if imagen is not None:
            mas.imagen = imagen
        
        mas.save()
        mensaje="Grabo"

    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.filter(usuario=request.user.username)
    cantidad = Mascota.objects.filter(usuario=request.user.username).count()
    datos = {"cate":categorias,"mensaje":mensaje,"mascotas":mascotas,"cant":cantidad}
    return render(request,"registro.html",datos)

@login_required(login_url='/login/')
@permission_required('misPerris.delete_mascota',login_url='/login/')
def eliminar(request,id):
    mensaje=""
    try:
        mas = Mascota.objects.get(nombre=id)
        mas.delete()
        mensaje = "Mascota Eliminada"
    except:
        mensaje = "No Existe la Mascota"

    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.filter(usuario=request.user.username)
    datos = {"cate":categorias,"mensaje":mensaje,"mascotas":mascotas}
    return render(request,"registro.html",datos)

@login_required(login_url='/login/')
@permission_required('misPerris.view_mascota',login_url='/login/')
def buscar_modificar(request,id):
    mensaje=""
    try:
        mas = Mascota.objects.get(nombre=id)
        categorias = Categoria.objects.all() # select * from Categoria
        datos = {"cate":categorias,"mascota":mas}
        return render(request,"modificar.html",datos)
    except:
        mensaje="No existe mascota"
    
    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.filter(usuario=request.user.username)
    datos = {"cate":categorias,"mensaje":mensaje,"mascotas":mascotas}
    return render(request,"registro.html",datos)

@login_required(login_url='/login/')
@permission_required('misPerris.change_mascota',login_url='/login/')
def modificar(request):
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        imagen = request.FILES.get("txtImg")
        cate = request.POST.get("cboCategoria")

        obj_cate = Categoria.objects.get(nombre=cate)

        try:
            mas = Mascota.objects.get(nombre=nombre)
            mas.edad = edad
            mas.descripcion = desc
            mas.categoria = obj_cate
            mas.comentario = '--'
            if imagen is not None:
                mas.imagen = imagen
            mas.save()
            mensaje = "Modifico mascota "+nombre
        except:
            mensaje = "No Modifico mascota"
    
    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.filter(usuario=request.user.username)
    datos = {"cate":categorias,"mensaje":mensaje,"mascotas":mascotas}
    return render(request,"registro.html",datos)

@login_required(login_url='/login/')
@permission_required('misPerris.add_galeria',login_url='/login/')
def agregar_imagen_galeria(request):
    mensaje=""
    if request.POST:
        nombre_mascota = request.POST.get("txtMascota")
        imagen = request.FILES.get("txtImg")
        obj_mascota = Mascota.objects.get(nombre= nombre_mascota)

        gale = Galeria()
        gale.imagen = imagen
        gale.mascota = obj_mascota
        gale.save()
        mensaje = "Agrego Imagen a Mascota "+nombre_mascota

    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.filter(usuario=request.user.username)
    datos = {"cate":categorias,"mensaje":mensaje,"mascotas":mascotas}
    return render(request,"registro.html",datos)
    