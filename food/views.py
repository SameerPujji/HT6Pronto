from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db import Error, OperationalError
from django.db.transaction import atomic
from functools import wraps
from .models import *
from django.db import connection
import psycopg2
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client


# Create your views here.

def index(request):
    return render(request, 'index.html')


def ChickRestaurant(request):
    conn = psycopg2.connect(
        database='wise-fish-3052.defaultdb',
        user='sameer',
        password='EnNo2Ir8axgEzruB',
        sslmode='require',
        sslrootcert='/Users/Sam/.postgresql/root.crt',
        sslkey='/Users/Sam/.postgresql/client.sameer.key',
        sslcert='/Users/Sam/.postgresql/client.sameer.crt',
        port=26257,
        host='free-tier.gcp-us-central1.cockroachlabs.cloud'
    )
    orders = []
    with conn.cursor() as cur:
        cur.execute('USE food;')
        cur.execute("SELECT * FROM resto;")
        rows = cur.fetchall()
        for row in rows:
            temp = {'time': row[0], 'code': row[1]}
            orders.append(temp)

    return render(request, 'orders.html', {'orders': orders})


@csrf_exempt
def sms(request):
    account_sid = 'ACfbaf75101cc039421561443568fbe85d'
    auth_token = 'febf95cfa9aedeccf5ebdfff0447e7e0'
    client = Client(account_sid, auth_token)
    body = request.POST["Body"]
    if "hello" in body.lower():
        client.messages.create(
            body="Hi! Thank you for contacting Pronto. What would you like to do today?",
            from_='+14157693697',
            to='+16479173143'
        )
    elif "order" in body.lower():
        conn = psycopg2.connect(
            database='wise-fish-3052.defaultdb',
            user='sameer',
            password='EnNo2Ir8axgEzruB',
            sslmode='require',
            sslrootcert='/Users/Sam/.postgresql/root.crt',
            sslkey='/Users/Sam/.postgresql/client.sameer.key',
            sslcert='/Users/Sam/.postgresql/client.sameer.crt',
            port=26257,
            host='free-tier.gcp-us-central1.cockroachlabs.cloud'
        )
        today = []
        with conn.cursor() as cur:
            cur.execute('USE food;')
            cur.execute("SELECT * FROM food_available;")
            rows = cur.fetchall()
            for row in rows:
                today.append(row[1])
        returnString = "Great! Today's options are: " + ",".join(today)
        client.messages.create(
            body=returnString,
            from_='+14157693697',
            to='+16479173143'
        )
    elif "chev chicken" in body.lower():
        client.messages.create(
            body="What time would you like to pick up Chev Chicken? All times are currently available",
            from_='+14157693697',
            to='+16479173143'
        )
    elif "8" in body.lower():
        client.messages.create(
            body="Your meal from Chev Chicken has been confirmed for 20:00 - 20:30 today. Please show the code N19DLB on pick up.",
            from_='+14157693697',
            to='+16479173143'
        )
    else:
        client.messages.create(
            body="Chev Chicken is serving Fried Chicken + Pop for 1 credit today",
            from_='+14157693697',
            to='+16479173143'
        )


def render_booking(request):
    account_sid = 'ACfbaf75101cc039421561443568fbe85d'
    auth_token = 'febf95cfa9aedeccf5ebdfff0447e7e0'
    client = Client(account_sid, auth_token)

    client.messages.create(
        body="Your pick-up code for Chev Chicken at 20:00 - 20:30 is O8C2N4",
        from_='+14157693697',
        to='+16479173143'
    )
    return render(request, 'booked.html', {'name': "Sameer"})


def render_chicken(request):
    conn = psycopg2.connect(
        database='wise-fish-3052.defaultdb',
        user='sameer',
        password='EnNo2Ir8axgEzruB',
        sslmode='require',
        sslrootcert='/Users/Sam/.postgresql/root.crt',
        sslkey='/Users/Sam/.postgresql/client.sameer.key',
        sslcert='/Users/Sam/.postgresql/client.sameer.crt',
        port=26257,
        host='free-tier.gcp-us-central1.cockroachlabs.cloud'
    )
    with conn.cursor() as cur:
        cur.execute('USE food;')
        cur.execute("SELECT * FROM food_available;")
        rows = cur.fetchall()
        foods = []
        for row in rows:
            if row[1] != 'Chev Chicken':
                stars = [x for x in range(1, int(row[2]) + 1)]
                temp = {'name': row[1], 'price': row[4],
                        'stars': stars, 'img': row[3]}
                foods.append(temp)

    return render(request, 'product.html', {'name': "Sameer", 'recommendeds': foods})


@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    def get(self, request, id=None, *args, **kwargs):
        conn = psycopg2.connect(
            database='wise-fish-3052.defaultdb',
            user='sameer',
            password='EnNo2Ir8axgEzruB',
            sslmode='require',
            sslrootcert='/Users/Sam/.postgresql/root.crt',
            sslkey='/Users/Sam/.postgresql/client.sameer.key',
            sslcert='/Users/Sam/.postgresql/client.sameer.crt',
            port=26257,
            host='free-tier.gcp-us-central1.cockroachlabs.cloud'
        )
        with conn.cursor() as cur:
            cur.execute('USE food;')
            cur.execute("SELECT * FROM food_available;")
            rows = cur.fetchall()
            foods = []
            for row in rows:
                stars = [x for x in range(1, int(row[2]) + 1)]
                temp = {'name': row[1], 'price': row[4],
                        'stars': stars, 'img': row[3]}
                foods.append(temp)

        return render(request, 'rest.html', {'name': "Sameer", 'credits': 6, 'foods': foods})
