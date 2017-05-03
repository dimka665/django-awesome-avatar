import os
from awesome_avatar.settings import config
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from awesome_avatar import forms

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

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
        defaults = {'form_class': forms.AvatarField}
        defaults['width'] = self.width
        defaults['height'] = self.height
        defaults.update(kwargs)
        return super(AvatarField, self).formfield(**defaults)

    def save_form_data(self, instance, data):
        # if data and self.width and self.height:
        file_ = data['file']
        if file_:

            image = Image.open(StringIO(file_.read()))
            image = image.crop(data['box'])
            image = image.resize((self.width, self.height), Image.ANTIALIAS)

            content = StringIO()
            image.save(content, config.save_format, quality=config.save_quality)

            file_name = u'{}.{}'.format(os.path.splitext(file_.name)[0], config.save_format)

            # new_data = SimpleUploadedFile(file.name, content.getvalue(), content_type='image/' + config.save_format)
            new_data = InMemoryUploadedFile(content, None, file_name, 'image/' + config.save_format, len(content.getvalue()), None)
            super(AvatarField, self).save_form_data(instance, new_data)
