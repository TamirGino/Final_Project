from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import UsersInput
from .func import *
from .scrapping import *


#background: url("/static/users/media/fashion_bar.jpg");
# Create your views here.

def test(request):
    data = UsersInput.objects.all()
    print(data)

def home(request):
    return render(request,"users/home.html")

def form(request):
    return render(request,"users/form.html")

def url_input(request):
    return render(request,"users/url_input.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class Form(TemplateView):
    template_name = "form.html"

def url_is_valid(request):
    url = request.POST["url"]
    help_dict = {'url' : url}
    is_url_correct = validate_url(url)
    if is_url_correct == "No URL specified":
        messages.error(request, "Please fill in the URL input")
        return redirect('url_input')
    if is_url_correct == "Invalid URL!":
        messages.error(request, "Invalid URL! \nPlease put a correct URL address")
        return redirect('url_input')
    if is_url_correct == "No size guide":
        messages.error(request, "This URL has no size guide!")
        return redirect('url_input')

    return render(request, "users/form.html", context = help_dict )






def add_user(request):
    url = request.POST["url"]
    user_name = request.POST["user_name"]
    gender = request.POST["gender"]
    age = request.POST["age"]
    height = request.POST["height"]
    weight = request.POST["weight"]
    tummy_shape = request.POST["tummy_shape"]
    fit_preference = request.POST["fit_preference"]
    item = request.POST["item"]
    brand = request.POST["brand"]
    size = request.POST["size"]

    user_in_process = {"weight": weight, "age": age, "height": height, "size": size, "gender": gender, "tummy_shape": tummy_shape ,"fit_preference": fit_preference, "item": item, "brand": brand}
    recommended_size = Find_My_Size(user_in_process, url)
    if not recommended_size:
        return render(request, "users/size_output.html", context = help_dict )
    size_list = []
    print(recommended_size)
    print("-----")
    for size in recommended_size:
        size_list.append(size)
        size_list.append(recommended_size[size])
    print(size_list)
    size1 = size_list[0]
    size_percentage1 = size_list[1]
    if len(size_list) == 4:
        size2 = size_list[2]
        size_percentage2 = size_list[3]
    else:
        size2 = "false"
        size_percentage2 = 0


    help_dict = {'help_insert' : size1, 'help_insert1': size_percentage1, 'help_insert2' : size2, 'help_insert3': size_percentage2  }
    # users_input = UsersInput(user_name = user_name, gender = gender, age = age, height = height, weight = weight, tummy_shape = tummy_shape,
    #                         fit_preference = fit_preference, item = item, brand = brand, size = size )


    #validate_scraping(url)
    # data = UsersInput.objects.values_list()
    # for x in data:
    #     print(x)
    # print(data)
    #users_input.save()
    return render(request, "users/size_output.html", context = help_dict ) # after Find my size button direct to...
