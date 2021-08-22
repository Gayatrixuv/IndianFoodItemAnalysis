from django.db import models

# Create your models here.

class Graphs(models.Model):
    Name    = models.CharField(max_length=100,default=None,null=True,blank=True)
    Image   = models.ImageField(upload_to='Graphs')
    Description = models.TextField()

    def __str__(self):
        return self.Name

DietChoices=(
        ('vegetarian','vegetarian'),
         ('non vegetarian','non vegetarian')
         )

# Create your models here.
class Data(models.Model):
     Name           =   models.CharField(max_length=20)
     Ingredient     =   models.CharField(max_length=300)
     Diet           =   models.CharField(max_length=20,choices=DietChoices)
     PrepTime       =   models.IntegerField()
     CookTime       =   models.IntegerField()
     Flavor         =    models.CharField(max_length=20)
     Course         =    models.CharField(max_length=20)
     State          =   models.CharField(max_length=20)
     Region         =   models.CharField(max_length=30)