import datetime

from dateutil.relativedelta import relativedelta as date_diff
from rest_framework import serializers


def check_birth_date(value):
    age = date_diff(datetime.date.today(), value).years
    if age < 9:
        raise serializers.ValidationError(f"Возраст {age} лет слишком мал")


def check_email_address(value):
    if 'rambler.ru' in value:
        raise serializers.ValidationError("Регистрация с домена rambler.ru запрещена")
