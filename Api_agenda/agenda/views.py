
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.template.loader import render_to_string
from agenda.views import About

import secrets
import string

# Create your views here.

# class Home(APIView):
#    template_name='index.html'
#    def get(self,request):
#        return render(request,self.template_name)

def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect("/")
   
def signup(request):
    if request.method =='GET':
        return render(request, 'signup.html',{
            'form' : UserCreationForm
        })
    # Si no, se esta posteando informacion
    else:
        try:
            # Aqui guarda en la base de datos
            user = User.objects.create_user(first_name=request.POST['first_name'], email=request.POST['email'], last_name=request.POST['last_name'], username=request.POST['username'], password=request.POST['password']) # Al final a password se le asigna el valor de contraseña aleatoria
            # Guardas el usuario
            user.save()
            correo = request.POST['email']
            contra = request.POST['password']
            return redirect('enviar_correo', correo=correo, contra=contra)
        except IntegrityError:
            return render(request, 'signup.html',{
                'form' : UserCreationForm,
                "mensaje" : 'Este usuario ya existe, por favor ingresa otro'
            })
def signout(request):
    logout(request)
    return redirect('signin')
    
class Home(APIView):
    template_name="index.html"
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        return render(request,self.template_name)
    
class tables(APIView):
    template_name="tables.html"
    def get(self,request):
        usuarios = User.objects.all()  # Obtén todos los registros de la tabla auth_user
        return render(request, 'tables.html', {'usuarios': usuarios})
    def post(self,request):
        return render(request,self.template_name)
   
class stats(APIView):
   template_name='stats.html'
   def get(self,request):
       return render(request,self.template_name)
   
class forgot(APIView):
   template_name='correo_recuperacion.html'
   def get(self,request):
       return render(request,self.template_name)     
     
def enviar_correo(request, correo, contra):
    subject = 'Bienvenida'
    from_email = 'carolinasancay21605@gmail.com'
    recipient_list = [correo]
    contexto = {'correo': correo,
                'contra': contra}
    contenido_correo = render_to_string('correo.html', contexto)
    send_mail(subject, '', from_email, recipient_list, html_message=contenido_correo)
    return redirect('signin')
     
   
def forgotPwd(request):
    longitud = 10  # Longitud de la contraseña
    caracteres = string.ascii_letters + string.digits  # Caracteres permitidos

    contra_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(longitud)) # Generacion de la contraseña
    # Si esta solicitando informacion por el metodo GET se envia el formulario
    if request.method =='GET':
        return render(request, 'correo_recuperacion.html',{
            'form' : UserCreationForm
        })
    # Si no, se esta posteando informacion
    else:
        try:
            user = User.objects.filter(email=request.POST['email'])
            if user.exists():
                user = user[0]
                user.set_password(contra_aleatoria)
            # Defines variables para que posteriormente las mandes por una mamada de link inverso xd a la clase que manda el correo
            correo = request.POST['email']
            # Igual aqui a contra le mandas el valor de la cadena generada automaticamente
            contra = contra_aleatoria
            # Aqui retorna a la clase de enviar correo
            return redirect('enviar_correo', correo=correo, contra=contra)
        # Aqui te regresa al mismo formulario si es que el usuario que ingresaste ya existe
        except IntegrityError:
            return render(request, 'correo_recuperacion.html',{
                'form' : UserCreationForm,
                "mensaje" : 'Este usuario ya existe, por favor ingresa otro'
            })