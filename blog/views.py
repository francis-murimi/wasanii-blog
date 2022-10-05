from django.shortcuts import render, get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Category,Blog,Preference,Comment,Topic,TopicVote, TComment
from django.contrib.auth.decorators import login_required
from .forms import BlogAddForm, CommentForm,TopicForm, TCommentForm,BlogEditForm
from django.contrib.auth.models import User
from home.models import WriterProfile
from django.views.generic import CreateView 
from django.urls import reverse_lazy
from django.contrib.auth.models import User

def blog_list(request, category_slug=None):
    # get the list of all arts that can be bided on.
    template = loader.get_template('blog/list.html')
    category = None
    categories = Category.objects.all()
    blogs = Blog.objects.filter(status= 1)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        blogs = blogs.filter(category=category)
    
    context = {'category':category,
                'categories':categories,
                'blogs':blogs,}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def blog_detail(request, id, slug):
    # show the detail of an individual blog that can be bided on.
    template = loader.get_template('blog/detail.html')
    blog = get_object_or_404(Blog,id=id,slug=slug)
    # count views
    blog.blog_views = blog.blog_views+1
    blog.save()
    comments = Comment.objects.filter(blog= blog)
    new_comment = None
    # Comment posted
    if request.method == 'POST': 
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.blog = blog
            new_comment.name = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'blog':blog,'comments': comments,'new_comment': new_comment,'comment_form': comment_form}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def edit_list(request):
    username = request.user
    try:
        profile = WriterProfile.objects.get(user=username)
        #profile_ = WriterProfile.objects.filter(user=username)
        #profile = WriterProfile.objects.get(user=username)
        blogs = Blog.objects.filter(writer=profile)
        context = {'profile':profile,'blogs':blogs,}
        template = loader.get_template('blog/edit_list.html')
        return HttpResponse(template.render(context,request))
    except WriterProfile.DoesNotExist:
        return HttpResponse('You are not registered as a writer.')


@login_required(login_url='/login/')
def archive_blog(request,id):
    blog = get_object_or_404(Blog,id=id)
    blog.status = 0
    blog.save()
    return redirect('blog:edit_list')

@login_required(login_url='/login/')
def publish_blog(request,id):
    blog = get_object_or_404(Blog,id=id)
    blog.status = 1
    blog.save()
    return redirect('blog:edit_list')

