from django.shortcuts import render , redirect, HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
    DataPoint,
    AnnualData
)
from UserManagement.forms import(
    CustomUserForm
)
from UserManagement.models import(
    CustomUser
)

from Base.serializer import (
    CategorySerializers,    
)

# Create your views here.

def index(request):
    context = {
        'total_topic' : Topic.objects.all().count(),
        'total_dashboard_topic' : Topic.objects.filter(is_dashboard = True).count(),
        'total_category' : Category.objects.all().count(),
        'total_indicator' : Indicator.objects.all().count(),
    }

    return render(request, 'user-admin/index.html' , context)

##Data View
def data_view(request):
    return render(request, 'user-admin/data_view.html')

def data_view_indicator_detail(request, id):
    form = IndicatorForm(request.POST or None)
    if request.method == "GET":
        indicator = None
        try:
            indicator = Indicator.objects.get(id=id)
        except:
            HttpResponse(404)
        context = {
            'indicator' : indicator,
            'form' : form,
        }
        return render(request, 'user-admin/data_view_indicator_detail.html', context=context)
    elif request.method == 'POST':
        if 'form_indicator_add_id' in request.POST:
            parent_id = request.POST['form_indicator_add_id']
            #try:
            indicator = Indicator.objects.get(id = parent_id)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.parent = indicator
                obj.save()
                for category in indicator.for_category.all():
                    obj.for_category.add(category)
                obj.save()
                AnnualData.objects.create(indicator = obj, performance = 0, for_datapoint = DataPoint.objects.first())
                messages.success(request, '😃 Hello User, Successfully Added Indicator')
            #except:
            #    messages.error(request, '😞 Hello User , An error occurred while Adding Indicator')
            return redirect('data_view_indicator_detail', id)
        elif 'indicator_id' in request.POST:
            indicator_id = request.POST['indicator_id']
            year_id = request.POST['year_id']
            new_value = request.POST['value']
    
            try:
                value = AnnualData.objects.get(indicator__id = indicator_id, for_datapoint__year_EC = year_id)
                value.performance = new_value
                value.save()
            except:
                try:
                    indicator = Indicator.objects.get(id = indicator_id)
                    datapoint = DataPoint.objects.get(year_EC = year_id)
                    AnnualData.objects.create(indicator = indicator, performance = new_value, for_datapoint = datapoint)
                except:
                    return JsonResponse({'response' : False})
            return JsonResponse({'response' : True})
    
    else: return HttpResponse("Bad Request!")



def topic(request):
    form = TopicForm(request.POST or None, request.FILES or None)
    topics = Topic.objects.filter(is_deleted=False)
    count = 5
   
    if 'q' in request.GET:
        q = request.GET['q']
        topics = Topic.objects.filter(is_deleted=False).filter( Q(title_ENG__contains=q) | Q(title_AMH__contains=q) | Q(created__contains=q))
    
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


@api_view(['POST'])
def edit_topic(request):    
    id = request.POST['id'] 
    title_ENG = request.POST['title_ENG']
    title_AMH = request.POST['title_AMH']
    is_dashboard = True if request.POST['is_dashboard'] == "true" else False
    rank = request.POST['rank']
    icons = request.POST.get('icon')
    try:
        topic = Topic.objects.get(id = id)
        topic.title_ENG = title_ENG
        topic.title_AMH = title_AMH
        topic.is_dashboard = is_dashboard
        topic.rank = rank
        topic.icon = icons
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

#All indicators
def all_indicators(request):
    all_indicators = Indicator.objects.filter(is_deleted=False)
    count = 50
    form = IndicatorForm(request.POST or None)
    if 'q' in request.GET:
        q = request.GET['q']
        all_indicators = Indicator.objects.filter(is_deleted=False).filter( Q(title_ENG__contains=q) | Q(title_AMH__contains=q))

    paginator = Paginator(all_indicators, 50)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (50 * (int(page_number) if page_number  else 1) ) - 50
        except: count = (50 * (int(1) if page_number  else 1) ) - 50
    except PageNotAnInteger:
        page = paginator.page(1)
        count = (50 * (int(1) if page_number  else 1) ) - 50
    except:
        page = paginator.page(paginator.num_pages)
        count = (50 * (int(paginator.num_pages) if page_number  else 1) ) - 50

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128532 Hello User, Indicator Successfully Added')
            return redirect('all_indicators')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding Indicator')


    context = {
        'all_indicators' : page,
        'count' : count,
        'form' : form
    }    
    return render(request, 'user-admin/all_indicators.html' , context)



    

#Data years
def years(request):
    years = DataPoint.objects.all()
    count = 3
   
    if 'q' in request.GET:
        q = request.GET['q']
        years = DataPoint.objects.filter( Q(year_EC__contains=q) | Q(year_GC__contains=q) | Q(created_at__contains=q))
    
    paginator = Paginator(years, 3) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (3 * (int(page_number) if page_number  else 1) ) - 3
        except: count = (3 * (int(1) if page_number  else 1) ) - 3
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (3 * (int(1) if page_number  else 1) ) - 3
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (3 * (int(paginator.num_pages) if page_number  else 1) ) - 3

    if request.method == 'POST':
        try:
          latest_year = DataPoint.objects.latest('year_EC').year_EC
          year_first = DataPoint.objects.first().year_EC
        except:
          latest_year = 1980
          year_first = 1981
        add_position = request.POST.get('addPosition')  # Get the selected position from the form

        if add_position == 'front':
            new_year_EC = int(latest_year) + 1
        elif add_position == 'back':
            new_year_EC = int(year_first) - 1
        else:
            # Handle invalid selection if needed
            return redirect('years')  # Redirect back to the same page

        DataPoint.objects.create(year_EC=new_year_EC)
        messages.success(request, '&#128532 Hello User, Year Successfully Added')
        return redirect('years')
    context = {
        'years' : page,
        'count' : count,
    }    
   
    return render(request, 'user-admin/years.html',context)



#Users
def users(request):
    users = CustomUser.objects.all()
    form = CustomUserForm(request.POST or None)
    count = 5
    total_users = CustomUser.objects.all().count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    inactive_users = CustomUser.objects.filter(is_active=False).count()


    if 'q' in request.GET:
        q = request.GET['q']
        users = CustomUser.objects.filter( Q(first_name__contains=q) | Q(last_name__contains=q) | Q(email__contains=q) | Q(username__contains=q))
    
    paginator = Paginator(users, 5) 
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
            messages.success(request, '&#128532 Hello User, User Successfully Added')
            return redirect('users')
        else:
            messages.error(request, '&#128532 Hello User , An error occurred while Adding User')
    
    
    context = {
        'users' : page,
        'count' : count,
        'form' : form,
        'total_users' : total_users,
        'active_users' : active_users,
        'inactive_users' : inactive_users
    }
    return render(request, 'user-admin/user_list.html', context) 



def user_activate(request, id):
    user = CustomUser.objects.get(id=id)    
    user.is_active = True if user.is_active == False else False
    status = "Deactivated" if user.is_active == False else "Activated"
    user.save()
    messages.success(request, f'😊 Hello User, User Successfully {status}')
    return redirect('users')

    
@api_view(['POST'])
def edit_user(request):    
    id = request.POST['id'] 
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    is_superuser = True if request.POST['is_superuser'] == "true" else False
    email = request.POST['email']
    username = request.POST.get('username')
    try:
        user = CustomUser.objects.get(id = id)
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = is_superuser
        user.rank = rank
        user.username = username
        user.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return Response(response)  
  
