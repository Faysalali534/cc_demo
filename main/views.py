from rest_framework.decorators import api_view

from main.api import ExchangeManipulation
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


@api_view(["POST"])
def handle_queue_data(request):
    if request.method == "POST":
        try:
            id = request.data.get("input_data_id")
            if not id:
                raise ValueError(f"provide 'input_data_id' to proceed")
            input_instance = Input.objects.get(pk=id)
            print()
            exchange_manipulation = ExchangeManipulation(
                start_date=input_instance.start_date,
                end_date=input_instance.end_date,
                currency=input_instance.currency.short_code,
                category=input_instance.category,
                exchange_id="bybit",
                api_key=input_instance.account.api_key,
                secret_key=input_instance.account.secret_key,
                input_instance=input_instance
            )
            exchange_manipulation.generate_balance_and_leger()
            return Response(dict(message="successfully queued"), status=status.HTTP_200_OK)
        except Exception as error:
            return Response(dict(message=str(error)), status=400)
