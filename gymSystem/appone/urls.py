from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"), 
    path('signup',views.services, name="services"),
    path('gallery',views.gallery, name="gallery"),
    path('trainerlogin',views.trainerlogin, name="trainerlogin"),
    path('trainerlogout',views.trainerlogout, name="trainerlogout"),
    path('trainer',views.trainer, name="trainer"),
    path('subplan',views.pricing, name="pricing"),
    path('dashboard',views.dashboard, name="dashboard"),
    path('attendance',views.attendance, name="attendance"),
    path('session/<int:id>',views.session, name="session"),
    path('workout',views.workout, name="workout"),
    path('legwork',views.legworkout, name="legworkout"),
    path('book_session/<int:id>',views.book_session, name="book_session"),
    path('galleryimages/<int:id>', views.galleryimages, name='galleryimages'),
    path('trainer_dashboard', views.trainer_dashboard, name='trainer_dashboard'),
    path('about', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('sessionlist', views.session_list, name='session_list'),
    path('blog1', views.blog1, name='blog1'),
    path('blog2', views.blog2, name='blog2'),
    path('blog3', views.blog3, name='blog3'),
    path('contact', views.contact, name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
