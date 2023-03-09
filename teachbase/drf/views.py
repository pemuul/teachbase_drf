from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets

from .models import Test
from .serializer import TestSerializer

# Create your views here.



class DRF_API(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer    


class TEACHBASE_API(APIView):
    def get(self, request):
        auth_token='aBRtpk6DJLAgDkF8UqiDpCAgEIAd2rZmXqNpDGDrwdg'
        hed = {'Authorization': 'Bearer ' + auth_token}
        data = {}

        url = 'https://go.teachbase.ru/endpoint/v1/courses'
        response = requests.get(url, json=data, headers=hed)

        return Response({'post' : response.json()})

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post' : serializer.data})
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error' : 'Method PUT not allowed!'})
        
        try:
            instanse = Test.objects.get(pk=pk)
        except:
            return Response({'error': 'Object dose not exist!'})
        
        serialazer = TestSerializer(data=request.data, instance=instanse)
        serialazer.is_valid(raise_exception=True)
        serialazer.save()

        return Response({'post' : serialazer.data})
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error' : 'Method DELETE not allowed!'})
        
        try:
            instanse = Test.objects.get(pk=pk)
        except:
            return Response({'error': 'Object dose not exist!'})
        
        instanse.delete()
        
        return Response({'post' : f'delete post {str(pk)}'})



'''
class DRF_API(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class DRF_API_update(generics.UpdateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class DRF_API_CRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
'''

''' рассписанный под капотом код работы ф_DRF_API
class __DRF_API(APIView):
    def get(self, request):
        t = Test.objects.all()
        return Response({'post' : TestSerializer(t, many=True).data})

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post' : serializer.data})
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error' : 'Method PUT not allowed!'})
        
        try:
            instanse = Test.objects.get(pk=pk)
        except:
            return Response({'error': 'Object dose not exist!'})
        
        serialazer = TestSerializer(data=request.data, instance=instanse)
        serialazer.is_valid(raise_exception=True)
        serialazer.save()

        return Response({'post' : serialazer.data})
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error' : 'Method DELETE not allowed!'})
        
        try:
            instanse = Test.objects.get(pk=pk)
        except:
            return Response({'error': 'Object dose not exist!'})
        
        instanse.delete()
        
        return Response({'post' : f'delete post {str(pk)}'})
'''
