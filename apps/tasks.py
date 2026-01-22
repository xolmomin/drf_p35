from random import randint

from django.core.cache import cache
from django.tasks import task


def register_key(phone):
    return f"register:{phone}"


@task
def send_sms_code(phone, msg):
    print(f"📞 {phone}\n{msg}")


@task
def register_sms(phone: str):
    code = randint(100000, 999999)
    key = register_key(phone)
    if not cache.get(key):
        cache.set(key, code, 60)

    text = f"""Tasdiqlash kodi: {code}"""
    send_sms_code.enqueue(phone, text)
