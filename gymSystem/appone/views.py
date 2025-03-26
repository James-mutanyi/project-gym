from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages




# Create your views here.
def home(request):
    return render(request, 'index.html')


#signup view for new users.
def signup(request):
    if request.method =="POST":
        username = request.POST.get('username')
        phonenumber= request.POST.get('phoneNumber')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirmPassword')
        if pass1!= pass2:
            messages.info(request, "password is not matching")
            return redirect('/signup')

        if len(phonenumber)>10 or len(phonenumber)<10:
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
        myuser=User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "User is created Sucessfully.") 
        return redirect('/login')   

    return render(request, 'signup.html')
