# from django import template
# from lesgv.models import BlogPosts

# register = template.Library()

# # @register.inclusion_tag('lesgv/tags/blog_posts.html', takes_context=True)
# # @register.simple_tag
# @register.inclusion_tag('lesgv/tags/blog_posts.html')
# def blog_posts(params={}):
#     return {
#         'posts': lesgv.services.get_blog_posts(lesgv.services.ProcessGhostParams(params))
#     }