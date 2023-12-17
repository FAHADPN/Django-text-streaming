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
from openai import OpenAI  # for OpenAI API calls
import time  # for measuring time duration of API calls

client = OpenAI(
    # This is the default and can be omitted
    api_key='OPENAI_API_KEY',
)

class StreamGeneratorView(APIView):

    def name_generator(self,fake,message):
        name = fake.name()
        
        for i in range(5):
            for i in name:
                yield i
                time.sleep(0.1)
            name = fake.name() + message

    def openaichatter(self,message):

        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}],
            stream=True,
        )

        for chunk in stream:
            yield chunk.choices[0].delta.content or ""

    def get(self,request): 
        fake = Faker()
        name = self.name_generator(fake)
        response =  StreamingHttpResponse(name,status=200, content_type='text/event-stream')
        response['Cache-Control']= 'no-cache'
        return response
    
    def post(self,request):
        print(request.data)
        # fake = Faker()
        # name = self.name_generator(fake,request.data['message'])
        # response =  StreamingHttpResponse(name,status=200, content_type='text/event-stream')
        if request.data['message'] == '':
            chat = self.openaichatter('Send a greetings message for me and ask me to ask you a question to continue a conversation')
        else:
            chat = self.openaichatter(request.data['message'])
        response =  StreamingHttpResponse(chat,status=200, content_type='text/event-stream')
        return response

class HomeView(View):

    def get(self,request):
        return render(request,'home.html')