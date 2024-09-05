from django.shortcuts import render , redirect
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from Base.models import Topic
from .forms import TopicForm
from django.contrib import messages

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
    return JsonResponse(response)  
  
