from django.forms.widgets import RadioSelect


# from django.utils.safestring import mark_safe


class SitesFacilesRadioSelect(RadioSelect):
    template_name = "wagatil_sites_faciles_forms/widgets/sites_faciles_radio_select.html"
