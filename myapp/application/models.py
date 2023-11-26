from django.db import models

MONTHS = models.IntegerChoices('Miesiace','Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')

SHIRT_SIZES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)


class Team(models.Model):
    name = models.CharField(max_length=60)
    city = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    month_added = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name



class Stanowisko(models.Model):
    nazwa = models.TextField(blank=False, null=False)
    opis = models.TextField(blank = True, null= True)


    def __str__(self):
        return f"{self.nazwa}"

    class Meta:
        db_table = "Stanowisko"
class Osoba(models.Model):


    imie = models.TextField(blank=False, null=False)
    nazwisko = models.TextField(blank=False, null=False)

    class Plec(models.IntegerChoices):
        MEZCZYZNA = 1
        KOBIETA = 2
        INNE = 3

    plec_choices = models.IntegerChoices("plec", "MEZCZYZNA KOBIETA INNE")
    plec = models.IntegerField(choices=plec_choices.choices)
    stanowisko = models.ForeignKey(Stanowisko, on_delete=models.CASCADE)
    data_dodania = models.DateField(auto_now_add=True, editable=False)
    wlasciciel = models.ForeignKey('auth.User', on_delete=models.CASCADE)



    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

    class Meta:
        # Ogranicz dostęp do rekordów tylko dla właścicieli
        permissions = [
            ("view_osoba", "Can view osoba owned by user"),
            ("can_view_other_persons", "Can view other persons"),
        ]

    class Meta:
        db_table = "Osoba"
        ordering = ('nazwisko',)






