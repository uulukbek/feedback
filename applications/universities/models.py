from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

REGION_NAME = (
    ('Bishkek', 'Bishkek'),
    ('Chuy', 'Chuy'),
    ('Osh', 'Osh'),
    ('Naryn', 'Naryn'),
    ('Talas', 'Talas'),
    ('Issyk Kul', 'Issyk Kul'),
    ('Jalal Abad', 'Jalal Abad'),
    ('Batken', 'Batken'),
)


class Faculty(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class University(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='universities')
    phone = models.BigIntegerField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=REGION_NAME)
    image = models.ImageField(upload_to='image/')
    faculties = models.ManyToManyField(Faculty, related_name='universities')

    def __str__(self) -> str:
        return self.name
