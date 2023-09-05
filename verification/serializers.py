from rest_framework import serializers
from .models import User, GoalsProfileQuestions, NutritionProfileQuestions, Exercise, Body_Part, InspirationalVideoLink, Recipe, StravaToken, example


class UserSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(write_only=True)

    class Meta:

        model = User
        fields = ["email", "first_name", "last_name", "age", "height", "weight", "gender", "password", "confirm_password"]
        #extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        
        return data

    def validate_age(self, value):
        if value < 18:

            raise serializers.ValidationError("Age must be at least 18 years old")
        
    def create(self, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
        

class GoalsSerializer(serializers.ModelSerializer):

    class Meta:

        model = GoalsProfileQuestions
        fields = "__all__"

class serializer1(serializers.ModelSerializer):
    class Meta:

        model = example
        fields = ["first_name", "last_name"]

class RecpieSerializer(serializers.ModelSerializer):

    class Meta:

        model = Recipe
        fields = "__all__"   

class NutritionSerializer(serializers.ModelSerializer):

    class Meta:

        model = GoalsProfileQuestions
        fields = "__all__"


class InspirationalVideoSerializer(serializers.ModelSerializer):

    class Meta:

        model = InspirationalVideoLink
        fields = "__all__"

    

class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:

        model = Exercise
        fields = "__all__"


class BodyPartSerializer(serializers.ModelSerializer):

    class Meta:

        model = Body_Part
        fields = "__all__"

    


class StravaTokenSerializer(serializers.ModelSerializer):

    class Meta:

        model = StravaToken
        fields = "__all__"