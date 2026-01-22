import time

from django.core.cache import cache
from django.tasks import task


def register_key(phone):
    return f"register:{phone}"


@task
def send_sms_code(phone, code):
    key = register_key(phone)
    if not cache.get(key):
        cache.set(key, code, 60)
        print(f" 📞 {phone} = {code} sending !!!")
    else:
        print('hali vaqt bor!')
