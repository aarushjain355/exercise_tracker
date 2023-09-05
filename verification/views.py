from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from .serializers import UserSerializer, GoalsSerializer, NutritionSerializer, ExerciseSerializer, BodyPartSerializer, InspirationalVideoSerializer, RecpieSerializer, serializer1
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import User, GoalsProfileQuestions, NutritionProfileQuestions, Body_Part, Exercise, InspirationalVideoLink, Recipe, example
import requests
from .algorithms import calculate_calories, get_macronutrient_ratios
from bs4 import BeautifulSoup

# Create your views here.

EXERCISE_API_KEY = "DQkj6i8AxB/G72a+bC7mLw==fM8MQJZua9k44Lz9"
NUTRITION_API_KEY = "84d12c98deeb46cbabcc842ea5b0af67"
YOUTUBE_API_KEY = "AIzaSyCpbsfCRnsgdzjN5-uEslF66YqWbo7AtsE"


class UserRegistrationView2(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        print(request.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class Retrieve_User(APIView):
    
    def get(self, request, email):

        try:
            user = User.objects.get(email=email)
            serializer = UserSerializer(user)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error" : "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
class UserGoalsFormCreate(CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = GoalsProfileQuestions.objects.all()
    serializer_class = GoalsSerializer

    def perform_create(self, serializer):
        print(self.request.data)
        instance = serializer.save()



class UserGoalsFormCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = GoalsProfileQuestions.objects.all()
    serializer_class = GoalsSerializer

class createview(CreateAPIView):

    queryset = example.objects.all()
    serializer_class = serializer1


class RecipeCRUD(CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Recipe.objects.all()
    serializer_class = RecpieSerializer

class UserNutritionFormCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = NutritionProfileQuestions.objects.all()
    serializer_class = NutritionSerializer

class UserNutritionFormCreate(CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = NutritionProfileQuestions.objects.all()
    serializer_class = NutritionSerializer


class BodyPartCRUD(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        body_parts = user.body_part_set.all()

        serializer = BodyPartSerializer(body_parts, many=True)
        return Response(serializer.data)

class ExerciseCRUD(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        body_parts = user.body_part_set.all()

        exercise_list = []
        for body_part in body_parts:
            exercises = body_part.exercise_set.all()
            exercise_list.extend(exercises)

        serializer = ExerciseSerializer(exercise_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class userCRUD(RetrieveUpdateDestroyAPIView):


    queryset = User.objects.all()
    serializer_class = UserSerializer
class ExerciseCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class InspirationalVideoCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = InspirationalVideoLink.objects.all()
    serializer_class = InspirationalVideoSerializer

class BodyPartCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Body_Part.objects.all()
    serializer_class = BodyPartSerializer

class FitnessAPIView1(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        exercises_list = ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms", "glutes", "hamstrings", "lats", "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"]
        user = request.user
        goals = GoalsProfileQuestions.objects.get(user=user)
        print(goals)

        if goals.exists():
            level = goals.first().fitness_level
            type = goals.first().fitness_goal
            for body_part in exercises_list:
                muscle = body_part
                api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&type={}&difficulty={}'.format(
                        muscle, type, level
                )

                bodyPart = Body_Part(name=muscle)
                bodyPart.save()
                print("HELLO BITCH ASS FUCKER")
                response = requests.get(api_url, headers={'X-Api-Key': EXERCISE_API_KEY})

                if response.status_code != requests.codes.ok:
                     return Response({'error': 'Error fetching data from the API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                response1 = response.json()
                for exercise in response1:
                    exercise_name = exercise.get('name')
                    exercise_type = exercise.get('type')
                    exercise_muscle = exercise.get('muscle')
                    exercise_equipment = exercise.get('equipment')
                    exercise_difficulty = exercise.get('difficulty')
                    exercise_instructions = exercise.get('instructions')
                
                    exercise = Exercise(name=exercise_name, type=exercise_type, 
                                        muscle=exercise_muscle, equipment=exercise_equipment,
                                        difficulty=exercise_difficulty, instructions=exercise_instructions)

                    exercise.save()
                
                
                return Response({'message' : "Exercise data saved successfully"}, status=status.HTTP_200_OK)
        else:
             print("whats up bitch")
             return Response({'message': 'No goals found for the user'}, status=status.HTTP_400_BAD_REQUEST)

class FitnessAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, counter):
        exercises_list = ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms", "glutes", "hamstrings", "lats", "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"]
        user = request.user
        print(user)
        goals = GoalsProfileQuestions.objects.get(identification=counter)
        print(goals)

    
        level = goals.fitness_level
        type = goals.fitness_goal
        for body_part in exercises_list:
            muscle = body_part
            api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&type={}&difficulty={}'.format(
                    muscle, type, level
            )

            bodyPart = Body_Part(name=muscle)
            bodyPart.save()
            print("HELLO BITCH ASS FUCKER")
            response = requests.get(api_url, headers={'X-Api-Key': EXERCISE_API_KEY})

            if response.status_code != requests.codes.ok:
                return Response({'error': 'Error fetching data from the API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response1 = response.json()
            for exercise in response1:
                exercise_name = exercise.get('name')
                exercise_type = exercise.get('type')
                exercise_muscle = exercise.get('muscle')
                exercise_equipment = exercise.get('equipment')
                exercise_difficulty = exercise.get('difficulty')
                exercise_instructions = exercise.get('instructions')
                
                exercise = Exercise(name=exercise_name, type=exercise_type, 
                    muscle=exercise_muscle, equipment=exercise_equipment,
                    difficulty=exercise_difficulty, instructions=exercise_instructions)

                exercise.save()
                
                
        return Response({'message' : "Exercise data saved successfully"}, status=status.HTTP_200_OK)
        
class FitnessAPIView2(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        exercises_list = ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms", "glutes", "hamstrings", "lats", "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"]
        user = request.user
        print(user)

        try:
            goals = GoalsProfileQuestions.objects.get(user=user)
            level = goals.fitness_level
            type = goals.fitness_goal
            for body_part in exercises_list:
                muscle = body_part
                api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&type={}&difficulty={}'.format(
                        muscle, type, level
                )

                bodyPart = Body_Part(name=muscle)
                bodyPart.save()
                print("HELLO BITCH ASS FUCKER")
                response = requests.get(api_url, headers={'X-Api-Key': EXERCISE_API_KEY})

                if response.status_code != requests.codes.ok:
                     return Response({'error': 'Error fetching data from the API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                response1 = response.json()
                for exercise in response1:
                    exercise_name = exercise.get('name')
                    exercise_type = exercise.get('type')
                    exercise_muscle = exercise.get('muscle')
                    exercise_equipment = exercise.get('equipment')
                    exercise_difficulty = exercise.get('difficulty')
                    exercise_instructions = exercise.get('instructions')
                
                    exercise = Exercise(name=exercise_name, type=exercise_type, 
                                        muscle=exercise_muscle, equipment=exercise_equipment,
                                        difficulty=exercise_difficulty, instructions=exercise_instructions)

                    exercise.save()
                
                
                return Response({'message' : "Exercise data saved successfully"}, status=status.HTTP_200_OK)

        except GoalsProfileQuestions.DoesNotExist:
        
             print("whats up bitch")
             return Response({'message': 'No goals found for the user'}, status=status.HTTP_400_BAD_REQUEST)

class NutritionAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        nutrition_profile = NutritionProfileQuestions.objects.get(user=user)
        goals_profile = GoalsProfileQuestions.objects.get(user=user)

        calories = calculate_calories(user.age, user.gender, user.weight, user.height, goals_profile.body_type,
                                      goals_profile.body_fat_percentage_goal, goals_profile.activity_level)
        
        ratios_list = get_macronutrient_ratios(goals_profile.primary_goal, nutrition_profile.num_of_meals,
                                               user.gender)
        
        min_protein_grams = ratios_list[0] * calories / 4 / nutrition_profile.num_of_meals
        max_protein_grams = ratios_list[1] * calories / 4 / nutrition_profile.num_of_meals
        min_carb_grams = ratios_list[2] * calories / 4 / nutrition_profile.num_of_meals
        max_carb_grams = ratios_list[3] * calories / 4 / nutrition_profile.num_of_meals
        min_fat_grams = ratios_list[4] * calories / 9 / nutrition_profile.num_of_meals
        max_fat_grams = ratios_list[5] * calories / 9 / nutrition_profile.num_of_meals

        api_url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
                
                "apiKey" : NUTRITION_API_KEY,
                "number" : 5,
                "minCarbs" : min_carb_grams,
                "maxCarbs" : max_carb_grams,
                "minProtein" : min_protein_grams,
                "maxProtein" : max_protein_grams,
                "minCalories" : calories - 100,
                "maxCalories" : calories + 100,
                "minFat" : min_fat_grams,
                "maxFat" : max_fat_grams,
                "minVitaminA" : ratios_list[6],
                "maxVitaminA" : ratios_list[6],
                "minFiber" : ratios_list[7],
                "maxFiber" : ratios_list[8]

        }
        response = requests.get(f'{api_url}', params=params)
        if response.status_code == 200:
            data = response.json()
    # Process the response data (data contains the API response)
        else:
            print('Error:', response.status_code)
            
        for result in data.get("results", []):
            recipe_id = result.get("id")
            title = result.get("title")
            image = result.get("image")
            image_type = result.get("imageType")

            # Create a new Recipe instance
            recipe = Recipe.objects.create(
                recipe_id=recipe_id,
                title=title,
                image=image,
                image_type=image_type
            )

            # You can perform additional processing or save the instance to the database
            recipe.save()



class inspirational_videos_youtube_api(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        try:
            user = request.user
            profile = GoalsProfileQuestions.objects.get(user=user)
            inspirations = profile.inspirations
            for person_name in inspirations:
                search_query = person_name

# URL for the YouTube Data API search endpoint
                search_url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&part=snippet&type=video&q={search_query}"

                # Send GET request to the API endpoint
                response = requests.get(search_url)
                data = response.json()

                # Extract video IDs from the search results
                video_ids = [item["id"]["videoId"] for item in data["items"]]

                # Construct video URLs using the video IDs
                video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids[:5]]

                for url in video_urls:

                    video = InspirationalVideoLink(user=user, video_link=url)
                    video.save()
                return Response({'message': 'Web scraping completed successfully'}, status=status.HTTP_200_OK)
        except GoalsProfileQuestions.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