@login_required(login_url='/login/')
def edit_blog(request,id):
    blog = get_object_or_404(Blog,id=id)
    if request.method == 'POST':
        form = BlogEditForm(request.POST,request.FILES,instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:edit_list')
    else:
        form = BlogEditForm(instance=blog)
    template = loader.get_template('blog/edit_blog.html')
    context = {'form':form}
    return HttpResponse(template.render(context,request)) 


@login_required(login_url='/login/')
def add_blog(request):
    # check if the user is an artist
    a = request.user
    b = WriterProfile.objects.filter(user=a).count()
    if b == 1:
        return redirect('blog:blog_add')
    else:
        return HttpResponse('Sorry.You are not registered as a writer.')
    
class blog_add(CreateView):
    # adding a blog
    model = Blog
    form_class = BlogAddForm
    template_name = 'blog/add_blog.html'
    success_url = reverse_lazy('blog:blog_list')
    def get_form_kwargs(self):
        kwargs = super(blog_add, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs 

@login_required(login_url='/login/')
def blogpreference(request,blogid, userpreference):
    if request.method == "POST":
        eachpost= get_object_or_404(Blog, id=blogid)
        aa = eachpost.id
        ss = eachpost.slug
        obj=''
        valueobj=''
        try:
            obj= Preference.objects.get(user= request.user, blog= eachpost)
            valueobj= obj.value #value of userpreference
            valueobj= int(valueobj)
            userpreference= int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref= Preference()
                upref.user= request.user
                upref.blog= eachpost
                upref.value= userpreference
                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -=1
                elif userpreference == 2 and valueobj != 2:
                        eachpost.dislikes += 1
                        eachpost.likes -= 1
                upref.save()
                eachpost.save()
                return redirect('blog:blog_detail',id=aa,slug=ss)

            elif valueobj == userpreference:
                obj.delete()
                if userpreference == 1:
                    eachpost.likes -= 1
                elif userpreference == 2:
                    eachpost.dislikes -= 1
                eachpost.save()
                return redirect('blog:blog_detail',id=aa,slug=ss)
        except Preference.DoesNotExist:
            upref= Preference()
            upref.user= request.user
            upref.blog= eachpost
            upref.value= userpreference
            userpreference= int(userpreference)
            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes +=1
            upref.save()
            eachpost.save()                            
            return redirect('blog:blog_detail',id=aa,slug=ss)

    else:
        eachpost= get_object_or_404(Blog, id=blogid)
        return redirect('home')

@login_required(login_url='/login/')
def add_topic(request):
    # show the detail of an individual blog that can be bided on.
    template = loader.get_template('blog/add_topic.html')
    topics = Topic.objects.all()
    new_topic = None
    # Comment posted
    if request.method == 'POST':
        topic_form = TopicForm(data=request.POST)
        if topic_form.is_valid():
            # Create Comment object but don't save to database yet
            new_topic = topic_form.save(commit=False)
            # Assign the current post to the comment
            new_topic.proposer = request.user
            # Save the comment to the database
            new_topic.save()
    else:
        topic_form = TopicForm()
    context = {'topics':topics,'new_topic': new_topic,'topic_form': topic_form}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def topic_detail(request, id):
    # show the detail of an individual blog that can be bided on.
    template = loader.get_template('blog/topic_detail.html')
    topic = get_object_or_404(Topic,id=id)
    comments = TComment.objects.filter(topic= topic)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        t_comment_form = TCommentForm(data=request.POST)
        if t_comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = t_comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.topic = topic
            new_comment.name = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        t_comment_form = TCommentForm()
    context = {'topic':topic,'comments': comments,'new_comment': new_comment,'t_comment_form': t_comment_form}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def topicpreference(request,topicid, userpreference):
    if request.method == "POST":
        eachpost= get_object_or_404(Topic, id=topicid)
        aa = eachpost.id
        obj=''
        valueobj=''
        try:
            obj= TopicVote.objects.get(user= request.user, topic= eachpost)
            valueobj= obj.value #value of userpreference
            valueobj= int(valueobj)
            userpreference= int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref= TopicVote()
                upref.user= request.user
                upref.topic= eachpost
                upref.value= userpreference
                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -=1
                elif userpreference == 2 and valueobj != 2:
                        eachpost.dislikes += 1
                        eachpost.likes -= 1
                upref.save()
                eachpost.save()
                return redirect('blog:topic_detail',id=aa)

            elif valueobj == userpreference:
                obj.delete()
                if userpreference == 1:
                    eachpost.likes -= 1
                elif userpreference == 2:
                    eachpost.dislikes -= 1
                eachpost.save()
                return redirect('blog:topic_detail',id=aa)
        except TopicVote.DoesNotExist:
            upref= TopicVote()
            upref.user= request.user
            upref.topic= eachpost
            upref.value= userpreference
            userpreference= int(userpreference)
            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes +=1
            upref.save()
            eachpost.save()                            
            return redirect('blog:topic_detail',id=aa)

    else:
        eachpost= get_object_or_404(Topic,topicid)
        return redirect('home')

def create_category(request):
    topics = Topic.objects.filter(active=False)
    for topic in topics:
        if topic.likes > 5:
            #order = Order.objects.create(orderer = winner, product = art,cost=top_bid[0].amount)
            added = Category.objects.create(name=topic.name,description=topic.description)
            topic.active = True
            topic.save()
    return redirect('blog:blog_list')