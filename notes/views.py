from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")

@login_required
def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
             note = form.save(commit=False)
             note.user = request.user
             note.save()
             return redirect("note_list")
            
    else:
        form = NoteForm()

    return render(request, "add_note.html", {"form": form})

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, "note_list.html", {"notes": notes})

@login_required
def edit_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm(instance=note)

    return render(request, "edit_note.html", {"form": form})

@login_required
def delete_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)

    if request.method == "POST":
        note.delete()
        return redirect("note_list")

    return render(request, "delete_note.html", {"note": note})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Registration Successful")
        return redirect("login")

    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")