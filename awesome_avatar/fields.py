import os
import uuid
from awesome_avatar.settings import config
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from awesome_avatar import forms
from awesome_avatar.widgets import AvatarWidget

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:  # python 3
        from io import BytesIO as StringIO

try:
    from PIL import Image
except ImportError:
    import Image

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^awesome_avatar\.fields\.AvatarField'])
except ImportError:
    pass


class AvatarField(models.ImageField):
    def __init__(self, *args, **kwargs):

        self.width = kwargs.pop('width', config.width)
        self.height = kwargs.pop('height', config.height)

        kwargs['upload_to'] = kwargs.get('upload_to', config.upload_to)

        super(AvatarField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.AvatarField,
            'width': self.width,
            'height': self.height,
        }
        defaults.update(kwargs)

        # django 1.7 fix default widget
        if not defaults.get('widget') or not isinstance(defaults.get('widget'), AvatarWidget):
            defaults['widget'] = AvatarWidget
        return super(AvatarField, self).formfield(**defaults)

    def save_form_data(self, instance, data):
        # if data and self.width and self.height:
        file_ = data['file']
        if file_:

            image = Image.open(file_)
            image = image.crop(data['box'])
            image = image.resize((self.width, self.height), Image.ANTIALIAS)

            file_name = u'{}.{}'.format(str(uuid.uuid1()), config.save_format)
            new_data = InMemoryUploadedFile(StringIO(), None, file_name, 'image/' + config.save_format, 0, None)

            image.save(new_data, config.save_format, quality=config.save_quality)

            super(AvatarField, self).save_form_data(instance, new_data)
