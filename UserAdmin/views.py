from django.shortcuts import render , redirect, HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import(
    TopicForm,
    CategoryForm,
    IndicatorForm
)
from django.contrib import messages
from Base.models import (
    Topic,
    Category,
    Indicator,
)

from Base.serializer import (
    CategorySerializers,    
)

# Create your views here.

def index(request):
    return render(request, 'user-admin/index.html')

def topic(request):
    form = TopicForm(request.POST or None, request.FILES or None)
    topics = Topic.objects.all()
    count = 5
   
    if 'q' in request.GET:
        q = request.GET['q']
        topics = Topic.objects.filter( Q(title_ENG__contains=q) | Q(title_AMH__contains=q) | Q(created__contains=q))
    
    paginator = Paginator(topics, 5) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (5 * (int(page_number) if page_number  else 1) ) - 5
        except: count = (5 * (int(1) if page_number  else 1) ) - 5
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (5 * (int(1) if page_number  else 1) ) - 5
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (5 * (int(paginator.num_pages) if page_number  else 1) ) - 5

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128532 Hello User, Topic Successfully Added')
            return redirect('topic')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Topic')
    

    
    context = {
        'topics' : page,
        'count' : count,
        'form' : form,
    }
    return render(request, 'user-admin/topic.html', context)   


def delete_topic(request, id):
    topic = Topic.objects.get(id=id)    
    topic.delete()
    messages.success(request, '&#128532 Hello User, Topic Successfully Deleted')
    return redirect('topic')


def edit_topic(request):    
    id = request.POST['id']  
    form = TopicForm(request.POST or None, request.FILES or None, instance=topic)
    try:
        topic = Topic.objects.get(id = id)
        topic.title_ENG = title_ENG
        topic.title_AMH = question
        topic.is_dashboard = title_AMH
        topic.icon = icon
        topic.rank = rank
        topic.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return Response(response)  
  




#### Category  

def categories(request):
    category = Category.objects.filter(is_deleted = False)
    form = CategoryForm(request.POST or None)
    count = 20

    if 'q' in request.GET:
        q = request.GET['q']
        category = Category.objects.filter(is_deleted = False).filter(  Q(name_ENG__contains=q) | Q(name_AMH__contains=q) | Q(topic__title_ENG__contains=q))

    paginator = Paginator(category, 20) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (20 * (int(page_number) if page_number  else 1) ) - 20
        except: count = (20 * (int(1) if page_number  else 1) ) - 20
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (20 * (int(1) if page_number  else 1) ) - 20
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (20 * (int(paginator.num_pages) if page_number  else 1) ) - 20

    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '😀 Hello User, Category Successfully Added')
            return redirect('categories')
        else:
            messages.error(request, '😞 Hello User , An error occurred while Adding Category')

    
    context = {
            'categories': page,
            'count' : count,
            'form': form
     }
    
    return render(request, 'user-admin/category.html', context)   

def update_category(request):
    id = request.POST['id']
    name_ENG = request.POST['name_ENG']
    name_AMH = request.POST['name_AMH']
    topic_id = request.POST['topic']
    is_dashboard = True if request.POST['is_dashboard_visible'] == "true" else False
    try:
        category = Category.objects.get(id = id)
        category.name_ENG = name_ENG
        category.name_AMH = name_AMH
        try:
           topic = Topic.objects.get(id = topic_id)
           category.topic = topic
        except:
           category.topic = None
        category.is_dashboard_visible = is_dashboard
        category.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return JsonResponse( response)

def delete_category(request, id):
    try:
        category = Category.objects.get(id=id)    
        category.is_deleted = True
        category.save()
        messages.success(request, '😀 Hello User, Category Successfully Deleted')
    except:
        messages.error(request, '😞 Hello User , An error occurred while Deleting Category')
    return redirect('categories')


### Indicator
def indicators(request, id):
    form = IndicatorForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            if 'subIndicatorId' in request.POST:
                parent_id = request.POST['subIndicatorId']
                try:
                    parent = Indicator.objects.get(id = parent_id)
                    obj.parent = parent
                    obj.save()
                    form.save_m2m()
                    messages.success(request, '😀 Hello User, Indicator Successfully Added')
                except:
                    messages.error(request, '😞 Hello User , An error occurred while Adding Indicator')
            else:
                obj.save()
                form.save_m2m()
                messages.success(request, '😀 Hello User, Indicator Successfully Added')
            return redirect('indicators', id)
        else:
            messages.error(request, '😞 Hello User , An error occurred while Adding Indicator')
    context = {
        'form' : form,
    }
    return render(request, 'user-admin/indicator.html', context=context)

def indicator_details(request, id):
    try:
        indicator = Indicator.objects.get(id=id)
    except:
        return HttpResponse("Bad Request!")
    
    form = IndicatorForm(request.POST or None, instance=indicator)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            print("Saved")
            messages.success(request, '😀 Hello User, Indicator Successfully Updated')
            return redirect('categories')
        else:
            messages.error(request, '😞 Hello User , An error occurred while Updating Indicator')
            print("Error")

    context = {
        'form' : form,
    }
    return render(request, 'user-admin/indicator_detail.html', context=context)

def delete_indicator(request, id):
    try:
        indicator = Indicator.objects.get(id=id)    
        indicator.is_deleted = True
        indicator.save()
        messages.success(request, '😀 Hello User, Indicator Successfully Deleted')
    except:
        messages.error(request, '😞 Hello User , An error occurred while Deleting Indicator')
    return redirect(request.META.get('HTTP_REFERER'))