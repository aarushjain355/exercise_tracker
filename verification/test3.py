import requests


EXERCISE_API_KEY = "DQkj6i8AxB/G72a+bC7mLw==fM8MQJZua9k44Lz9"
exercises_list = ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms", "glutes", "hamstrings", "lats", "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"]
        
for body_part in exercises_list:
    muscle = body_part
    type = "powerlifting"
    level = "beginner"
    api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&type={}&difficulty={}'.format(
        muscle, type, level
    )

    response = requests.get(api_url, headers={'X-Api-Key': EXERCISE_API_KEY})

    response1 = response.json()
    for exercise in response1:
        print(exercise.get("name"))
