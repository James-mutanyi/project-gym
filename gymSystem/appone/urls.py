from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"), 
    path('services',views.services, name="services"),
    path('gallery',views.gallery, name="gallery"),
    path('trainerlogin',views.trainerlogin, name="trainerlogin"),
    path('trainerlogout',views.trainerlogout, name="trainerlogout"),
    path('trainer',views.trainer, name="trainer"),
    path('galleryimages/<int:id>', views.galleryimages, name='galleryimages'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
