from django import template
from django.core.urlresolvers import reverse

import datetime


register = template.Library()


class ServerTime(template.Node):

    def __init__(self):
        self.format_time = '%I:%M %a, %Y-%m-%d'

    def render(self, context):
        now = datetime.datetime.now()
        return now.strftime(self.format_time)


@register.tag(name="server_time")
def server_datetime(parser, token):
#    tag_name, format_string = token.split_contents()
    return ServerTime()

INSTAGRAM_USER_URL_TEMPLATE = 'http://instagram.com/{}'


@register.simple_tag
def instagram_url(username):
    return INSTAGRAM_USER_URL_TEMPLATE.format(username)


@register.simple_tag
def url_for_today():
    d = datetime.date.today()
    return reverse(
        'photo-date-view',
        kwargs={'year': d.year, 'month': d.month, 'day': d.day}
    )
