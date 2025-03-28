from django.contrib import admin
from .models import *
# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(Services, ServiceAdmin)

class GalleryAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(Gallery, GalleryAdmin)

class GalleryImageAdmin(admin.ModelAdmin):
    list_display=('alt_text', 'image_tag')
admin.site.register(GalleryImage, GalleryImageAdmin)

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display=('title', 'price', 'highlited')
    list_editable=('highlited',)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)

class SubPlanAdmin(admin.ModelAdmin):
    list_display=('title', )
admin.site.register(SubPlan, SubPlanAdmin)

class TrainerAdmin(admin.ModelAdmin):
    list_display=('full_name', 'mobile', 'image_tag', 'is_active')
    list_editable=('is_active',)
admin.site.register(Trainer, TrainerAdmin)

class WorkoutAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(Workout, WorkoutAdmin)

class SessionAdmin(admin.ModelAdmin):
    list_display=('workout', 'trainer', 'image_tag')
admin.site.register(Session, SessionAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display=('user', 'session')
admin.site.register(Booking, BookingAdmin)

admin.site.register(Attendance)
