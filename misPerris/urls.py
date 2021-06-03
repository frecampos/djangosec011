from django.contrib import admin
from django.urls import path
# importar los controladores "views" desde archivo views.py
from .views import devolver,admin_usuario, adoptar, agregar_imagen_galeria, modificar,buscar_modificar, eliminar, crear_usuario, cerrar_sesion,login, filtro_cate,filtro_nombre,filtro_pd,filtro_categoria, ficha,index, galeria, formulario, quienes,registro

urlpatterns = [
    path('',index,name='IND'),
    path('galeria/',galeria,name='GALE'),
    path('formulario/',formulario, name='FORMU'),
    path('quienes/',quienes,name='QUIENES'),
    path('registro/',registro,name='REG'),
    path('ficha/<id>/',ficha,name='FICHA'),
    path('filtro_categoria/',filtro_categoria,name='FILTROC'),
    path('filtro_descripcion',filtro_pd,name='FILTROPC'),
    path('filtro_nombre/',filtro_nombre,name='FILTRON'),
    path('filtro_cate/<id>/',filtro_cate,name='FILTROCATE'),
    path('login/',login,name='LOGIN'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRAR'),
    path('crear_usuario/',crear_usuario,name='CREARU'),
    path('eliminar/<id>/',eliminar,name='ELIMINAR'),
    path('buscar_modificar/<id>/',buscar_modificar,name='BUSCARM'),
    path('modificar/',modificar,name='MODIFICAR'),
    path('agregar_imagen/',agregar_imagen_galeria,name='AGREGARIMG'),
    path('adoptar/<id>/',adoptar,name='ADOPTAR'),
    path('admin_usuario/',admin_usuario,name='ADMINUSER'),
    path('devolver/<id>/',devolver,name='DEVOLVER'),
]

# {% url '<nombre>' %}