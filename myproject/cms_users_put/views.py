from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from models import Birthday
from django.template.loader import get_template
from django.template import Context

# Create your views here.


def auth(request):

    if request.user.is_authenticated():
        response = ("Welcome <b> " + request.user.get_username()
                    + " </b> <a href=/logout>Logout</a>")
    else:
        response = "You are not authenticated. <a href='/login'>Login</a>"

    return '<p align="right">' + response + '</p>'


@csrf_exempt
def mi_login(request):

    form = ("<form action ='' method='POST'><br/>" + "Username: " +
            "<input type = 'text' name = 'login'><br/> Password: " +
            "<input type = 'password' name='pwd'><br/>" +
            "<input type='submit' value='Enviar'></form>")
    if request.user.is_authenticated():
        response = (auth(request) +
                    "<p><h1> You're already authenticated!</h1></p>")
    else:
        if request.method == "GET":
            response = auth(request) + "<h1>Login: </h1>" + form
        elif request.method == 'POST':
            username = request.POST['login']
            password = request.POST['pwd']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/cumple')
            else:
                response = (auth(request) + "<h1>Login:</h1><p> The username" +
                            " or password were incorrect</p>" + form)

    return HttpResponse(response)


@csrf_exempt
def mi_logout(request):

    logout(request)

    return redirect('/cumple')


@csrf_exempt
def home(request):

    salida = auth(request) + "<h1>My friends' upcoming birthdays:</h1>"
    tabla = Birthday.objects.all()
    for fila in tabla:
        salida += ("<li><a href=cumple/" + fila.nombre +
                   ">" + fila.nombre + "</a></li>\n")
    salida += "</ul>\n"
    return HttpResponse(salida)


@csrf_exempt
def info(request, recurso):

    if request.method == "POST":
        new = Birthday(nombre=request.POST['nombre'],
                       fecha=request.POST['fecha'],
                       regalo=request.POST['regalo'])
        new.save()

    elif request.method == "PUT":
        (name, date, gift) = request.body.split(";")
        new = Birthday(nombre=name, fecha=date, regalo=gift)
        new.save()

    lista = Birthday.objects.filter(nombre=recurso)
    salida = auth(request)

    if not lista:
        if request.user.is_authenticated():
            form = "<form action='' method='POST'>\n"
            form += ("Name: <input type='text' name='nombre' value='" +
                     recurso + "'><br>\n")
            form += "Date: <input type='date' name='fecha'><br>\n"
            form += "Gift: <input type='text' name='regalo'><br>\n"
            form += "<input type='submit' value='enviar'>\n"
            form += "</form>\n"
            salida += form
        else:
            salida += "You must be logged in. <a href='/login'>Login</a>"

        return HttpResponse(salida)

    for user in lista:
        salida += ("<li><b>Name: </b>" + user.nombre + "</li><li><b>" +
                   "Date: </b>" + str(user.fecha) + "</li><li><b>" +
                   "Birthday gift: </b>" + user.regalo + "</li><br>")
        salida += "</ul>\n"

    return HttpResponse(salida)


def notfound(request, recurso):
    salida = auth(request)
    salida += "No he encontrado el recurso " + recurso
    return HttpResponseNotFound(salida)

@csrf_exempt
def plantilla(request, recurso):

    lista = Birthday.objects.filter(nombre=recurso)

    salida = ""

    for user in lista:
        salida += ("Name: " + user.nombre + " "
                   "Date: " + str(user.fecha) + " "
                   "Birthday gift: " + user.regalo)

    # 1. Indicar la plantilla
    template = get_template("index.html")

    # 2. Marcar el contexto:
    c = Context({'contenido': salida})

    # 3. Renderizar
    lorenderizado = template.render(c)

    return HttpResponse(lorenderizado)
    #return HttpResponse(lorenderizado)

