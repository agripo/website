from core.models import News


def cookies_notification(request):
    return {'cookies_notification_shown': 'cookies_notification_shown' in request.session}

def last_news_box(request):
    return {'last_news': News.get_last()}

def bd_webdoc_slideshow(request):
    return {
        'bd_webdoc_slideshow': {
            'carousel_id': 'bd_webdoc_carousel',
            'images': [
                {'src': '/static/img/shared/webdoc.jpg', 'alt': "Webdocumentaire", "caption": "", "title": "Webdocumentaire"},
                {'src': '/static/img/shared/bd.jpg', 'alt': "Bande dessinée", "caption": "", "title": "Bande dessinée"},
            ]
        }
    }
