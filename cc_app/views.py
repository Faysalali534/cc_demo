from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from cc_app import api

from cc_app.api import API_HOST

HOST=f"{API_HOST}/"

def home(request):
    return render(request, 'cc_app/home.html', context={})


def index(request):
    context = dict()
    if request.POST:
        password = request.POST.get("password")
        email = request.POST.get("email")
        response = api.login(
            password=password,
            username=email
        )
        if response[1]:
            request.session['token'] = response[0]['token']
            request.session['account_id'] = response[0]['account_id']
            request.session['is_account_input_used'] = response[0]['is_account_input_used']
            request.session['input_id'] = response[0]['input_id']

            return redirect(reverse('cc_app:information'))
        context['message'] = response[0]
    return render(request, 'cc_app/index.html', context=context)


def information(request):
    context = dict()
    token = request.session.get("token")
    
    if not token:
        return redirect(reverse('cc_app:index'))
    get_account_detail_response = api.get_account_detail(
        account_id=request.session["account_id"],
        token=token
    )
    if get_account_detail_response[1]:
        context["account_detail"] = get_account_detail_response[0]
    if request.POST:
        secret_key = request.POST.get("secret_key")
        api_key = request.POST.get("api_key")
        update_account_detail_response = api.update_account_detail(
            account_id=request.session["account_id"],
            token=token,
            api_key=api_key,
            secret_key=secret_key
        )
        if update_account_detail_response[1]:
            context["message"] = "Account is updated successfully"
            get_account_detail_response = api.get_account_detail(
                account_id=request.session["account_id"],
                token=token
            )

            if get_account_detail_response[1]:
                context["account_detail"] = get_account_detail_response[0]
                
    is_account_input_used = request.session.get("is_account_input_used")
    input_id = request.session.get("input_id")

    response = api.get_currency(token=token)
    exchanges = api.get_exchange(token=token)
    if is_account_input_used:
        get_input_data = api.get_input_data(
            token=token,
            input_id=input_id
        )
        if get_input_data[1]:
            context["input_data"] = get_input_data[0]

    if response[1]:
        context["currencies"] = response[0]
    if exchanges[1]:
        context["exchanges"] = exchanges[0]
    if request.POST:
        start_date = request.POST.get("start_date")
        currency = request.POST.get("currency_capture")
        exchange = request.POST.get("exchange")
        end_date = request.POST.get("end_date")
        category = request.POST.get("category") or "inverse"
        if not bool(is_account_input_used):
            insert_response = api.insert_input(
                account=request.session["account_id"],
                start_date=start_date,
                end_date=end_date,
                currency=currency,
                category=category,
                token=token,
                exchange=exchange
            )

            if insert_response[1]:
                request.session["is_account_input_used"] = True
                request.session["input_id"] = insert_response[0].get("id")
                context["message"] = "Input is added successfully"
                return redirect(reverse('cc_app:portal'))
        else:
            update_response = api.update_input(
                account=request.session["account_id"],
                start_date=start_date,
                end_date=end_date,
                currency=currency,
                category=category,
                token=token,
                input_id=input_id,
                exchange=exchange
            )
            if update_response[1]:
                context["message"] = "Input is updated successfully"
                get_input_data = api.get_input_data(
                    token=token,
                    input_id=input_id
                )
                if get_input_data[1]:
                    context["input_data"] = get_input_data[0]
                return redirect(reverse('cc_app:portal'))
    return render(request, "cc_app/information.html", context=context)


def portal(request):
    if not request.session.get("token"):
        return redirect(reverse("cc_app:index"))
    context = dict(
        api_host=HOST,
        token=request.session.get("token"),
        input=request.session["input_id"],
    )
    return render(request, "cc_app/portal.html", context=context)



def logout(request):
    del request.session['token']
    del request.session['account_id']
    del request.session['is_account_input_used']
    del request.session['input_id']

    return redirect(reverse('cc_app:home'))


def log(request):
    if not request.session.get('token'):
        return redirect(reverse('cc_app:index'))
    context = dict(
        api_host=HOST,
        token=request.session.get("token"),
        input=request.session["input_id"],
    )
    return render(request, 'cc_app/log.html',context=context)
