from django.db import models
from django. utils.html  import mark_safe
from django.contrib.auth.models import User 

# Create your models here.
class Services(models.Model):
    title =models.CharField(max_length=200)
    description =models.CharField(max_length=200)
    img =models.ImageField(upload_to="services")
    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />'% (self.img.url))
    
class Gallery(models.Model):
    title =models.CharField(max_length=200)
    details =models.TextField()
    img =models.ImageField(upload_to="gallery")
    timetag=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />'% (self.img.url)) 
    
class GalleryImage(models.Model):
    gallery =models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)
    alt_text =models.CharField(max_length=200)
    img =models.ImageField(upload_to="gallery_image")
    timetag=models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.alt_text
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />'% (self.img.url)) 
    
class SubscriptionPlan(models.Model):
    price =models.IntegerField()
    title =models.CharField(max_length=200)
    highlited=models.BooleanField(default=True, null=True)

    def __str__(self):
        return self.title
    
class SubPlan(models.Model):
    title =models.CharField(max_length=200)
    subscriptionplan =models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Trainer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='trainer_profile')
    full_name=models.CharField(max_length=205)
    username=models.CharField(max_length=205, null =True)
    psw =models.CharField(max_length=205, default="trainer")
    mobile=models.CharField(max_length=205)
    details=models.TextField()
    image= models.ImageField(upload_to="trainers/")
    is_active= models.BooleanField(default=False)
    datejoined=models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.full_name
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />'% (self.image.url)) 
    
class Attendance(models.Model):
     selectdate= models.DateTimeField(auto_now_add=True)
     login =models.CharField(max_length=200)
     logout =models.CharField(max_length=200)
     selectworkout =models.CharField(max_length=200)
     trainedby =models.CharField(max_length=200)
     def __str__(self):
         return self.id
     
class Workout(models.Model):
    title=models.CharField(max_length=200)
    image= models.ImageField(upload_to="workout/")
    
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />'% (self.image.url)) 


class Session(models.Model):
    name=models.CharField(max_length=200)
    workout=models.ForeignKey(Workout, on_delete=models.CASCADE)
    starttime=models.TimeField()
    endtime=models.TimeField()
    trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='classes')
    img= models.ImageField(upload_to="session/")
    capacity = models.PositiveIntegerField(default=30)
    


    def __str__(self):
        return self.name
    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />'% (self.img.url)) 

class Booking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    session=models.ForeignKey(Session, on_delete=models.CASCADE, related_name='bookings')
    def __str__(self):
        return self.user.username + " " + self.session.name
    # To prevevent user from booking the same session twice
    class Meta:
        unique_together = ('user', 'session')