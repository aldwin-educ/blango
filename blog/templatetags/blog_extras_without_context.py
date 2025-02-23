from django import template
from django.contrib.auth.models import User
#from django.utils.html import escape
#from django.utils.safestring import mark_safe
from django.utils.html import format_html

register = template.Library()

@register.filter
def author_details(author, current_user=None):
  if not isinstance(author, User):
      # return empty string as safe default
      return ""
  '''
  if author.first_name and author.last_name:
      name = escape(f"{author.first_name} {author.last_name}")
  else:
      name = escape(f"{author.username}")

  if author.email:
      email = escape(author.email)
      prefix = f'<a href="mailto:{email}">'
      suffix = "</a>"
  else:
      prefix = ""
      suffix = ""

  return mark_safe(f"{prefix}{name}{suffix}")
  '''

  if author == current_user:
    return format_html("<strong>me</strong>")

  if author.first_name and author.last_name:
      name = f"{author.first_name} {author.last_name}"
  else:
      name = f"{author.username}"

  if author.email:
      prefix = format_html('<a href="mailto:{}">', author.email)
      suffix = format_html("</a>")
  else:
      prefix = ""
      suffix = ""

  return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">',extra_classes)

@register.simple_tag
def endrow():
    return format_html("</div>")

@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">',extra_classes)

@register.simple_tag
def endcol():
    return format_html("</div>")    