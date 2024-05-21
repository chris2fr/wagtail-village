from django.forms import Media, widgets


class WagtailCfranIconPickerWidget(widgets.TextInput):
    template_name = "wagtail_cfran/widgets/cfran-icon-picker-widget.html"

    def __init__(self, attrs=None):
        default_attrs = {}
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return Media(
            css={"all": ["css/icon-picker.css", "django_cfran/dist/utility/utility.min.css"]},
            js=["django_cfran/icon-picker/assets/js/universal-icon-picker.min.js"],
        )
