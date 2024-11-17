# image_formats.py
from wagtail.images.formats import Format, register_image_format


class FaireMainOriginalImageFormat(Format):
    def image_to_html(self, image, alt_text, extra_attributes=None):
        # the custom HTML representation of your image here
        # in Format, the image's rendition.img_tag(extra_attributes) is used to generate the HTML
        # representation

        custom_html = "<img src='{{ image.url }}' alt='{{ alt_text }}' class='original'>"

        return custom_html


register_image_format(FaireMainOriginalImageFormat("original ", "Original", "richtext-image", "original "))
