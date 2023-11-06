from rest_framework import serializers
from .models import Person, Team, Stanowisko, Osoba, MONTHS, SHIRT_SIZES

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class OsobaSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        read_only=True,
    )
    imie = serializers.CharField(
        required=True,
    )
    nazwisko = serializers.CharField(
        required=True,
    )
    plec = serializers.ChoiceField(
        choices=Osoba.Plec.choices,
        default=Osoba.Plec.MEZCZYZNA,
    )
    stanowisko = serializers.PrimaryKeyRelatedField(
        queryset=Stanowisko.objects.all(),
    )
    data_dodania = serializers.DateField(
        read_only=True,
    )

    def validate_imie(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Imię może zawierać tylko litery.")
        return value

    def validate_data_dodania(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Data dodania nie może być z przyszłości.")
        return value
    def create(self, validated_data):
        return Osoba.objects.create(**validated_data)

    # przesłonięcie metody update() z klasy serializers.Serializer
    def update(self, instance, validated_data):
        instance.imie = validated_data.get('imie', instance.imie)
        instance.nazwisko = validated_data.get('nazwisko', instance.nazwisko)
        instance.plec = validated_data.get('plec', instance.plec)
        instance.stanowisko = validated_data.get('stanowisko', instance.stanowisko)
        instance.save()
        return instance


        # def validate_imie(self, value):
        #     if not value.isalpha():
        #         raise serializers.ValidationError(
        #             "Imie osoby musi składać się tylko z liter!"
        #         )
        #
        # def clean(self):

class StanowiskoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanowisko
        fields = [
            'id',
            'nazwa',
            'opis',
        ]
        read_only_fields = [
            'id',
        ]