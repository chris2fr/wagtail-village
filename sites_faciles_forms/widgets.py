from django.forms.widgets import RadioSelect


# from django.utils.safestring import mark_safe


class VillageRadioSelect(RadioSelect):
    template_name = "wagatil_village_forms/widgets/village_radio_select.html"
