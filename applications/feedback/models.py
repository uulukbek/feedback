from django.db import models
from django.contrib.auth import get_user_model
from applications.universities.models import University
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} - {self.comment[:7]}...' 
    
    
class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(
        validators= [
        MinValueValidator(1),
        MaxValueValidator(10)
        ], blank=True, null= True
    )
    
    def __str__(self) -> str:
        return f'{self.owner} - {str(self.rating)}'
        
   
class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)
      
    def __str__(self) -> str:
        return f'{self.owner} - {str(self.like)}'
      

class Favourite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='favourites')
    favourite = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.owner} - {self.product}'
    
      
      
      
      
      
      
      