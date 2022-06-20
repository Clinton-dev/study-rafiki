from django.shortcuts import render, redirect
from django.db.models import Q #allow chaining of queries
from django.http import HttpResponse
from .models import Room,Topic, Message
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout



def loginView(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request, 'login details are invalid please check the username or password!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'login failed!')
            return redirect('login')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutView(request):
    logout(request)
    return redirect('login')

def register(request):
    context = {
        'form': UserCreationForm()
    }

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Registration failed! Please check form for errors.")

    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q) |
        Q(name__icontains=q)
    )
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': rooms_count,
        'room_messages': room_messages
    }
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if  request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room':room,
        'room_messages': room_messages,
        'participants': participants
        }

    return render(request,"base/room.html", context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }

    return render(request, 'base/room_form.html', context )

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        form =  RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='/login')
def deleteComment(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        message.delete()
        messages.success(request, "message deleted")
        return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='/login')
def updateComment(request, pk):
    # Add update functionality to comments
    pass