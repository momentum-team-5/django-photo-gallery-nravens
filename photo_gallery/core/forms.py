from .models import Gallery, Photo, Comment
from django import forms
from django.forms import inlineformset_factory
 

CommentFormSet = inlineformset_factory(Photo, Comment, 
    fields = ('text',), )

PhotoFormSet = inlineformset_factory(Gallery, Photo,
    fields = ('title', 'alt_text', 'photo'),
    extra=1)


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = [
            'title',
            'is_private',
                 ]

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            'title',
            'description',
            'alt_text',
            'photo',
            'default',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]





      
