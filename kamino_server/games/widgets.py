from django import forms
from django.utils.safestring import mark_safe


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)


        search_key = "name=\""
        start = input_html.find(search_key) + len(search_key)
        end = input_html.find("\"", start)
        input_name = input_html[start:end]

        img_html = mark_safe(
            f'<br><br><img id="{input_name}" src="#" width="50" />')
        return f'{input_html}{img_html}'
