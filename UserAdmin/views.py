from django.shortcuts import render , redirect, HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from UserManagement.forms import CustomUserForm
from UserManagement.models import CustomUser
from DashBoard.models import (
    Component,
    Dashboard,
    DashboardIndicator,
    Row,
)
from Base.forms import (ImportFileForm, ImportFileIndicatorAddValueForm)
from Base.resource import (
    handle_uploaded_Topic_file,
    confirm_file,
    handle_uploaded_Category_file,
    handle_uploaded_Indicator_file,
    handle_uploaded_Annual_file,
    handle_uploaded_Quarter_file,
    handle_uploaded_Month_file
)

from .forms import(
    TopicForm,
    CategoryForm,
    IndicatorForm,
    DocumentForm
)

from Base.resource import(
    TopicResource,
    CategoryResource,
    IndicatorResource
)
from django.contrib import messages
from Base.models import (
    Topic,
    Category,
    Indicator, 
    DataPoint,
    AnnualData,
    QuarterData,
    MonthData,
    Month,
    Quarter,
    Document
)
import random

from django.db.models import Count
from django.contrib.auth.decorators import login_required
from DashBoard.forms import(
    DashboardForm,
    DashboardIndicatorForm
)





@login_required(login_url='login')
def index(request , id=None):
    bootstrap_colors = ['secondary', 'success', 'warning', 'info', 'dark']
 
    topics = Topic.objects.annotate(num_categories=Count('categories'))
    if id:   
        try :  
               selected_topic = Topic.objects.get(id=id)
               selected_topic_categories = Category.objects.filter(topic__id=id)
               cat_indicator = []
               for selected_topic_category in selected_topic_categories:
                    indicators = list(Indicator.objects.filter(for_category=selected_topic_category).values('id', 'title_ENG', 'title_AMH'))
                    
                    for indicator in indicators:
                        annual_data_values = list(AnnualData.objects.filter(indicator_id=indicator['id']).values(
                            'id',
                            'indicator__title_ENG',
                            'indicator__title_AMH',
                            'indicator_id',
                            'indicator__parent_id',
                            'for_datapoint__year_EC',
                            'for_datapoint__year_GC',
                            'performance',
                            'target'
                        ))
                        
                        indicator['annual_data_values'] = annual_data_values
                    
                    cat_indicator.append({
                        'cat_name_ENG': selected_topic_category.name_ENG,
                        'cat_name_AMH': selected_topic_category.name_AMH,
                        'cat_id': selected_topic_category.id,
                        'indicators': indicators
                    })  
               
        except: 
            cat_indicator = []
            selected_topic  = None
    else :
        cat_indicator = []
        selected_topic  = None        
    if 'q' in request.GET: # Cheking if query is present
        q = request.GET['q']
        id = None
        # first try if the query exists in the indicator 
        indicators = Indicator.objects.filter(Q(title_ENG__contains=q) | Q(title_AMH__contains=q))
        if not indicators:
            selected_topic_categories = Category.objects.filter(Q(name_ENG__contains=q) | Q(name_AMH__contains=q))
            cat_indicator = []
            for selected_topic_category in selected_topic_categories:
                 indicators = list(Indicator.objects.filter(for_category=selected_topic_category).values('id', 'title_ENG', 'title_AMH'))
                 
                 for indicator in indicators:
                     annual_data_values = list(AnnualData.objects.filter(indicator_id=indicator['id']).values(
                         'id',
                         'indicator__title_ENG',
                         'indicator__title_AMH',
                         'indicator_id',
                         'indicator__parent_id',
                         'for_datapoint__year_EC',
                         'for_datapoint__year_GC',
                         'performance',
                         'target'
                     ))
                     
                     indicator['annual_data_values'] = annual_data_values
                 
                 
                 cat_indicator.append({
                     'cat_name_ENG': selected_topic_category.name_ENG,
                     'cat_name_AMH': selected_topic_category.name_AMH,
                     'cat_id': selected_topic_category.id,
                     'indicators': indicators
                 })  
             
        # if the query is not present in the indicator but exixts in the category         
        else :       
            indicator_ids = [] 
            for indicator in indicators:
                annual_data_values = list(AnnualData.objects.filter(indicator_id=indicator.id).values(
                    'id',
                    'indicator_id',
                    'indicator__parent_id',
                    'for_datapoint__year_EC',
                    'for_datapoint__year_GC',
                    'performance',
                    'target',
                ))
                for data_value in annual_data_values:
                      indicator_ids.append(data_value['indicator_id'])
    
                
                indicator.annual_data_values = annual_data_values
                categories = list(Category.objects.filter(indicators__id__in=indicator_ids).values_list('name_ENG' , flat=True).distinct())
                output_str = ', '.join(categories)
                cat_indicator = []
                cat_indicator.append({
                    'cat_name_ENG': output_str,
                    'indicators': indicators
                })  

  
    for topic in topics:
        topic.color = random.choice(bootstrap_colors)
    context = {
        'topics': topics,
        'total_topic': Topic.objects.all().count(),
        'total_dashboard_topic': Topic.objects.filter(is_dashboard=True).count(),
        'total_category': Category.objects.all().count(),
        'total_indicator': Indicator.objects.all().count(),
        'cat_indicator' : cat_indicator,
        'selected_topic' : selected_topic
    }

    return render(request, 'user-admin/index.html', context)

