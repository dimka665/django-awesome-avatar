from django import forms

from awesome_avatar.settings import config
from awesome_avatar.widgets import AvatarWidget


class AvatarField(forms.ImageField):
    widget = AvatarWidget
