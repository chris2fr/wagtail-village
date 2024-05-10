from django.forms import Media, widgets


class DsfacileIconPickerWidget(widgets.TextInput):
    template_name = "content_manager/widgets/webfastoche-icon-picker-widget.html"

    def __init__(self, attrs=None):
        default_attrs = {}
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return Media(
            css={"all": ["css/icon-picker.css", "dist/webfastoche/utility/utility.min.css"]},
            js=["django-webfastoche/icon-picker/assets/js/universal-icon-picker.min.js"],
        )
