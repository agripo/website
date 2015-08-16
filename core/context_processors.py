from core.models import News


def cookies_notification(request):
    return {'cookies_notification_shown': 'cookies_notification_shown' in request.session}

def last_news_box(request):
    return {'last_news': News.get_last()}
