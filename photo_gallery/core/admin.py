from django.contrib import admin
from .models import Gallery, Photo, Comment, User

# Register your models here.
admin.site.register(Gallery)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(User)
