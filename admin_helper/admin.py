from django.contrib import admin


class AdminHelperAdmin(admin.ModelAdmin):

    class Media:
        js = (
            '/static/js/admin_helper/jquery.js',
            '/static/js/admin_helper/script.js',
        )
        css = {
            'all': ('/static/css/admin_helper/style.css', )
        }