##Data View
@login_required(login_url='login')
def data_view(request):
    form = ImportFileIndicatorAddValueForm(request.POST or None, request.FILES or None)
    last_indicator_id = Indicator.objects.last().id
    global imported_data_global
    global type_of_data

    if request.method == 'POST':
        if 'fileDataValue' in request.POST:
            if form.is_valid():
                type_of_data = form.cleaned_data['type_of_data']
                if type_of_data == 'yearly':
                    type_of_data = 'yearly'
                    success, imported_data,result = handle_uploaded_Annual_file(file = request.FILES['file'])
                elif type_of_data == 'quarterly':
                    type_of_data = 'quarterly'
                    success, imported_data, result = handle_uploaded_Quarter_file(file = request.FILES['file'])
                elif type_of_data == 'monthly':
                    type_of_data = 'monthly'
                    success, imported_data, result = handle_uploaded_Month_file(file = request.FILES['file'])
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'user-admin/import_preview.html', context=context)
            else:
                messages.error(request, '😞 Hello User , An error occurred while Importing Data')
        elif 'confirm_data_form' in request.POST:
            success, message = confirm_file(imported_data_global, type_of_data)
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

    context = {
        'form' : form,
        'last_indicator_id' : last_indicator_id+1
    }
    return render(request, 'user-admin/data_view.html', context=context)

@login_required(login_url='login')
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
            try:
                indicator = Indicator.objects.get(id = parent_id)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.parent = indicator
                    obj.save()
                    for category in indicator.for_category.all():
                        obj.for_category.add(category)
                    obj.save()
                    messages.success(request, '😃 Hello User, Successfully Added Indicator')
            except:
               messages.error(request, '😞 Hello User , An error occurred while Adding Indicator')
            return redirect('data_view_indicator_detail', id)
        elif 'indicator_id' in request.POST:
            indicator_id = request.POST['indicator_id']
            year_id = request.POST['year_id']
            new_value = request.POST['value']
            quarter_id = request.POST['quarter_id']
            month_id = request.POST['month_id']




    
            if quarter_id == "" and month_id == "":
                try:
                    value = AnnualData.objects.filter(indicator__id = indicator_id, for_datapoint__year_EC = year_id).first()
                    value.performance = new_value
                    value.save()
                except:
                    try:
                        indicator = Indicator.objects.get(id = indicator_id)
                        datapoint = DataPoint.objects.get(year_EC = year_id)
                        AnnualData.objects.create(indicator = indicator, performance = new_value, for_datapoint = datapoint)
                    except:
                        return JsonResponse({'response' : False})
            elif quarter_id != "" and month_id == "":
                try:
                    value = QuarterData.objects.filter(indicator__id = indicator_id, for_datapoint__year_EC = year_id, for_quarter__number = quarter_id).first()
                    value.performance = new_value
                    value.save()
                except:
                    try:
                        indicator = Indicator.objects.get(id = indicator_id)
                        datapoint = DataPoint.objects.get(year_EC = year_id)
                        quarter = Quarter.objects.get(id = quarter_id)
                        QuarterData.objects.create(indicator = indicator, performance = new_value, for_datapoint = datapoint, for_quarter = quarter)
                    except:
                        return JsonResponse({'response' : False})
            elif quarter_id == "" and month_id != "":
                try:
                    value = MonthData.objects.filter(indicator__id = indicator_id, for_datapoint__year_EC = year_id, for_month__number = month_id).first()
                    value.performance = new_value
                    value.save()
                    print("month-update")
                except:
                    try:
                        indicator = Indicator.objects.get(id = indicator_id)
                        datapoint = DataPoint.objects.get(year_EC = year_id)
                        month = Month.objects.get(id = month_id)
                        MonthData.objects.create(indicator = indicator, performance = new_value, for_datapoint = datapoint, for_month = month)
                    except:
                        return JsonResponse({'response' : False})
                

            return JsonResponse({'response' : True})
    
    else: return HttpResponse("Bad Request!")

