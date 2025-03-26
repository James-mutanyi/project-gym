from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def signup(request):
    if request.method =="POST":
      
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1!= pass2:
            messages.info(request, "pasword is not matching")
            return redirect('/signup')

        if len(username)>10 or len(username)<10:
            messages.info(request, "Phone number must be 10 digits")
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