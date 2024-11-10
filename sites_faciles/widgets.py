from django.forms import Media, widgets


class WagtailSitesFacilesIconPickerWidget(widgets.TextInput):
    template_name = "sites_faciles/widgets/design-system-icon-picker-widget.html"

    def __init__(self, attrs=None):
        default_attrs = {}
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        super().__init__(attrs=attrs)

    @property
    def media(self):
        return Media(
            css={"all": ["css/icon-picker.css", "design-system/dist/utility/utility.min.css"]},
            js=["django_design_system/icon-picker/assets/js/universal-icon-picker.min.js"],
        )
