from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category',
    )
    list_editable = ('category',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Title, TitleAdmin)
