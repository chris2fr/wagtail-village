from django import template


register = template.Library()


@register.filter
def field_class_from_name(field_name, form_fields):
    class_corres = {
        "singleline": "input",
        "multiline": "none",
        "email": "input",
        "number": "input",
        "url": "input",
        "checkbox": "none",
        "checkboxes": "none",
        "dropdown": "input",
        "radio": "none",
        "date": "input",
        "datetime": "input",
        "hidden": "none",
    }
    """Returns the field type for the given field name."""
    for form_field in form_fields:
        if form_field.clean_name == field_name:
            return class_corres[form_field.field_type]
    return "input"
