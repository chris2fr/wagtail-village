from django.forms import Media, widgets


class WagtailVillageIconPickerWidget(widgets.TextInput):
    template_name = "wagtail_village/widgets/village-icon-picker-widget.html"

    def __init__(self, attrs=None):
        default_attrs = {}
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return Media(
            css={"all": ["css/icon-picker.css", "django_village/dist/utility/utility.min.css"]},
            js=["django_village/icon-picker/assets/js/universal-icon-picker.min.js"],
        )
