def cookies_notification(request):
    return {'cookies_notification_shown': 'cookies_notification_shown' in request.session}
