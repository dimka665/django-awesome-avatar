from django.conf import settings
from django.forms import FileInput
from django.template.loader import render_to_string

from awesome_avatar.settings import config


class AvatarWidget(FileInput):

    def value_from_datadict(self, data, files, name):
        value = {}
        value['file'] = super(AvatarWidget, self).value_from_datadict(data, files, name)

        x1 = data.get(name + '-x1', 0)
        y1 = data.get(name + '-y1', 0)
        x2 = data.get(name + '-x2', x1)
        y2 = data.get(name + '-y2', y1)

        ratio_str = data.get(name + '-ratio', 1)
        if (ratio_str != ''):
            ratio = float(ratio_str)
        else:
            ratio = 1.0

        box_raw = [x1, y1, x2, y2]
        box = []

        for coord in box_raw:
            try:
                coord = int(coord)
            except ValueError:
                coord = 0

            if ratio > 1:
                coord = int(coord * ratio)
            box.append(coord)

        value['box'] = box
        return value

    def render(self, name, value, attrs=None):

        config.height = self.attrs['height']
        config.width = self.attrs['width']

        context = {}
        context['name'] = name
        context['config'] = config

        if type(value) != dict:
            context['avatar_url'] = value.url if value else '/static/awesome_avatar/default.png'
        else:
            context['avatar_url'] = '/static/awesome_avatar/default.png'

        context['id'] = attrs.get('id', 'id_' + name)

        # todo fix HACK
        context['STATIC_URL'] = settings.STATIC_URL
        return render_to_string('awesome_avatar/widget.html', context)
