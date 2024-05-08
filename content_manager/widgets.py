from django.forms import Media, widgets


class DsfacileIconPickerWidget(widgets.TextInput):
    template_name = "content_manager/widgets/dsfacile-icon-picker-widget.html"

    def __init__(self, attrs=None):
        default_attrs = {}
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return Media(
            css={"all": ["css/icon-picker.css", "dist/dsfacile/utility/utility.min.css"]},
            js=["django-dsfacile/icon-picker/assets/js/universal-icon-picker.min.js"],
        )
