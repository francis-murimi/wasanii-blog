from django.shortcuts import render, get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Legend,Preference,Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

def legend_list(request):
    # get the list of all legends.
    legends = Legend.objects.filter(published = True)
    context = {'legends':legends}
    template = loader.get_template('legends/list.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def legend_detail(request, id):
    # show the detail of an individual blog that can be bided on.
    template = loader.get_template('legends/detail.html')
    legend = get_object_or_404(Legend,id=id)
    comments = Comment.objects.filter(legend = legend)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.legend = legend
            new_comment.name = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'legend':legend,'comments': comments,'new_comment': new_comment,'comment_form': comment_form}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def legendpreference(request,legendid, userpreference):
    if request.method == "POST":
        eachpost= get_object_or_404(Legend, id=legendid)
        aa = eachpost.id
        #ss = eachpost.slug
        obj=''
        valueobj=''
        try:
            obj= Preference.objects.get(user= request.user, legend= eachpost)
            valueobj= obj.value #value of userpreference
            valueobj= int(valueobj)
            userpreference= int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref= Preference()
                upref.user= request.user
                upref.legend= eachpost
                upref.value= userpreference
                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -=1
                elif userpreference == 2 and valueobj != 2:
                        eachpost.dislikes += 1
                        eachpost.likes -= 1
                upref.save()
                eachpost.save()
                return redirect('legends:legend_detail',id=aa)

            elif valueobj == userpreference:
                obj.delete()
                if userpreference == 1:
                    eachpost.likes -= 1
                elif userpreference == 2:
                    eachpost.dislikes -= 1
                eachpost.save()
                return redirect('legends:legend_detail',id=aa)
        except Preference.DoesNotExist:
            upref= Preference()
            upref.user= request.user
            upref.legend= eachpost
            upref.value= userpreference
            userpreference= int(userpreference)
            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes +=1
            upref.save()
            eachpost.save()                            
            return redirect('legends:legend_detail',id=aa)

    else:
        eachpost= get_object_or_404(Legend, id=legendid)
        return redirect('home')