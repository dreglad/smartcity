from django.contrib.admin import ModelAdmin


class SmartCityModelAdmin(ModelAdmin):
    class Media:
        css = {
            "all": ("css/smartcityadmin.css",)
        }