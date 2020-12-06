from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GalleryForm, PhotoForm, CommentForm, PhotoFormSet
from .models import Gallery, Photo, Comment, User
from django.http import HttpResponse



# These galleries have a default photo -- the photo shown when looking at galleries
# Idea: Make public and private galleries
# Idea: Can galleries be shared so that multiple users can add photos to them?
# Users can upload photos
# Consider whether photos need to be in a gallery or not. Can they be in multiple galleries? These are questions you need to answer. 
# Photos should have thumbnails. Look at Django-Imagekit and see if it will work for your needs.
# Users have profiles where you can see their galleries
# If you have public and private galleries, then don't show private galleries
# What if you can have pictures not in galleries? How does that work?
# This doesn't have to look like a list of galleries. This could be a series of updates, Facebook-style, for example.
# Idea: Users can pin or spotlight photos or galleries to appear first.
# Users can leave comments on photos
# When a user leaves a comment, the owner of the photo should get an email notifying them of that comment. (Idea: perhaps you don't get the email if you are both the owner and wrote the comment.)

def homepage(request):
    if request.user.is_authenticated:
        return redirect(to="gallery_list", username=request.user.username)

    return render(request, "core/home.html")

def gallery_list(request, user_id=None):
    
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)
    galleries = user.galleries.all()
    if user != request.user:
        galleries = galleries.filter(is_private=False)
    
    return render(request, "core/gallery_list.html", {"galleries":galleries})


def gallery_detail(request, gallery_pk):
    """
    Renders of all of a gallery's photos. 
    If the gallery is private, only the user associated with the gallery
    can view the photos. 
    """
    
    gallery = get_object_or_404(Gallery, pk=gallery_pk)
    if gallery.is_private:
        if request.user != gallery.user:
            return HttpResponse(status=401)
    photos = gallery.photos.all()
    
    return render(request, "core/gallery_detail.html", {"gallery": gallery, "photos": photos})


@login_required
def gallery_create(request):
    
    if request.method=="GET":
        form = GalleryForm()
        photo_formset = PhotoFormSet()
    else:
        form = GalleryForm(data=request.POST)
        photo_formset = PhotoFormSet(data=request.POST, files=request.FILES)
        if form.is_valid() and photo_formset.is_valid():
            gallery = form.save(commit=False)
            gallery.user = request.user
            gallery.save()
            photos = photo_formset.save(commit=False)
            for photo in photos:
                photo.gallery = gallery
                photo.default = True
                photo.save()
    
            return redirect(to="gallery_detail", gallery_pk = gallery.pk)
    return render(request, "core/gallery_create.html", {"form": form, "photo_formset": photo_formset})

@login_required
def gallery_update(request, gallery_pk):
    gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)

    if request.method=="GET":
        form = GalleryForm(instance=gallery)
    else:
        form = GalleryForm(instance=gallery, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="gallery_detail", gallery_pk = gallery_pk)
    return render(request, "core/gallery_update.html", {"form": form})

@login_required
def gallery_delete(request, gallery_pk):
    gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)
    gallery.delete()
    return redirect(to="gallery_list", user_id=request.user.id)



def photo_detail(request, photo_pk):
    photo = get_object_or_404(Photo, pk=photo_pk)
    
    if photo.gallery.is_private:
        if request.user != photo.gallery.user:
            return HttpResponse(status=401)

    if request.method=="GET":
        form=CommentForm()
    else:
        form=CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author=request.user
            comment.photo=photo
            comment.save()
            return redirect(to="photo_detail", photo_pk=photo.pk)
    comments = photo.comments.all()

    return render(request, "core/photo_detail.html", {"form": form, "photo": photo, "comments": comments})

@login_required
def photo_create(request, gallery_pk):
    gallery = get_object_or_404(request.user.galleries, pk=gallery_pk)
    if request.method=="GET":
        form = PhotoForm()
    else:
        form = PhotoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.gallery = gallery
            photo.save()
            return redirect(to="photo_create", gallery_pk = gallery_pk)
    return render(request, "core/photo_create.html", {"gallery":gallery, "form": form})

@login_required
def photo_update(request, photo_pk):
    photo = get_object_or_404(Photo.objects.filter(gallery__user=request.user), pk=photo_pk)
    if request.method=="GET":
        form = PhotoForm(instance=photo)
    else:
        form = PhotoForm(instance=photo, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(to="gallery_detail", gallery_pk = photo.gallery.pk)
    return render(request, "core/photo_update.html", {"photo":photo, "form":form})

@login_required
def photo_delete(request, photo_pk):
    photo = get_object_or_404(Photo.objects.filter(gallery__user=request.user), pk=photo_pk)
    gallery_pk = photo.gallery.pk
    photo.delete()
    return redirect(to="gallery_detail", gallery_pk = gallery_pk)



            
