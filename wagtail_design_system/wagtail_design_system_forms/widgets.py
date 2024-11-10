from django.forms.widgets import RadioSelect


# from django.utils.safestring import mark_safe


class WagtailDesignSystemFormsRadioSelect(RadioSelect):
    template_name = "wagtail_design_system_forms/widgets/radio_select.html"
