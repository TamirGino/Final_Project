from django.db import models
from django.contrib.auth.models import User


class FemalePants(models.Model):
    id = models.BigAutoField(primary_key=True)
    weight = models.IntegerField()
    age = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.CharField(max_length=5)
    gender = models.CharField(max_length=5)
    tummy_shape = models.CharField(max_length=20)
    fit_preference = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    waist_lower = models.IntegerField()
    waist_top = models.IntegerField()



    def __str__(self):
        return str(self.id)

class FemaleShirts(models.Model):
    id = models.BigAutoField(primary_key=True)
    weight = models.IntegerField()
    age = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.CharField(max_length=5)
    gender = models.CharField(max_length=5)
    tummy_shape = models.CharField(max_length=20)
    fit_preference = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    chest_lower = models.IntegerField()
    chest_top = models.IntegerField()



    def __str__(self):
        return str(self.id)

class MalePants(models.Model):
    id = models.BigAutoField(primary_key=True)
    weight = models.IntegerField()
    age = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.CharField(max_length=5)
    gender = models.CharField(max_length=5)
    tummy_shape = models.CharField(max_length=20)
    fit_preference = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    waist_lower = models.IntegerField()
    waist_top = models.IntegerField()



    def __str__(self):
        return str(self.id)

class MaleShirts(models.Model):
    id = models.BigAutoField(primary_key=True)
    weight = models.IntegerField()
    age = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    size = models.CharField(max_length=5)
    gender = models.CharField(max_length=5)
    tummy_shape = models.CharField(max_length=20)
    fit_preference = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    chest_lower = models.IntegerField()
    chest_top = models.IntegerField()


    def __str__(self):
        return str(self.id)

class UsersInput(models.Model):
    #user_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.IntegerField()
    tummy_shape = models.CharField(max_length=20)
    fit_preference = models.CharField(max_length=20)
    item = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    size = models.CharField(max_length=5)


    def __str__(self):
        return str(self.user_name)

class NormTable(models.Model):
   id = models.BigAutoField(primary_key=True)
   cluster = models.IntegerField(null=True)
   gender = models.CharField(max_length=5)
   item = models.CharField(max_length=20)
   weight = models.FloatField()
   age = models.FloatField()
   height = models.FloatField()
   chest_lower = models.FloatField()
   chest_top = models.FloatField()
   waist_lower = models.FloatField()
   waist_top = models.FloatField()
   brand_ASOS = models.FloatField()
   brand_HM = models.FloatField()
   brand_PULL_BEAR = models.FloatField()
   brand_ZARA = models.FloatField()
   size_labels = models.FloatField()
   fit_labels = models.FloatField()
   tummy_labels = models.FloatField()

   def __str__(self):
       return str(self.id)

class StdTable(models.Model):
   gender = models.CharField(max_length=5)
   item = models.CharField(max_length=20)
   cluster = models.IntegerField(null=True)
   weight = models.FloatField()
   age = models.FloatField()
   height = models.FloatField()

   def __str__(self):
       return str(self.gender)

class Brand(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return str(self.name)

class Item(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return str(self.name)

class Size(models.Model):
    name = models.CharField(max_length=5, primary_key=True)

    def __str__(self):
        return str(self.name)

class Size_by_brand(models.Model):
    brand_name = models.ForeignKey(Brand, on_delete = models.CASCADE)
    item_name = models.ForeignKey(Item, on_delete = models.CASCADE)
    size_name = models.ForeignKey(Size, on_delete = models.CASCADE)
    chest = models.CharField(max_length=20)
    waist = models.CharField(max_length=20)

    def __str__(self):
        return str(self.brand_name)
