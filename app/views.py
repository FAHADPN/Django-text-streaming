from django.shortcuts import render
import time
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.views.generic import View  
from django.shortcuts import render
from django.http import StreamingHttpResponse
from rest_framework import status
from faker import Faker

class StreamGeneratorView(APIView):

    def name_generator(self,fake):
        name = fake.name()
        while True:
            for i in name:
                yield i
                # time.sleep(0.1)
            name = fake.name()

    def get(self,request): 
        fake = Faker()
        name = self.name_generator(fake)
        response =  StreamingHttpResponse(name,status=200, content_type='text/event-stream')
        response['Cache-Control']= 'no-cache',
        return response
    
class HomeView(View):

    def get(self,request):
        return render(request,'index.html')