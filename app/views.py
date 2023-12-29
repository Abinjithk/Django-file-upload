from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import UploadedFile


# creating a form
class InputForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())



class UploadFileForm(forms.Form):
    Name_of_the_file = forms.CharField(max_length=50)
    file = forms.FileField()


# Create your views here.

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                print('User authenticated. Redirecting to home.')
                return redirect('home')
            else:
                print('Authentication failed.')
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm(request)

    print('Redirection failed. Form errors:', form.errors)
    return render(request, "login.html", {'form': form})


def register(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            # Create a new user instance and save it to the database
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = InputForm()

    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    return render(request, "index.html")


@login_required
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["Name_of_the_file"]
            file = form.cleaned_data["file"]
            store = UploadedFile(title=title, file=file,user_id=request.user.id)
            store.save()
            print("data saved successfully")
            return redirect('home')

        else:
            return render(request, "upload_file.html", {"form": form})
    else:
        form = UploadFileForm()

    return render(request, "upload_file.html", {"form": form})


@login_required
def uploaded_file(request):
    user_uploaded_files = UploadedFile.objects.filter(user_id=request.user.id)
    return render(request, "uploaded_file.html",{"user_uploaded_files": user_uploaded_files})



def user_logout(request):
    logout(request)
    return redirect("signin")

