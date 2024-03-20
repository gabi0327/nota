from django.shortcuts import render, redirect
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Blog
from django.contrib import messages
from .models import Blog , Comentario
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden











@login_required
def eliminar_comentario(request, comentario_id):
    # Intenta obtener el comentario por su ID
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verifica si el usuario autenticado es el mismo que creó el comentario
    if request.user != comentario.usuario:
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")
    
    # Si el usuario tiene permiso, elimina el comentario
    comentario.delete()
    return redirect('mostrar_comentarios', blog_id=comentario.blog.id)


def mostrar_comentarios(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comentarios = Comentario.objects.filter(blog=blog)
    return render(request, 'mostrar_comentarios.html', {'comentarios': comentarios})

def insertar_comentarios(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        contenido_comentario = request.POST['contenido_comentario']
        # Aquí asumimos que el usuario está autenticado y queremos usar el usuario actual
        Comentario.objects.create(blog=blog, contenido_comentario=contenido_comentario, usuario=request.user)
        return redirect('mostrar_comentarios', blog_id=blog_id)
    return render(request, 'insertar_comentarios.html', {'blog_id': blog_id})





@login_required
def eliminar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # Asegúrate de que el usuario autenticado es el propietario del blog antes de permitir la eliminación
    if request.user != blog.usuario:
        return HttpResponseForbidden("No tienes permiso para eliminar este blog.")
    
    # Elimina todos los comentarios relacionados al blog
    Comentario.objects.filter(blog=blog).delete()
    
    # Elimina el blog de la base de datos
    blog.delete()
    return redirect('elegir') # Redirige al usuario a la página 'elegir'















@login_required
def guardar_blog(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        contenido_comentario = request.POST['contenido_comentario']
        correo_electronico = request.POST['correo_electronico']
        
        # Verificar si el correo electrónico ya existe
        if Blog.objects.filter(correo_electronico=correo_electronico).exists():
            messages.error(request, 'El correo está en uso. Por favor, usa otro correo.')
            return render(request, 'blog.html', {})
        
        Blog.objects.create(nombre=nombre, contenido_comentario=contenido_comentario, correo_electronico=correo_electronico, usuario=request.user)
 
        return redirect('blog_registrados')
    else:
        return render(request, 'blog.html', {})
    



@login_required
def actualizar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    # Asegúrate de que el usuario autenticado es el propietario del blog antes de permitir la actualización
    if request.user != blog.usuario:
        return HttpResponseForbidden("No tienes permiso para actualizar este blog.")
    
    if request.method == 'POST':
        # Actualizar los campos del blog con los datos de la solicitud POST
        blog.nombre = request.POST['nombre']
        blog.contenido_comentario = request.POST['contenido_comentario']
        blog.correo_electronico = request.POST['correo_electronico']
        blog.save() # Guardar los cambios en la base de datos
        return HttpResponseRedirect(reverse('blog_registrados')) # Redirigir al usuario a la página de blogs registrados
    else:
        # Si no es una solicitud POST, renderiza el template con los datos del blog para la edición
        return render(request, 'actualizar_blog.html', {'blog': blog})



def blog(request):
    return render(request, 'blog.html')






@login_required
def blog_registrados(request):
    blogs = Blog.objects.all() # Obtiene todos los blogs
    return render(request, 'blog_registrados.html', {'blogs': blogs, 'user': request.user})




def elegir(request):
    return render(request, 'elegir.html')



def autenticarse(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Ahora puedes verificar si el usuario tiene blogs creados
            blogs_usuario = Blog.objects.filter(usuario=user)
            if blogs_usuario.exists():
                # Si el usuario tiene blogs, redirigir a 'blog_registrados'
                return HttpResponseRedirect(reverse('blog_registrados'))
            else:
                # Si el usuario no tiene blogs, redirigir a 'blog'
                return HttpResponseRedirect(reverse('blog'))
        else:
            # Mensaje de error si las credenciales no son válidas
            return render(request, 'autenticarse.html', {'error': 'Nombre de usuario o contraseña incorrectos'})
    return render(request, 'autenticarse.html')





def registarse(request):
    return render(request, 'registrarse.html')






class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return redirect(reverse('registarse') + '?error=Las contraseñas no coinciden')

        if User.objects.filter(username=username).exists():
            return redirect(reverse('registarse') + '?error=El nombre de usuario ya existe. Por favor, ingrese otro nombre.')

        User.objects.create_user(username=username, password=password)
        return redirect('elegir')