from rest_framework import serializers
from applications.universities.models import University, Faculty


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'description']

class UniversitySerializer(serializers.ModelSerializer):
    faculties = FacultySerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'location', 'owner', 'phone', 'description', 'price', 'category', 'image', 'faculties']
