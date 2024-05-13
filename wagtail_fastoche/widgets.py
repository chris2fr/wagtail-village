from django.forms import Media, widgets


class WagtailFastocheIconPickerWidget(widgets.TextInput):
    template_name = "wagtail_fastoche/widgets/fastoche-icon-picker-widget.html"

    def __init__(self, attrs=None):
        default_attrs = {}
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return Media(
            css={"all": ["css/icon-picker.css", "fastoche/dist/utility/utility.min.css"]},
            js=["django-fastoche/icon-picker/assets/js/universal-icon-picker.min.js"],
        )
