from main.serializers import AccountSerializer

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
