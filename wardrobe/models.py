from django.db import models
from django.contrib.auth.models import User

class Piece(models.Model):
    CATEGORY_CHOICES = [
        ('shirt', 'Parte de Cima'),
        ('pants', 'Parte de Baixo'),
        ('shoes', 'Sapatos'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='pieces/') # Para salvar a imagem
    created_at = models.DateTimeField(auto_now_add=True)

class Outfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pieces = models.ManyToManyField(Piece) # Um look tem várias peças
    created_at = models.DateTimeField(auto_now_add=True)