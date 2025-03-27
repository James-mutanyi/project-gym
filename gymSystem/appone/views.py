from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .forms import TrainerLoginForm



# Create your views here.
def home(request):
    return render(request, 'index.html')



def signup(request):
    if request.method =="POST":
      
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1!= pass2:
            messages.info(request, "pasword is not matching")
            return redirect('/signup')

  

        try:
            if User.objects.get(username= username):
                messages.warning(request, "User is already taken!")
                return redirect('/signup')

        except Exception as identifier:
            pass

        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email is Taken")
                return redirect('/signup')
        except Exception as identifier:
            pass  
        myuser=User.objects.create_user( username, email,pass1)
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.save()
        messages.success(request, "User is created Sucessfully.") 
        return redirect('/login')   

    return render(request, 'signup.html')

def services(request):
    service= Services.objects.all()
    context ={"service":service}
    return render(request, "services2.html", context)

def gallery(request):
    gallery=Gallery.objects.all().order_by('-id')
    context ={"gallery":gallery,}
    return render(request, "gallery.html", context)

def galleryimages(request, id):
    gallery=Gallery.objects.get(id=id)
    galleryimg =GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    # context ={"gallery":gallery, "galleryimg":galleryimg}
    return render(request, "galleryimg.html", {"gallery":gallery, "galleryimg":galleryimg})


def trainerlogin(request): 
   
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['psw']
        trainer =Trainer.objects.filter(username= username, psw=password).count()
        if trainer >0:
            request.session['trainerlogin']=True
            messages.success(request, "login sucess")
            
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
    form =TrainerLoginForm()
    return render (request, 'trainerlogin.html', {"form":form})

def trainerlogout(request):
    del request.session['trainerlogin']
    return redirect('/trainerlogin')


def trainer(request):
    trainer=Trainer.objects.all()
    context ={"trainer":trainer}
    return render(request, "trainer.html", context)

