import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CreditWallet, WhiteListedIP, Transaction
from users.models import Users 


@csrf_exempt
@api_view(['POST'])
def transaction_webhook(request):
    
    try:
        data = json.loads(request.body)
        user_id = data.get('extra_daa',{}).get('user_id')
        credit_amount = data.get('extra_daa',{}).get('credit_amount')

        payment_id = data.get('event',{}).get('payment_id')
        transaction_id = data.get('event',{}).get('transaction_id')
        product_id = data.get('event',{}).get('product_id')
        payment_method = data.get('event',{}).get('payment_method','other')
        status = "SUCCESS" if data["event"]["type"] == "INITIAL_PURCHASE" else "FAILED"

        type = data["event"]["type"]
        app_user_id = data["event"]["app_user_id"]
        purchase_date = data["event"]["purchase_date"]
        store = data["event"]["store"]
        price = data["event"]["price"]
        currency = data["event"]["currency"]
        region_code = data["event"]["region_code"]

        if user_id:
            user = Users.objects.filter(user=user_id).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            Transaction.objects.create(
                user=user,
                payment_id=payment_id,
                transaction_id=transaction_id,
                product_id=product_id,
                payment_method=payment_method,
                type=type,
                app_user_id=app_user_id,
                purchase_date=purchase_date,
                store=store,
                price=price,
                currency=currency,
                region_code=region_code,
                credit_amount=credit_amount,
            )
            if status == "SUCCESS":
                user_credit = CreditWallet.objects.get(user=user)
                user_credit.balance += credit_amount
                user_credit.save()
            return Response({'message': 'Transaction processed successfully'}, status=status.HTTP_200_OK)
        

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'status': status.HTTP_400_BAD_REQUEST})
