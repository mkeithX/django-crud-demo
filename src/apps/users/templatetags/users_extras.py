from django import template
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils import timezone
import math
from datetime import datetime

register = template.Library()


@register.filter
def time_ago(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        seconds = diff.seconds
        if seconds == 1:
            return str() + " Just now"
        else:
            return str(seconds) + " seconds ago"
        # minutes
    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        minutes = math.floor(diff.seconds / 60)
        if minutes == 1:
            return str() + " about a minute ago"
        else:
            return str(minutes) + " minutes ago"
    # hours
    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        hours = math.floor(diff.seconds / 3600)
        if hours == 1:
            return str() + " about an hour ago"
        else:
            return str(hours) + " hours ago"

    # days
    if diff.days >= 1 and diff.days < 7:
        days = diff.days
        if days == 1:
            return str() + " Yesterday"
        else:
            return str(days) + " days ago"
    # WEEKS
    if diff.days >= 7 and diff.days < 30:
        weeks = math.floor(diff.days / 7)
        if weeks == 1:
            return str() + " about a week ago"
        else:
            return str(weeks) + " weeks ago"
    # months
    if diff.days >= 30 and diff.days < 365:
        months = math.floor(diff.days / 30)
        if months == 1:
            return str() + " about a month ago"
        else:
            return str(months) + " months ago"
    # years
    if diff.days >= 365:
        years = math.floor(diff.days / 365)
        if years == 1:
            return str() + " about a year ago"
        else:
            return str(years) + " years ago"


@register.filter
def mask_email(email):
    name, domain = email.split("@")

    if len(name) > 5:
        masked_name = name[:3]

    else:
        masked_name = name[:0]

    return "%s*****@%s" % (masked_name, domain)


@register.filter
def time_based_greeting(value):
    current_hour = datetime.now().hour

    if current_hour < 12:
        return "Good morning"
    elif current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"