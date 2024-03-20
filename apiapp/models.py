from django.db import models
from django.contrib.auth.models import User

class Nombre(User):
    class Meta:
        abstract = True

        

class Blog(models.Model):
    nombre = models.CharField(max_length=255)
    contenido_comentario = models.TextField()
    correo_electronico = models.EmailField(max_length=254, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    updated_at = models.DateTimeField(auto_now=True) # Nuevo campo

    class Meta:
        verbose_name_plural = "Blogs"
        ordering = ['-updated_at'] # Ordenar por fecha de actualización descendente


        

class Comentario(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    contenido_comentario = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Asegúrate de que este campo exista

    class Meta:
        verbose_name_plural = "Comentarios"