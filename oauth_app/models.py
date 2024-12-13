from django.db import models

class OAuthCredentials(models.Model):
    user_id = models.CharField(max_length=255)  # Almacena el ID único del usuario
    token = models.TextField()  # Credenciales en formato JSON
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de actualización
