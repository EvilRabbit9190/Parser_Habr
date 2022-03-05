from django.contrib import admin

from .models import Hubs


class HubsAdmin(admin.ModelAdmin):
    list_display = ("header", "date", "link_post", "author_name", "author_link", "content", "post_id")
    list_filter = ("date", "author_name")


admin.site.site_header = "Административная панель Парсера"
admin.site.index_title = "Модели"
admin.site.register(Hubs, HubsAdmin)
