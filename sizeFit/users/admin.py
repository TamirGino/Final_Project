from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from .models import FemalePants, FemaleShirts, MalePants, MaleShirts
from .models import UsersInput, NormTable, StdTable
from .models import Brand, Item, Size, Size_by_brand
import pandas as pd
import numpy as np
from .func import *


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class Size_by_brandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'item_name', 'size_name', 'chest', 'waist')

class StdTableAdmin(admin.ModelAdmin):
    list_display = ('gender', 'item', 'cluster')

class NormTableAdmin(admin.ModelAdmin):
    list_display = ('gender', 'item')


    def get_urls(self):
        urls = super().get_urls() #existing urls
        new_urls = [path('norm-tbl/', self.norm)]#, ('norm-tbl/', self.upload_csv)] #when go to 'upload-csv' activate func upload_csv
        return new_urls + urls # add the new url to the existing ones

    def norm(self, request):
        insert_into_norm(FemalePants, 'female', 'pants')
        insert_into_norm(FemaleShirts, 'female', 't-shirt')
        insert_into_norm(MalePants, 'male', 'pants')
        insert_into_norm(MaleShirts, 'male', 't-shirt')
        return render(request, "admin/k_means.html" )




class FemalePantsAdmin(admin.ModelAdmin):
    #list_display = ('name', 'balance')

    def get_urls(self):
        urls = super().get_urls() #existing urls
        new_urls = [path('upload-csv/', self.upload_csv),]#, ('norm-tbl/', self.upload_csv)] #when go to 'upload-csv' activate func upload_csv
        return new_urls + urls # add the new url to the existing ones


    def upload_csv(self, request):


        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data[1::]:
                fields = x.split(",")
                created = FemalePants.objects.update_or_create(
                    id = fields[0],
                    weight = fields[1],
                    age = fields[2],
                    height = fields[3],
                    size = fields[4],
                    gender = fields[5],
                    tummy_shape = fields[6],
                    fit_preference = fields[7],
                    brand = fields[8],
                    waist_lower = fields[9],
                    waist_top = fields[10],
                )



        form = CsvImportForm()
        data = {"form": form}

        return render(request, "admin/csv_upload.html", data)


class FemaleShirtsAdmin(admin.ModelAdmin):
    #list_display = ('name', 'balance')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data[1::]:
                fields = x.split(",")
                created = FemaleShirts.objects.update_or_create(
                    id = fields[0],
                    weight = fields[1],
                    age = fields[2],
                    height = fields[3],
                    size = fields[4],
                    gender = fields[5],
                    tummy_shape = fields[6],
                    fit_preference = fields[7],
                    brand = fields[8],
                    chest_lower = fields[9],
                    chest_top = fields[10],
                )



        form = CsvImportForm()
        data = {"form": form}

        return render(request, "admin/csv_upload.html", data)

class MalePantsAdmin(admin.ModelAdmin):
    #list_display = ('name', 'balance')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data[1::]:
                fields = x.split(",")
                created = MalePants.objects.update_or_create(
                    id = fields[0],
                    weight = fields[1],
                    age = fields[2],
                    height = fields[3],
                    size = fields[4],
                    gender = fields[5],
                    tummy_shape = fields[6],
                    fit_preference = fields[7],
                    brand = fields[8],
                    waist_lower = fields[9],
                    waist_top = fields[10],
                )



        form = CsvImportForm()
        data = {"form": form}

        return render(request, "admin/csv_upload.html", data)

class MaleShirtsAdmin(admin.ModelAdmin):
    #list_display = ('name', 'balance')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data[1::]:
                fields = x.split(",")
                created = MaleShirts.objects.update_or_create(
                    id = fields[0],
                    weight = fields[1],
                    age = fields[2],
                    height = fields[3],
                    size = fields[4],
                    gender = fields[5],
                    tummy_shape = fields[6],
                    fit_preference = fields[7],
                    brand = fields[8],
                    chest_lower = fields[9],
                    chest_top = fields[10],
                )



        form = CsvImportForm()
        data = {"form": form}

        return render(request, "admin/csv_upload.html", data)


# Register your models here.
admin.site.register(FemalePants, FemalePantsAdmin)
admin.site.register(FemaleShirts, FemaleShirtsAdmin)
admin.site.register(MalePants, MalePantsAdmin)
admin.site.register(MaleShirts, MaleShirtsAdmin)
admin.site.register(UsersInput)
admin.site.register(NormTable, NormTableAdmin)
admin.site.register(StdTable, StdTableAdmin)
admin.site.register(Size)
admin.site.register(Item)
admin.site.register(Brand)
admin.site.register(Size_by_brand, Size_by_brandAdmin)
