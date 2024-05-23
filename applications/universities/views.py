from django.shortcuts import render
from rest_framework import viewsets
from applications.universities.serializers import UniversitySerializer, FacultySerializer
from applications.universities.models import University, Faculty

class UniversitiesViewSet(viewsets.ModelViewSet):
    serializer_class = UniversitySerializer
    queryset = University.objects.all()
    filterset_fields = ['category']
    search_fields = ['name']
    order_fields = ['price']



class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