@login_required(login_url='login')
def data_view_indicator_update(request, id):
    try:
        indicator = Indicator.objects.get(id=id)
    except:
        return HttpResponse("Bad Request!")
    
    previous_page = id
    i = indicator
    while i != None:
        previous_page = i.parent.id if i.parent else i.id
        i = i.parent 
    
    form = IndicatorForm(request.POST or None, instance=indicator)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '😀 Hello User, Indicator Successfully Updated')
            return redirect('data_view_indicator_detail', previous_page)
        else:
            messages.error(request, '😞 Hello User , An error occurred while Updating Indicator')

    context = {
        'form' : form,
    }
    return render(request, 'user-admin/indicator_detail.html', context=context)

@login_required(login_url='login')
def topic(request):
    form = TopicForm(request.POST or None, request.FILES or None)
    topics = Topic.objects.filter(is_deleted=False)
    count = 30

    formFile = ImportFileForm() #responsive to read imported file for import export 
    global imported_data_global #global variable to store imported data
   
    if 'q' in request.GET:
        q = request.GET['q']
        topics = Topic.objects.filter(is_deleted=False).filter( Q(title_ENG__contains=q) | Q(title_AMH__contains=q) | Q(created__contains=q))
    
    paginator = Paginator(topics, 30) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30

    if request.method == 'POST':
        if 'addTopic' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, '😀 Hello User, Topic Successfully Added')
                return redirect('topic')
            else:
                messages.error(request, '😞 Hello User , An error occurred while Adding Topic')
        elif 'fileTopic' in request.POST:
            formFile = ImportFileForm(request.POST, request.FILES)
            if formFile.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_Topic_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'user-admin/import_preview.html', context=context)
            else:
                messages.error(request, '😞 Hello User , An error occurred while Importing Topic')
        elif 'confirm_data_form' in request.POST:
            success, message = confirm_file(imported_data_global, 'topic')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

    

    
    context = {
        'topics' : page,
        'count' : count,
        'form' : form,
        'formFile' : formFile
    }
    return render(request, 'user-admin/topic.html', context)   

@login_required(login_url='login')
def delete_topic(request, id):
    topic = Topic.objects.get(id=id)    
    topic.delete()
    messages.success(request, '&#128532 Hello User, Topic Successfully Deleted')
    return redirect('topic')

@login_required(login_url='login')
@api_view(['POST'])
def edit_topic(request):    
    id = request.POST['id'] 
    title_ENG = request.POST['title_ENG']
    title_AMH = request.POST['title_AMH']
    is_dashboard = True if request.POST['is_dashboard'] == "true" else False
    rank = int(request.POST.get('rank'))
    print(rank)
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
@login_required(login_url='login')
def categories(request):
    category = Category.objects.filter(is_deleted = False).select_related()
    form = CategoryForm(request.POST or None)
    count = 20

    formFile = ImportFileForm() #responsive to read imported file for import export 
    global imported_data_global #global variable to store imported data

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
        if 'addTopicForm' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, '😀 Hello User, Category Successfully Added')
                return redirect('categories')
            else:
                messages.error(request, '😞 Hello User , An error occurred while Adding Category')
        elif 'fileCategory' in request.POST:
            formFile = ImportFileForm(request.POST, request.FILES)
            if formFile.is_valid():
                file = request.FILES['file']
                success, imported_data, result = handle_uploaded_Category_file(file)
                imported_data_global = imported_data
                context = {'result': result}
                return render(request, 'user-admin/import_preview.html', context=context)
            else:
                messages.error(request, '😞 Hello User , An error occurred while Importing Category')
        elif 'confirm_data_form' in request.POST:
            success, message = confirm_file(imported_data_global, 'category')
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)

    
    context = {
            'categories': page,
            'count' : count,
            'form': form,
            'formFile' : formFile
     }
    
    return render(request, 'user-admin/category.html', context)   
