from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import MinValueValidator, MinLengthValidator


class User(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    weight = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_month = models.CharField(max_length=244)
    password = models.CharField(max_length=244)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class example(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

class GoalsProfileQuestions(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    body_type = models.CharField(max_length=135)
    fitness_goal = models.CharField(max_length=135)
    fitness_level = models.CharField(max_length=135)
    primary_goal = models.CharField(max_length=135)
    body_fat_percentage_goal = models.PositiveIntegerField(default=10, validators=[MinValueValidator(0)])
    activity_level = models.CharField(max_length=135)
    motivation = models.CharField(max_length=135)
    identification = models.PositiveIntegerField(default=0)
    


class NutritionProfileQuestions(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    dietary_restrictions = models.CharField(max_length=135)
    num_of_meals = models.CharField(max_length=135)
    macronutrient_goals = models.CharField(max_length=135)
    target_daily_calorie_intake = models.PositiveIntegerField(default=2000)
    



class Body_Part(models.Model):

    name = models.CharField(max_length=253)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    
class Exercise(models.Model):

    name = models.CharField(max_length=135)
    type = models.CharField(max_length=135)
    muscle = models.ForeignKey(Body_Part, on_delete=models.CASCADE)
    equipment = models.CharField(max_length=135)
    difficulty = models.CharField(max_length=135)
    instructions = models.TextField(validators=[MinLengthValidator(15)])


class InspirationalVideoLink(models.Model):
    user = models.ManyToManyField("User")
    video_link = models.URLField()

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.PositiveIntegerField(unique = True)
    title = models.CharField(max_length=255)
    image = models.URLField()
    image_type = models.CharField(max_length=10)
    

class StravaToken(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    
# Create your models here.
