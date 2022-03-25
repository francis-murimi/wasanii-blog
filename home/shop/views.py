from django.shortcuts import render, get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Category,Art,Preference
from orders.models import Order, Bids
from django.contrib.auth.decorators import login_required
from .forms import BiddingForm, ArtAddForm
from django.contrib.auth.models import User
from django.db.models import Max
from datetime import datetime,timedelta,date
from home.models import ArtistProfile
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

def art_list(request, category_slug=None):
    # get the list of all arts that can be bided on.
    template = loader.get_template('shop/art/list.html')
    category = None
    categories = Category.objects.all()
    arts = Art.objects.all()
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        arts = arts.filter(category=category)
    
    context = {'category':category,
                'categories':categories,
                'arts':arts,}
    return HttpResponse(template.render(context,request))

def art_detail(request, id, slug):
    # show the detail of an individual art that can be bided on.
    template = loader.get_template('shop/art/detail.html')
    art = get_object_or_404(Art,id=id,slug=slug)
    context = {'art': art,}
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def bidding_detail(request,id,slug):
    art = get_object_or_404(Art,id=id,slug=slug,available=True)
    bids = Bids.objects.filter(product = art).order_by('-created')
    bid_count = Bids.objects.filter(product = art).count()
    context = {'art': art,'bids':bids,'bid_count':bid_count}
    template = loader.get_template('shop/art/bidding.html')
    return HttpResponse(template.render(context,request))

@login_required(login_url='/login/')
def bidding(request,id,slug):
    # the bidding process
    art = get_object_or_404(Art,id=id,slug=slug,available=True)
    start_date = art.updated
    end_bid_date = start_date + timedelta(days=7)
    tarehe = datetime.today()
    if start_date < tarehe < end_bid_date:
        bei = ''
        b_bei = art.bid_price + 1
        if request.method == 'POST':
            form = BiddingForm(request.POST)
            if form.is_valid():
                bid = form.cleaned_data.get('amount')
                if Bids.objects.filter(product = art).count() == 0:
                    bei = art.bid_price
                else:
                    bei = Bids.objects.filter(product = art).aggregate(Max('amount')).get('amount__max')
                
                if bid > art.bid_price:
                    bids = form.save(commit=False)
                    bids.bidder = request.user
                    bids.product = Art.objects.get(name=art.name,id=art.id)
                    bids.save()
        else:
            form = BiddingForm()
        a_bids = Bids.objects.order_by('-created').filter(product = art)[:15]
        context = {'art': art,'form':form,'a_bids':a_bids,'bei':bei,'b_bei':b_bei,}
        template = loader.get_template('shop/art/bidding.html')
        return HttpResponse(template.render(context,request))
    else:
        winner = ''
        bei = Bids.objects.filter(product = art).aggregate(Max('amount')).get('amount__max')
        top_bid = Bids.objects.filter(product = art,amount= bei).order_by('-created')
        winner = top_bid[0].bidder
        order = Order.objects.create(orderer = winner, product = art,cost=top_bid[0].amount)
        art.available = False
        art.save()
        return redirect('shop:art_list')

@login_required(login_url='/login/')
def add_art(request):
    # check if the user is an artist
    a = request.user
    b = ArtistProfile.objects.filter(user=a).count()
    if b == 1:
        return redirect('shop:art_add')
    else:
        return HttpResponse('Sorry.You are not registered as an artist.')
    
class art_add(CreateView):
    # adding an art
    model = Art
    form_class = ArtAddForm
    template_name = 'shop/add_art.html'
    success_url = reverse_lazy('shop:art_list')
    def get_form_kwargs(self):
        kwargs = super(art_add, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs 

@login_required(login_url='/login/')
def artpreference(request,artid, userpreference):
    if request.method == "POST":
        eachpost= get_object_or_404(Art, id=artid)
        aa = eachpost.id
        ss = eachpost.slug
        obj=''
        valueobj=''
        try:
            obj= Preference.objects.get(user= request.user, art= eachpost)
            valueobj= obj.value #value of userpreference
            valueobj= int(valueobj)
            userpreference= int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref= Preference()
                upref.user= request.user
                upref.art= eachpost
                upref.value= userpreference
                if userpreference == 1 and valueobj != 1:
                    eachpost.likes += 1
                    eachpost.dislikes -=1
                elif userpreference == 2 and valueobj != 2:
                        eachpost.dislikes += 1
                        eachpost.likes -= 1
                upref.save()
                eachpost.save()
                return redirect('shop:art_detail',id=aa,slug=ss)

            elif valueobj == userpreference:
                obj.delete()
                if userpreference == 1:
                    eachpost.likes -= 1
                elif userpreference == 2:
                    eachpost.dislikes -= 1
                eachpost.save()
                return redirect('shop:art_detail',id=aa,slug=ss)
        except Preference.DoesNotExist:
            upref= Preference()
            upref.user= request.user
            upref.art= eachpost
            upref.value= userpreference
            userpreference= int(userpreference)
            if userpreference == 1:
                eachpost.likes += 1
            elif userpreference == 2:
                eachpost.dislikes +=1
            upref.save()
            eachpost.save()                            
            return redirect('shop:art_detail',id=aa,slug=ss)

    else:
        eachpost= get_object_or_404(Art, id=artid)
        return redirect('home')