@login_required(login_url='login')
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

@login_required(login_url='login')
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
@login_required(login_url='login')
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



@login_required(login_url='login')
def indicator_details(request, id):
    try:
        indicator = Indicator.objects.get(id=id)
    except:
        return HttpResponse("Bad Request!")
    
    form = IndicatorForm(request.POST or None, instance=indicator)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '😀 Hello User, Indicator Successfully Updated')
            return redirect('categories')
        else:
            messages.error(request, '😞 Hello User , An error occurred while Updating Indicator')

    context = {
        'form' : form,
    }
    return render(request, 'user-admin/indicator_detail.html', context=context)


@login_required(login_url='login')
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
@login_required(login_url='login')
def all_indicators(request):
    last_indicator_id = Indicator.objects.last().id
    all_indicators = Indicator.objects.filter(is_deleted=False)
    count = 30
    form = IndicatorForm(request.POST or None)

    formFile = ImportFileForm() #responsive to read imported file for import export 
    global imported_data_global #global variable to store imported data

    if 'q' in request.GET:
        q = request.GET['q']
        all_indicators = Indicator.objects.filter(is_deleted=False).filter( Q(title_ENG__contains=q) | Q(title_AMH__contains=q))

    paginator = Paginator(all_indicators,30)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) -30
        except: count = (30 * (int(1) if page_number  else 1) ) -30
    except PageNotAnInteger:
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) -30
    except:
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) -30

    if request.method == 'POST':
            if 'addIndicatorForm' in request.POST:
                if form.is_valid():
                    form.save()
                    messages.success(request, '😀 Hello User, Indicator Successfully Added')
                    return redirect('all_indicators')
            elif 'fileIndicator' in request.POST:
                print("hreee")
                formFile = ImportFileForm(request.POST, request.FILES)
                if formFile.is_valid():
                    file = request.FILES['file']
                    success, imported_data, result = handle_uploaded_Indicator_file(file)
                    imported_data_global = imported_data
                    context = {'result': result}
                    return render(request, 'user-admin/import_preview.html', context=context)
                else:
                    messages.error(request, '😞 Hello User , An error occurred while Importing Indicator')
            elif 'confirm_data_form' in request.POST:
                success, message = confirm_file(imported_data_global, 'indicator')
                if success:
                    messages.success(request, message)
                else:
                    messages.error(request, message)
                


    context = {
        'all_indicators' : page,
        'count' : count,
        'form' : form,
        'formFile' : formFile,
        'last_indicator_id' : last_indicator_id+1
    }    
    return render(request, 'user-admin/all_indicators.html' , context)



    

#Data years
@login_required(login_url='login')
def years(request):
    years = DataPoint.objects.all()
    count = 20
   
    if 'q' in request.GET:
        q = request.GET['q']
        years = DataPoint.objects.filter( Q(year_EC__contains=q) | Q(year_GC__contains=q) | Q(created_at__contains=q))
    
    paginator = Paginator(years, 20) 
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
@login_required(login_url='login')
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


@login_required(login_url='login')
def user_activate(request, id):
    user = CustomUser.objects.get(id=id)    
    user.is_active = True if user.is_active == False else False
    status = "Deactivated" if user.is_active == False else "Activated"
    user.save()
    messages.success(request, f'😊 Hello User, User Successfully {status}')
    return redirect('users')

    
@login_required(login_url='login')
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
        user.username = username
        user.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return Response(response)  
  


