from application.models import Osoba, Stanowisko
from application.serializers import OsobaSerializer, StanowiskoSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# 1.Stworzenie nowej instancji klasy Osoba
- osoba = Osoba(imie='Jakub', nazwisko='Matelak', plec='1', stanowisko=Stanowisko.objects.get(nazwa='Malarz'))
- osoba.save()
# 2.Inicjalizacja serializera
- serializer = OsobaSerializer(osoba)
- serializer.data
#### Output
{'id': 6, 'imie': 'Jakub', 'nazwisko': 'Matelak', 'plec': 1, 'stanowisko': 2, 'data_dodania': '2023-11-03'}

# 3.Serializacja danych do JSON
- content = JSONRenderer().render(serializer.data)
- content
#### Output
b'{"id":6,"imie":"Jakub","nazwisko":"Matelak","plec":1,"stanowisko":2,"data_dodania":"2023-11-03"}'

# Walidacja
- import io
- stream = io.BytesIO(content)
- data = JSONParser().parse(stream)
- deserializer = OsobaSerializer(data=data)
- deserializer.is_valid()
#### Output
True
- deserializer.fields
#### Output
{'id': IntegerField(read_only=True), 'imie': CharField(required=True), 'nazwisko': CharField(required=True), 'plec': ChoiceField(choices=[(1, 'Mezczyzna'), (2, 'Kobieta'), (3, 'Inne')], default=Osoba.PLCI.MEZCZYZNA), 'stanowisko': PrimaryKeyRelatedField(queryset=<QuerySet [<Stanowisko: Piłkarz>, <Stanowisko: Malarz>, <Stanowisko: Piekarz>]>), 'data_dodania': DateField(read_only=True)}
- deserializer.validated_data
#### Output
OrderedDict([('imie', 'Jakub'), ('nazwisko', 'Matelak'), ('plec', 1), ('stanowisko', <Stanowisko: Malarz>)])
- deserializer.save()
<Osoba: Jakub Matelak>
- deserializer.data
{'id': 7, 'imie': 'Jakub', 'nazwisko': 'Matelak', 'plec': 1, 'stanowisko': 2, 'data_dodania': '2023-11-03'}

# 1.Stworzenie nowej instancji klasy Stanowisko
- stanowisko = Stanowisko(nazwa='Rezydent', opis='Rezydent klubu')
- stanowisko.save()

# 2.Inicjalizacja serializera
- serializer = StanowiskoSerializer(stanowisko) 
- serializer.data
#### Output
{'id': 4, 'nazwa': 'Rezydent', 'opis': 'Rezydent klubu'}

# 3.Serializacja danych do JSON
- content = JSONRenderer().render(serializer.data)
- content
#### Output
b'{"id":4,"nazwa":"Rezydent","opis":"Rezydent klubu"}'

# Walidacja
- import io
- stream = io.BytesIO(content)
- data = JSONParser().parse(stream)
- deserializer = StanowiskoSerializer(data=data)
- deserializer.is_valid()
#### Output
True
- deserializer.fields
#### Output
{'id': IntegerField(label='ID', read_only=True), 'nazwa': CharField(), 'opis': CharField(allow_blank=True, required=False)}
- deserializer.validated_data
#### Output
OrderedDict([('nazwa', 'Rezydent'), ('opis', 'Rezydent klubu')])
- deserializer.save()
<Stanowisko: Rezydent>
- deserializer.data
{'id': 5, 'nazwa': 'Rezydent', 'opis': 'Rezydent klubu'}