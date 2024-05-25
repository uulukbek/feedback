from rest_framework import serializers
from applications.universities.models import University, Faculty
from applications.feedback.models import Comment
from applications.feedback.serializers import CommentSerializer
from django.db.models import Avg



class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'description']

class UniversitySerializer(serializers.ModelSerializer):
    faculties = FacultySerializer(many=True, read_only=True)

    class Meta:
        model = University
        fields = ['id', 'name', 'location', 'owner', 'phone', 'description', 'price', 'category', 'image', 'faculties']

    def create(self, validated_data):
        request = self.context.get('request')
        university = University.objects.create(**validated_data)
        return university
    
    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     comment = Comment.objects.filter(university=instance.id)
    #     serializer = CommentSerializer(comment, many=True)
    #     comments = serializer.data
        
    #     rep['price'] = float(instance.price) - float(instance.discount/100)*float(instance.price)
    #     rep['likes'] = instance.likes.filter(like=True).count()
    #     rep['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
    #     rep['comment'] = comments
    #     return rep
    






