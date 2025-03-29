from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages
from .models import *
from .forms import *



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

def about(request):
    return render(request, "about.html")
    

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
    attendance=Attendance.objects.all()
    user_session =request.user.bookings.all()
    return render(request, 'dashboard.html', {"attendance":attendance, "user_session":user_session})    

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
        login =request.POST.get('login')
        logout =request.POST.get('logout')
        workout =request.POST.get('workout')
        trainer =request.POST.get('domain')

        myquery=Attendance( login=login, logout=logout, selectworkout=workout, trainedby=trainer)
        myquery.save()
        messages.success(request,("Your attendace has been updated sucessfully."))
        return redirect('/dashboard')
    
    return render(request, "attendance.html", context)

#To check if the user is a trainer or not
def is_trainer(user):
    # return user.groups.filter(name='Trainer').exists()
    return hasattr(user, 'trainer_profile')

# To list all the sessions
@login_required(login_url='/login')
def session_list(request):
    session=Session.objects.all().annotate(num_bookings=Count('bookings'))
    context={"session":session}
    return render(request, 'sessionlist.html', context)

@login_required(login_url='/login')

def book_session(request, id):
    session =get_object_or_404(Session, id=id)
    #check if the session is already booked
    existing_booking = Booking.objects.filter(user=request.user, session=session).first() 
    if existing_booking:
        messages.warning(request, "You have already booked this session.")
        return redirect('/darshboard')
    if request.method == 'POST':
        form =BookingForm(request.POST)
        if form.is_valid():
            booking =form.save(commit=False)
            booking.user =request.user
            booking.session =session
            
            # check if there is still space in the session
            if session.bookings.count() < session.capacity:
                booking.save()
                messages.success(request, "You have booked the session sucessfully.")
                return redirect('/dashboard')
            else:
                messages.error(request, "The session is already full.")
                return redirect('/session_list')
           
    else:
        form = BookingForm()
    return render(request, 'workout.html', { "form":form, "session":session})

#To list all the bookings in the trainer's dashboard
@login_required(login_url='/login')
@user_passes_test(is_trainer, login_url='/login') #Only trainers can access this view
def trainer_dashboard(request):
    trainer =request.user.trainer_profile
    trainer_session=trainer.classes.all()
    trainer_booking =Booking.objects.filter(session__trainer=trainer).order_by('-booking_date')
    context ={"trainer_session":trainer_session, "trainer_booking":trainer_booking}
    return render(request, 'trainer_session.html', context)

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