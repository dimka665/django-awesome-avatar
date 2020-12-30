=====================
django-awesome-avatar
=====================

Django-awesome-avatar is a reusable application providing Avatar model field.
It allows crop selected area before saving image.

Now supports python3.x / django3.x

Purpose
=======

| Unlike django-avatar_ and django-upload-avatar_  
| django-awesome-avatar_ uses:

- field in profile model instead creating model for saving images
- HTML5 File API instead hidden iframe AJAX for image preview
- easy customizable presence (any view and widget templates)

Install
=======

To integrate ``django-awesome-avatar`` with your site, there are few things
that are required:

#. Installing::

       pip install django-awesome-avatar

#. List this application in the ``INSTALLED_APPS`` portion of your settings file.
   Your settings file will look something like::

        INSTALLED_APPS = (
            ...
            'awesome_avatar',
        )

Usage examples
==============

with ModelForm
--------------

Add the ``AvatarField`` to your user or profile model::
        
    from awesome_avatar.fields import AvatarField
 
    class Profile(Model):
        user = OneToOneField(User, related_name='profile')
        ...
        avatar = AvatarField(upload_to='avatars', width=100, height=100)

Use model form usually way::

    class AvatarChangeForm(ModelForm):
        class Meta:
            model = Profile
            fields = ['avatar']
        
    def change_avatar(request):
        if request.method == 'POST':
            form = AvatarChangeForm(request.POST, request.FILES,
                                    instance=request.user.profile)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/profile/')
        else:
            form = AvatarChangeForm(instance=request.user.profile)

        return render(request, 'template.html', {'form': form})
            
with Form
---------

Define some model for saving images::
    
    class Images(Model):
        image = ImageField(upload_to='images')
            
Use form field for cropping image::

    from awesome_avatar import forms as avatar_forms

    class UploadAndCropImageForm(Form):
        image = avatar_forms.AvatarField()
 
    def upload_and_crop_image(request):
        if request.method == 'POST':
            form = UploadAndCropImageForm(request.POST)
                
            if form.is_valid():
                Images(image=form.image).save()
                return HttpResponseRedirect('/any/')
        else:
            form = UploadAndCropImageForm()

        return render(request, 'template.html', {'form': form})
            
        
Global Settings
===============

Django's ``settings.py``::
     
    AWESOME_AVATAR = {
        'width': 100,
        'height': 100,
        
        'select_area_width': 400,
        'select_area_height': 300,
        
        'save_quality': 90,
        'save_format': 'png',
        ...
    }
     
.. _django-avatar: https://github.com/jezdez/django-avatar
.. _django-upload-avatar: https://github.com/yueyoum/django-upload-avatar
.. _django-awesome-avatar: https://github.com/dimka665/django-awesome-avatar
