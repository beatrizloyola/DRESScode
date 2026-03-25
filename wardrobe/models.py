from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage

class Piece(models.Model):
    CATEGORY_CHOICES = [
        ('shirt', 'Parte de cima (Blusas, Camisas, Casacos)'),
        ('pants', 'Parte de baixo (Calças, Saias, Shorts)'),
        ('shoes', 'Sapatos e Calçados'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pieces/', storage=MediaCloudinaryStorage())
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else f"Peça ({self.category}) de {self.user.username}"
    
class Outfit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='outfits/')
    
    tags = models.CharField(max_length=200, blank=True, null=True, help_text="Separe as tags por vírgula")

    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

    def __str__(self):
        return self.name