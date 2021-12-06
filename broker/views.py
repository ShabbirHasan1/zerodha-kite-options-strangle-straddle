from django.shortcuts import render, HttpResponse
from .models import KiteBroker
from kiteconnect import KiteConnect
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def kite_set_access_token(request):
    request_data = request.GET

    request_token = request_data.get('request_token')

    if request_token:
        obj = KiteBroker.objects.filter(user = request.user).first()

        if obj:
            kite = KiteConnect(obj.api_key)
            session = kite.generate_session(request_token, obj.api_secret)
            access_token = session["access_token"]
            obj.access_token = access_token
            obj.save()

            return HttpResponse(f"<h1>Request Token {request_token} and Access Token {access_token} Saved!</h1>")
        
        return HttpResponse("<h1>User Doesn't have api key setup.</h1>")
    
    return HttpResponse("<h1>Request Token not found</h1>")
