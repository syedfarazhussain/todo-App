from django.shortcuts import render, redirect
from .models import List
from .forms import ListForm
from django.contrib import messages
from django.http import HttpResponseRedirect
import calendar
from calendar import HTMLCalendar 

def calender(request, year, month):
    month = month.capitalize()
    months = list(calendar.month_name).index(month)
    months = int(months)

    # create calender

    cal = HTMLCalendar().formatmonth(year,months)

    context = {
        "month_number": months,
        "cal": cal,
    }
    return render(request, 'calender.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        post = List.objects.filter(item__contains=searched)
        context = {
            "searched"      : searched,
            "searched_post" : post,
        }
        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')

def home(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:

            all_items = List.objects.all
            messages.success(request, ('Item has been successfully added to the list.'))
            return render(request, 'home.html', {'todo_items': all_items})
    else: 
        all_items = List.objects.all
        return render(request, 'home.html', {'todo_items': all_items})

def delete(request, item_id):
    item = List.objects.get(pk=item_id)
    item.delete()
    messages.success(request, ('Item has been deleted'))
    return redirect('home')

def cross_off(request, item_id):
    item = List.objects.get(pk=item_id)
    item.completed = True
    item.save()
    messages.success(request, ('Item has been  completed.'))
    return redirect('home')

def uncross(request, item_id):
    item = List.objects.get(pk=item_id)
    item.completed = False
    item.save()
    messages.success(request, ('Item has been not completed.'))
    return redirect('home')

def edit(request, item_id):
    if request.method == 'POST':
        item = List.objects.get(pk=item_id)
        form = ListForm(request.POST or None, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, ('Item has been successfully edited.'))
            return redirect('home')
    else: 
        item = List.objects.get(pk=item_id)
        return render(request, 'edit.html', {'item': item})