#######Document#########
def document(request):
    form = DocumentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128532 Hello User, Document Successfully Added')
            return redirect('document')
        else:
            messages.error(request, '&#128532 Hello User, An error occurred while Adding Document')
    
    topics = Topic.objects.filter(is_deleted = False)

    if 'q' in request.GET:
        q = request.GET['q']
        documents = Document.objects.filter(Q(title_ENG__contains=q) | Q(title_AMH__contains=q)).values_list('topic__id', flat=True)
        topics = Topic.objects.filter(is_deleted = False).filter(  Q(title_ENG__contains=q) | Q(title_AMH__contains=q) | Q(id__in=list(documents)) ).distinct()  


    context ={
        'form' : form,
        'topics' : topics
    }
    return render(request, 'user-admin/document.html', context=context)



def document_edit(request, id):
    
    try:
        document = Document.objects.get(id=id)
    except Document.DoesNotExist:
        return HttpResponse("Document does not exist")
    

    form = DocumentForm(request.POST or None, request.FILES or None, instance=document)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128532 Hello User, Document Successfully Updated')
            return redirect('document')
        else:
            messages.error(request, '&#128532 Hello User, An error occurred while Updating Document')
    
    context = {
        'form' : form,
        'document' : document
    }
    return render(request, 'user-admin/document_edit.html', context=context)


def document_delete(request, id):
    try:
        document = Document.objects.get(id=id)
        document.delete()
    except Document.DoesNotExist:
        return HttpResponse("Document does not exist")
    
    messages.success(request, '&#128532 Hello User, Document Successfully Deleted')
    return redirect('document')
    


#################Dashboard####################  
def custom_dashboard(request):
    dashboards = Dashboard.objects.all()
    form = DashboardForm(request.POST or None)
    if 'q' in request.GET:
        q = request.GET['q']
        dashboards = Dashboard.objects.filter( Q(title__contains=q))
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '&#128532 Hello User, Dashboard Successfully Added')
            return redirect('custom-dashboard-index')
        else:
            messages.error(request, '&#128532 Hello User, An error occurred while Adding Dashboard')
    paginator = Paginator(dashboards, 10) 
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
        try: count = (30 * (int(page_number) if page_number  else 1) ) - 30
        except: count = (30 * (int(1) if page_number  else 1) ) - 30
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page = paginator.page(1)
        count = (30 * (int(1) if page_number  else 1) ) - 30
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page = paginator.page(paginator.num_pages)
        count = (30 * (int(paginator.num_pages) if page_number  else 1) ) - 30        
    context = {
        'dashboards' : page,
        'form' : form,
    }
    return render(request, 'user-admin/dashboard-admin/dashboard_list.html', context=context)


@api_view(['POST'])
def edit_dashboard(request):    
    id = request.POST['id'] 
    title = request.POST['title']
    description = request.POST['description'] 
    print(id , title , description)
    try:
        dashboard = Dashboard.objects.get(id = id)
        dashboard.title = title
        dashboard.description = description
        dashboard.save()
        response = {'success' : True}
    except:
        response = {'success' : False}
    return Response(response)  


@login_required(login_url='login')
def delete_dashboard(request, id):
    dashboard = Dashboard.objects.get(id=id)    
    dashboard.delete()
    messages.success(request, '&#128532 Hello User, Dashboard Successfully Deleted')
    return redirect('custom-dashboard-index')



def custom_dashboard_topic(request,id):
    try:
        dashboard = Dashboard.objects.get(id=id)
    except Dashboard.DoesNotExist:
        return HttpResponse("Dashboard does not exist")
    
    components = Component.objects.all()
    form = DashboardIndicatorForm(request.POST or None)

    if request.method == 'POST':
        #save row
        if 'rank' in request.POST:
            row = Row()
            row.for_dashboard = dashboard
            row.rank = request.POST['rank']
            row.save()

            response = {'success' : True, 'row' : row.id }
            return JsonResponse( response)


    context = {
        'dashboard' : dashboard,
        'components' : components,
        'form' : form
    }
    return render(request, 'user-admin/dashboard-admin/index.html', context=context)





################EXPORT DATA####################
@login_required(login_url='login')
def export_topic(request):
    topic = TopicResource()
    dataset = topic.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="topic.xlsx"'
    return response



@login_required(login_url='login')
def export_category(request):
    category = CategoryResource()
    dataset = category.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="category.xlsx"'
    return response


@login_required(login_url='login')
def export_indicator(request):
    indicator = IndicatorResource()
    dataset = indicator.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="indicator.xlsx"'
    return response

