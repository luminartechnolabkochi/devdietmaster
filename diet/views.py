from django.shortcuts import render

from django.views.generic import View
# Create your views here.


class DietPlanView(View):

    def get(self,request,*args,**kwargs):

        return render(request,"profile.html")
    
    def post(self,request,*args,**kwargs):

        form_data = request.POST

        height_in_cm = form_data.get("height")

        weight_in_kg = form_data.get("weight")

        gender = form_data.get("gender")

        age = form_data.get("age")

        activitylevel = form_data.get("activitylevel")

        target=form_data.get("target")

        duration=form_data.get("duration")

        print(height_in_cm,weight_in_kg,gender,age,activitylevel,duration,target)

        return render(request,"profile.html")




    
