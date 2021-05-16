from rest_framework.decorators import api_view

from main.models import Input
from main.serializers import AccountSerializer
from main.serializers import InputSerializer

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status


class Register(APIView):

    def post(self, request):
        try:
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(dict(error=str(error)), status=status.HTTP_400_BAD_REQUEST)


class InputData(APIView):

    def post(self, request):
        try:
            serializer = InputSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(dict(error=str(error)), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def handle_input_update(request, id):
    if request.method == 'PUT':
        try:
            input_instance = Input.objects.get(pk=id)
            serializer = InputSerializer(instance=input_instance, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(dict(message=str(error)), status=400)
