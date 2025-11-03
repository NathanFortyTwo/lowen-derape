import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event
from decimal import Decimal

def index(request):
    events = Event.objects.order_by('-date')
    total_sum = sum(e.amount for e in events)
    is_logged_in = request.session.get('is_lowen', False)
    return render(request, 'main_app_lowen_button/index.html', {
        'events': events,
        'total_sum': total_sum,
        'is_logged_in': is_logged_in,
    })


def login_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        secret = os.getenv('LOWEN_SECRET')
        if code == secret:
            request.session['is_lowen'] = True
        return redirect('index')
    return redirect('index')


def logout_view(request):
    request.session.flush()
    return redirect('index')


@csrf_exempt
def add_event(request):
    if not request.session.get('is_lowen', False):
        return JsonResponse({'error': 'unauthorized'}, status=403)

    reason = request.POST.get('reason', '').strip()
    amount = request.POST.get('amount', '0').strip()
    if not reason:
        return JsonResponse({'error': 'reason required'}, status=400)

    try:
        amount = Decimal(amount)
    except:
        return JsonResponse({'error': 'invalid amount'}, status=400)

    event = Event.objects.create(reason=reason, amount=amount)
    total_sum = sum(e.amount for e in Event.objects.all())

    return JsonResponse({
        'id': event.id,
        'reason': event.reason,
        'amount': float(event.amount),
        'date': event.date.strftime('%Y-%m-%d %H:%M:%S'),
        'total_sum': float(total_sum)
    })
