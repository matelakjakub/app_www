from django.contrib import admin

# Register your models here.
from .models import Team,Person,Osoba,Stanowisko

class OsobaAdmin(admin.ModelAdmin):
    # zmienna list_display przechowuje listę pól, które mają się wyświetlać w widoku listy danego modelu w panelu administracynym
    list_display = ['imie', 'nazwisko','plec','stanowisko_with_id','data_dodania']
    list_filter = ['plec', 'stanowisko', 'data_dodania']
    ordering = ['imie', 'nazwisko']

    @admin.display()
    def stanowisko_with_id(self, obj):
        return f'{obj.stanowisko} ({obj.stanowisko.id})'

    stanowisko_with_id.short_description = 'Stanowisko (id)'

admin.site.register(Team)
admin.site.register(Person)
admin.site.register(Osoba, OsobaAdmin)
admin.site.register(Stanowisko)
