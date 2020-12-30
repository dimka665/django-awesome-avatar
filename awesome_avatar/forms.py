from django import forms

from awesome_avatar.settings import config
from awesome_avatar.widgets import AvatarWidget


class AvatarField(forms.ImageField):
    widget = AvatarWidget

    def __init__(self, **defaults):
        self.width = defaults.pop('width', config.width)
        self.height = defaults.pop('height', config.height)
        super(AvatarField, self).__init__(**defaults)

    def to_python(self, data):
        super(AvatarField, self).to_python(data['file'])
        return data


    def widget_attrs(self, widget):
        return {'width': self.width, 'height': self.height}
