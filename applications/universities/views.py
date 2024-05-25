from django.shortcuts import render
from core.universities.viewsets import ModelViewSet
from rest_framework import viewsets
from applications.universities.serializers import UniversitySerializer, FacultySerializer
from applications.universities.permissions import IsUniversityOwnerOrReadOnly, IsFeedbackOwner
from applications.universities.models import University, Faculty
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
import logging


logger = logging.getLogger("main")


class PaginationApiView(PageNumberPagination):
    page_size = 5
    max_page_size = 100
    page_size_query_param = 'university_pages'


class UniversitiesViewSet(ModelViewSet):
    serializer_class = UniversitySerializer
    queryset = University.objects.all()
    filterset_fields = ['category']
    search_fields = ['name']
    order_fields = ['price']


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def get_permissions(self):
        if self.action == 'delete_comment':
            return [IsFeedbackOwner()]
        return super().get_permissions()

    @action(detail=False, methods=['GET'])
    def popular(self, request, *args, **kwargs):
        universities = University.objects.filter(ratings__rating__gt=7.0).distinct()
        print(universities)
        serializer = UniversitySerializer(universities, many=True)
        logger.info("User listing popular.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def recommend(self, request, pk=None):
        category = self.get_object().category
        queryset = University.objects.filter(category=category)
        serializers = UniversitySerializer(queryset, many=True)
        logger.info("User listing recomended university.")
        return Response(serializers.data)



class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
