# from wagtail.contrib.forms.panels import FormSubmissionsPanel
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractFormField, EmailFormMixin, FormMixin
from wagtail.fields import RichTextField

from sites_faciles.models import ContentPage

from .widgets import VillageRadioSelect


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")

    def get_field(self):
        print("get_field")
        if self.field_type == "radio":
            print("VillageRadioSelect")
            return forms.ChoiceField(
                label=self.label,
                required=self.required,
                help_text=self.help_text,
                widget=VillageRadioSelect,
                choices=self.choices,
            )
        return super().get_field()

    # # add custom fields to FormField model
    # field_classname = models.CharField("Field classes", max_length=254, blank=True)
    # placeholder = models.CharField("Placeholder", max_length=254, blank=True)

    # # revise panels so that the field can be edited in the admin UI
    # panels = AbstractFormField.panels + [
    #     FieldPanel("field_classname"),
    #     FieldPanel("placeholder"),
    # ]


# class CustomFormBuilder(FormBuilder):
#     def get_create_field_function(self, type):
#         """
#         Override the method to prepare a wrapped function that will call the original
#         function (which returns a field) and update the widget's attrs with a custom
#         value that can be used within the template when rendering each field.
#         """

#         create_field_function = super().get_create_field_function(type)

#         def wrapped_create_field_function(field, options):

#             created_field = create_field_function(field, options)
#             created_field.widget.attrs.update(
#                 # {"class": field.field_classname}
#                 # Important: using the class may be sufficient,
#                 # depending on how your form is being rendered, try this first.
#                 {"field_classname": field.field_classname},
#                 # this is a non-standard attribute
#                 # and will require custom template rendering of your form to work
#                 {"placeholder": field.placeholder},
#             )

#             return created_field

#         return wrapped_create_field_function


class FormPage(EmailFormMixin, FormMixin, ContentPage):
    thank_you_text = RichTextField(blank=True)
    # form_builder = CustomFormBuilder  # use custom form builder to override behaviour

    content_panels = ContentPage.content_panels + [
        # FormSubmissionsPanel(),
        InlinePanel("form_fields", label=_("Form fields")),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="village-input"),
                        FieldPanel("to_address", classname="village-input"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        return form

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["form_fields"] = self.form_fields.all()
        return context

    # def send_mail(self, form):
    #     return 1

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)

    #     # If you need to show results only on landing page,
    #     # You may need to check request.method

    #     results = dict()
    #     # Get information about form fields
    #     data_fields = [(field.clean_name, field.label) for field in self.get_form_fields()]
    #     return context
