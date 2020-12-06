from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

class User(AbstractUser):
    pass

class Gallery(models.Model):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, related_name="galleries")
    title = models.CharField(max_length=15)
    is_private = models.BooleanField(default=True)

    def get_thumbnail(self):
        return self.photos.filter(default=True).first()
        
class Photo(models.Model):
    gallery = models.ForeignKey(to="Gallery", on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True, max_length=100)
    alt_text = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='media/gallery_photos/')
    photo_large = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(600, 800, upscale=False)],
        format='JPEG',
        options={'quality': 65})
    photo_medium = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(450, 600, upscale=False)],
        format='JPEG',
        options={'quality': 65})
    photo_thumbnail = ImageSpecField( 
        source='photo',
        processors=[ResizeToFill(200, 200)],
        format='JPEG',
        options={'quality': 65})
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    commenting_users = models.ManyToManyField(User, through='Comment')


    class Meta:
        constraints = [models.UniqueConstraint(fields=['gallery'], condition=models.Q(default=True), name = 'unique_default_photo')]


   
class Comment(models.Model):
    photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(to=User,on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
