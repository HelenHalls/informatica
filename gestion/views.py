from django.shortcuts import render, redirect, get_object_or_404
from .models import Message, UserProfile, Follow, Coment
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm, ComentForm


# Create your views here.
@login_required(login_url='login')
def message_list(request):
    messages = Message.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    followed_users = Follow.objects.filter(follower=request.user)
    usuario = UserProfile.objects.get(user=request.user)
    return render(request, 'gestion/message_list.html', {'messages': messages, 'followed_users': followed_users, 'usuario': usuario})

@login_required(login_url='login')
def users_list(request):
    users = User.objects.all()
    me = User.objects.get(username = request.user.username)
    return render(request, 'gestion/users_list.html', {'users': users, 'me':me})

@login_required(login_url='login')
def user_detail(request, user_details):
    usuario = get_object_or_404(User, username=user_details)
    return render(request, 'gestion/user_detail.html', {'usuario': usuario})

@login_required(login_url='login')
def message_detail(request, pk):
    mensaje = get_object_or_404(Message, pk=pk)
    comentarios = Coment.objects.filter(id_message=pk)
    return render(request, 'gestion/message_detail.html', {'mensaje':mensaje, 'comentarios':comentarios})

def acceso(request):
    if not request.user.is_anonymous():
        return redirect('/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return redirect('/')
            else:
                return render(request, 'gestion/no_activo.html')
        else:
            return render(request, 'gestion/no_usuario.html')
    else:
        formulario = AuthenticationForm()
    return render(request, 'gestion/login.html', {'formulario': formulario})

@login_required(login_url='login')
def salir(request):
    logout(request)
    return redirect('/')

def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            usuario = User.objects.get(username=formulario.cleaned_data['username'])
            user = UserProfile(user=usuario)
            user.save()
            return redirect('/')
        else:
            return render(request, 'gestion/no_valido.html')
    else:
        formulario = UserCreationForm()
    return render(request, 'gestion/nuevo_usuario.html', {'formulario':formulario})

@login_required(login_url='login')
def follow(request, userr):
    response = ''

    if request.method == 'GET':

      try:
          usr2folw = User.objects.get(username=userr)
      except:
          response = 'Lo sentimos, no puedes seguir a nadie en estos momentos.'

      # Follow process. create master and slave.
      # slave follows master. Update followers count
      # and following count once done.
      else:
          if request.user == usr2folw:

              response = 'Un usuario no puede seguirse a si mismo.'

          else:

              try:
                  obj, created = Follow.objects.get_or_create(follower=request.user, followed=usr2folw)

                  if created:
                      master = UserProfile.objects.get(user=usr2folw) # El que es seguido
                      slave = UserProfile.objects.get(user=request.user) # El que sigue
                      master.follower_count = master.follower_count+1 # Aumentamos el numero de seguidores del que es seguido
                      slave.followed_count = slave.followed_count+1 # Aumentamos el numero de seguidos del que sigue
                      master.save()
                      slave.save()

                      response = 'Ahora sigues a @%s.' % (usr2folw.username)
                  elif obj is not None:

                      response = 'Ya sigues a @%s.' % (usr2folw.username)


              except:
                  response = 'Lo sentimos, no puedes seguir a @%s en estos momentos.' % (usr2folw.username)
    else:
      response = 'Lo sentimos, la peticion no puede ser atendida en estos momentos, intentalo de nuevo mas tarde.'

    return render(request, 'gestion/follow.html', {'response':response})

@login_required(login_url='login')
def unfollow(request, userr):

    response = ''

    if request.method == 'GET':

        try:
            usr2unfolw = User.objects.get(username=userr)
        except:
            response = 'Lo sentimos, no puedes dejar de seguir a nadie en estos momentos.'

        else:
            if request.user == usr2unfolw: # Si intentamos dar unfollow a nosotros mismos
                response = 'Un usuario no puede seguirse a si mismo, y tampoco dejar de seguirse.'

            else:
                try:
                    obj = Follow.objects.get(follower=request.user,followed=usr2unfolw).delete()
                    master = UserProfile.objects.get(user=usr2unfolw) # El que es seguido
                    slave = UserProfile.objects.get(user=request.user) # El que sigue
                    master.follower_count = master.follower_count-1
                    slave.followed_count = slave.followed_count-1
                    master.save()
                    slave.save()

                    response = 'Has dejado de seguir a @%s.' % usr2unfolw.username
                except:
                    response = 'No sigues a @%s.' %(usr2unfolw.username)

    else: # Si no es method == 'GET'
        response = 'Lo sentimos, la peticion no puede ser atendida en estos momentos, intentalo de nuevo mas tarde.'

    return render(request, 'gestion/unfollow.html', {'response':response})

@login_required(login_url='login')
def ver_seguidores(request):
    seguidores = Follow.objects.filter(followed=request.user)
    return render(request, 'gestion/ver_seguidores.html', {'seguidores': seguidores})

@login_required(login_url='login')
def ver_seguidos(request):
    seguidos = Follow.objects.filter(follower=request.user)
    return render(request, 'gestion/ver_seguidos.html', {'seguidos': seguidos})

@login_required(login_url='login')
def new_message(request):
        if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.published_date = timezone.now()
                message.save()
                return redirect('/')
        else:
            form = MessageForm()
        return render(request, 'gestion/new_message.html', {'form': form})

@login_required(login_url='login')
def new_coment(request, pk):
        if request.method == "POST":
            form = ComentForm(request.POST)
            if form.is_valid():
                coment = form.save(commit=False)
                coment.author = request.user
                coment.published_date = timezone.now()
                coment.id_message = Message.objects.get(pk=pk)
                coment.save()
                return redirect('detalle_mensaje', pk=pk)
        else:
            form = ComentForm()
        return render(request, 'gestion/new_coment.html', {'form': form})
