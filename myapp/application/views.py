from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Osoba
from .models import Stanowisko
from .serializers import OsobaSerializer
from .serializers import StanowiskoSerializer
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied



@api_view(['GET'])
def osoba_list(request):
    if request.method == 'GET':
        # Wybierz tylko rekordy należące do zalogowanego użytkownika
        osoby = Osoba.objects.filter(wlasciciel=request.user)
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

# @api_view(['GET', 'PUT', 'DELETE'])
# def osoba_detail(request, pk):
#     try:
#         osoba = Osoba.objects.get(pk=pk)
#     except Osoba.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = OsobaSerializer(osoba)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = OsobaSerializer(osoba, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         osoba.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#

@api_view(['GET'])
def osoba_detail(request, pk):
    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Person
    :return: Response (with status and/or object/s data)
    """
    try:
        person = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Person.
    """
    if request.method == 'GET':
        person = Osoba.objects.get(pk=pk)
        serializer = OsobaSerializer(person)
        return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def osoba_update(request, pk):
    try:
        person = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = OsobaSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def osoba_delete(request, pk):
    try:
        person = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'POST'])
def stanowisko_list(request):
    if request.method == 'GET':
        stanowiska = Stanowisko.objects.all().order_by('id')
        serializer = StanowiskoSerializer(stanowiska, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StanowiskoSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def stanowisko_detail(request, pk):
    try:
        stanowisko = Stanowisko.objects.get(pk=pk)
    except Stanowisko.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StanowiskoSerializer(stanowisko)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StanowiskoSerializer(stanowisko, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stanowisko.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def stanowisko_members(request, pk):
    try:
        stanowisko = Stanowisko.objects.get(pk=pk)
        members = Osoba.objects.filter(stanowisko=stanowisko)
        serializer = OsobaSerializer(members, many=True)
        return Response(serializer.data)
    except Stanowisko.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Dekorator sprawdzający uprawnienie
def has_view_osoba_permission(user):
    return user.has_perm('myapp.view_osoba')

def can_view_other_persons(user):
    return user.has_perm('myapp.can_view_other_persons')

# Prosty widok
@user_passes_test(lambda u: has_view_osoba_permission(u) or can_view_other_persons(u))
def osoba_view(request):
    try:
        if can_view_other_persons(request.user):
            # Użytkownik ma uprawnienie do przeglądania innych osób
            osoby = Osoba.objects.all()
        else:
            # Użytkownik może przeglądać tylko swoje osoby
            osoby = Osoba.objects.filter(wlasciciel=request.user)

        # Tworzymy odpowiedź HttpResponse z danymi
        response_data = "\n".join([f"{osoba.imie} {osoba.nazwisko}" for osoba in osoby])
        return HttpResponse(response_data)
    except Osoba.DoesNotExist:
        return HttpResponse("Brak danych dla tego użytkownika.")