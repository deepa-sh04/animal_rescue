# D:\project1\animal_rescue\pets\models.py

from django.db import models

class Pet(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('rescued', 'Rescued'),
    ]
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    age = models.IntegerField()
    image = models.ImageField(upload_to='pet_images/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name