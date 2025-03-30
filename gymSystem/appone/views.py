from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages
from .models import *
from .forms import *



# Create your views here.
def home(request):
    return render(request, 'index.html')



def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('confirmPassword')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")  # Use error for password mismatch
            return redirect('/signup/')

        try:
            # Check if username or email already exists using get()
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username is already taken!")
                return redirect('/signup/')
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email is already taken!")
                return redirect('/signup/')

            # If we get here, the username and email are unique, so create the user
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()  #redundant
            messages.success(request, "User created successfully.")
            return redirect(reverse('login'))

        except IntegrityError:  # Catch IntegrityError specifically
            messages.error(request, "Error: User could not be created.  Username or email may already exist.")
            return redirect('/signup/')
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect('/signup/')

    return render(request, 'signup.html')


def services(request):
    service= Services.objects.all()
    context ={"service":service}
    return render(request, "services2.html", context)

def about(request):
    return render(request, "about.html")


def gallery(request):
    post=Gallery.objects.all()
    context ={"post": post}
    return render (request, "gallery.html", context)



def galleryimages(request, id):
    gallery=Gallery.objects.get(id=id)
    galleryimg =GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    return render(request, "galleryimg.html", {"gallery":gallery, "galleryimg":galleryimg})

def is_trainer(user):
    # return user.groups.filter(name='Trainer').exists()
    return hasattr(user, 'trainer_profile')

# @user_passes_test(is_trainer, login_url='/login')
def trainerlogin(request): 
   
    if request.method=='POST':
        username= request.POST['username']
        password= request.POST['psw']
        trainer =Trainer.objects.filter(username= username, psw=password).count()
        if trainer >0:
            request.session['trainerlogin']=True
            messages.success(request, "login sucess")
            
            return redirect('/trainer_dashboard')
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

def workout(request):
    workout=Workout.objects.all()   
    context ={"workout":workout}
    return render(request, "workout.html", context)

def session(request, id):
    workout=Workout.objects.get(id=id)
    session=Session.objects.filter(workout=workout)
    context ={"session":session}
    return render(request, "session.html", context)

def pricing(request):
    price= SubscriptionPlan.objects.all()
    context={"price":price}
    return render(request, 'plans.html', context )

def dashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please login first.")
        return redirect('/login')
    user = request.user
    attendance=Attendance.objects.all()
    user_session =request.user.bookings.all()
    attendance_records = Attendance.objects.filter(user=user)
    user_bookings = Booking.objects.filter(user=user).select_related('session', 'session__trainer__user')
    return render(request, 'dashboard.html', {"attendance":attendance, "user_session":user_session, 'user_bookings': user_bookings, "attendance_records": attendance_records})    

def gallery(request):
    post=Gallery.objects.all()
    context ={"post": post}
    return render (request, "gallery.html", context)

def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please login first.")
        return redirect('/login')
        
    trainer =Trainer.objects.all()
    context={"trainer":trainer}
    if request.method =='POST':
        user =request.user
        login =request.POST.get('login')
        logout =request.POST.get('logout')
        workout =request.POST.get('workout')
        trainer =request.POST.get('domain')
       

        myquery=Attendance( user =user,login=login, logout=logout, selectworkout=workout, trainedby=trainer)
        myquery.save()
        messages.success(request,("Your attendace has been updated sucessfully."))
        return redirect('/dashboard')
    
    return render(request, "attendance.html", context)

#To check if the user is a trainer or not


# To list all the sessions
@login_required(login_url='/login')
def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'session_list.html', {'sessions': sessions})

@login_required(login_url='/login')
def book_session(request, id):
    session =get_object_or_404(Session, id=id)
    user=request.user
    #check if the session is already booked
    existing_booking = Booking.objects.filter(user=request.user, session=session).first() 
    if existing_booking:
        messages.warning(request, "You have already booked this session.")
        return redirect('/dashboard')
    if session.capacity <= 0:
        messages.error(request, "Sorry, this session is fully booked.")
        return redirect('session_list')  # Redirect to the session list page
     # Create the booking
    booking = Booking.objects.create(user=user, session=session)
    messages.success(request, f"You have successfully booked {session.name}.")
    return redirect('dashboard') 


#To list all the bookings in the trainer's dashboard
# @login_required(login_url='/login')
# @user_passes_test(is_trainer, login_url='/login') #Only trainers can access this view
def trainer_dashboard(request):
    user = request.user
    try:
        trainer = Trainer.objects.get(user=user)
    except Trainer.DoesNotExist:
        messages.error(request, "You are not a trainer.")
        return redirect('/') 
    trainer_sessions = Session.objects.filter(trainer=trainer).prefetch_related('bookings__user')
    return render(request, 'trainer_dashboard.html', {'trainer_sessions': trainer_sessions})

 

def leg(request):
    return render(request, 'leg.html')
def blog(request):
    return render(request, 'blog.html')
def blog1(request):
    return render(request, 'blog1.html')
def blog2(request):
    return render(request, 'blog2.html')
def blog3(request):
    return render(request, 'blog3.html')
def contact (request):
    return render(request, 'contact.html')
def upper (request):
    return render(request, 'upper.html')
def fitness (request):
    return render(request, 'fitness.html')
def abs (request):
    return render(request, 'abs.html')