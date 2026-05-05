from django.shortcuts import render

from django.views.generic import View
# Create your views here.


class DietPlanView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"profile.html")
    
    def post(self,request,*args,**kwargs):

        form_data = request.POST

        height_in_cm = int(form_data.get("height"))

        weight_in_kg = int(form_data.get("weight"))

        gender = form_data.get("gender")

        age = int(form_data.get("age"))

        activitylevel = float(form_data.get("activitylevel",1.2))

        target=int(form_data.get("target"))

        duration=int(form_data.get("duration"))

        print(height_in_cm,weight_in_kg,gender,age,activitylevel,duration,target)


        tdee=daily_calorie_consumption(gender=gender,weight=weight_in_kg,height=height_in_cm,age=age,activitylevel=activitylevel)

        print("TDEE",tdee)

        goal = "weight loss" if weight_in_kg > target else "weight gain"

        diet_plan=generate_kerala_diet_plan(goal=goal,age=age,weight=weight_in_kg,gender=gender,target_weight=target,duration=duration)
      
        print(diet_plan)
        context={
            "tdee":tdee
        }
        return render(request,"profile.html",context)


def daily_calorie_consumption(gender="male",weight=None,height=None,age=None,activitylevel=1.2):

    """
    
    """
    if gender == "male":

        bmr = 10 * weight + 6.25 * height - 5*age + 5

    else:

        bmr = 10 * weight + 6.25 * height - 5*age - 161

    tdee = bmr * activitylevel

    return tdee

    

from google import genai
from google.genai import types

# # pip install -U google-genai
def generate_kerala_diet_plan(goal="weight loss",age =None,weight=None,gender="male",target_weight=None,duration=None):
    
    # Initialize the new Client
    client = genai.Client(api_key="your api key")
    
    # Extract user
   
    
    prompt = f"Create a Kerala-style {goal} diet plan.User: {gender}, {age}yrs, {weight}kg. Target: {target_weight}kg in {duration} months"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a Kerala Nutritionist. Return ONLY JSON.",
                response_mime_type="application/json",
                # This schema ensures your frontend never breaks
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "daily_calories": {"type": "NUMBER"},
                        "diet_plan": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "day": {"type": "STRING"},
                                    "meals": {"type": "ARRAY", "items": {"type": "STRING"}}
                                }
                            }
                        }
                    }
                }
            )
        )
        return response.parsed
    except Exception as e:
        return e

# generate_kerala_diet_plan(goal="weight loss",age=32,weight=75,gender="male",target_weight=68,duration=4)




# prompt = f"""
#     Act as a Clinical Nutritionist. Create a Kerala-style weight loss diet plan.
#     User: {"male"}, {32}yrs, {64}kg. Target: {60}kg in 2 months.
    
#     Format the output strictly as a JSON object with these keys:
#     - "daily_calories": (int)
#     - "nutritional_advice": (string)
#     - "weekly_plan": (list of 7 objects with keys: "day", "breakfast", "lunch", "snack", "dinner")
#     - "kerala_tips": (list of strings)

#     Use traditional Kerala foods (Matta rice, Thoran, Fish curry, etc.). 
#     Ensure portions are specific (e.g., "1/2 cup Matta rice"). 
#     Return ONLY the JSON. No preamble.
#     """






# def process_food_image():

#         food_image = self.request.FILES.get('food_image')

#         genai.configure(api_key = '')

#         image_bytes = food_image.read()

#         model = genai.GenerativeModel("gemini-2.5-flash",
#                                       generation_config={
#                                           "response_mime_type": "application/json"
#                                       })

#         prompt = """
        
#         identify this food item and return the response  strictly  and only in this json format
#         {
#          "food_name" :"",
#          "quantity" : "",
#          "calories" : ""
#         }

#         """

#         response = model.generate_content([prompt, {'mime_type':food_image.content_type, 'data':image_bytes} ])

#         result = response.text

#         data = json.loads(result)




# print(generate_kerala_diet_plan(goal="weight loss",age=19,gender="male",target_weight=80,duration=4))