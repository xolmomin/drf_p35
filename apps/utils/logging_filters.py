from .threadlocals import get_current_request


class ClientIPFilter:
    def filter(self, record):
        request = get_current_request()
        if request:
            xff = request.META.get('HTTP_X_FORWARDED_FOR')
            record.ip = xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')
        else:
            record.ip = '-'
        return True
