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

    




