from ccxt import AuthenticationError
from rest_framework.authentication import TokenAuthentication

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from main.models import Input
from main.models import Currency

from main.serializers import AccountSerializer
from main.serializers import CurrencySerializer
from main.serializers import InputSerializer

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status
from rest_framework import generics

from main.tasks import generate_balance_and_leger


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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def handle_queue_data(request):
    if request.method == "POST":
        try:
            id = request.data.get("input_data_id")
            if not id:
                raise ValueError(f"provide 'input_data_id' to proceed")
            generate_balance_and_leger.delay(id)
            return Response(
                dict(message="successfully queued"), status=status.HTTP_200_OK
            )
        except AuthenticationError:
            return Response(
                dict(message="provide correct 'api key' and 'secret key'"),
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as error:
            return Response(dict(message=str(error)), status=400)


class Currency(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CheckAuth(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'detail': 'You\'re Authenticated'})


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'You\'re logout'})
