from django.shortcuts import render,redirect
from django.http import JsonResponse
import csv 
import boto3
from django.conf import settings
from rest_framework.decorators import api_view
from .serializers import UserSerializer,Meterserializer
from .models import User,Meter
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator

api_view(['GET','POST'])
def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        # print("user -= ",user.password)
        if user is not None:
            if check_password(password,user.password):
                request.session['user'] = email
                return render(request,'ui_page.html',{'user':user})
            else:
                return render(request,'login.html',{'error':"Wrong Password"})
        else:
            return render(request,'login.html',{'error':"Invalid username or password"})    
    else:
        return JsonResponse({"status":'Error'})


api_view(['GET','POST'])
def signup(request):
    if request.method=="GET":
        return render(request,'signup.html')
    elif request.method=="POST":
        serializer = UserSerializer(data=request.POST)
        # print("value = ",serializer)
        # print("value = ",serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
        else:
            # print("error=",serializer.errors)
            return render(request,'signup.html')
    else:
        return JsonResponse({"status":'Error'})

def all_Data(request):
    
    ITEMS_PER_PAGE = 50
    items = Meter.objects.all()
    paginator = Paginator(items, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'all_data.html',{'page_obj': page_obj})


def home(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request,'ui_page.html')
    # return render(request,'ui_page.html')

def logout(request):
    # Delete the user session
    del request.session['user']
    return redirect('login')    

@csrf_exempt
def upload_file(request):
    if request.method=="POST":
        file = request.FILES.get('file')
        # print(file)
        if file:
            decoded_file = file.read().decode('cp1252').splitlines()
            reader = csv.reader(decoded_file)
            print("whole data = ",reader)
            for row in reader:
                # print(row)
                serial_number, inc_name, proprietor_name, meter_measurement, diff_units, avg_unit, power_utility_index, power_station_name, usage_type, csi_index = row
                if csi_index=="":
                    csi_index=0
                meter = Meter(
                    serial_number=serial_number,
                    inc_name=inc_name,
                    proprietor_name=proprietor_name,
                    meter_measurement=float(meter_measurement),
                    diff_units=float(diff_units),
                    avg_unit=float(avg_unit),
                    power_utility_index=float(power_utility_index),
                    power_station_name=power_station_name,
                    usage_type=usage_type,
                    csi_index=float(csi_index)
                )
                meter.save()
            s3 = boto3.client('s3',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,region_name=settings.AWS_S3_REGION_NAME)
            s3.upload_fileobj(file,settings.AWS_STORAGE_BUCKET_NAME,file.name)
            return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'ERROR'}) 