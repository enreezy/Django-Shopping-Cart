from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.conf import settings

import os

from .models import Items, Accounts



class IndexView(generic.ListView):
	template_name = 'home/index.html'
	context_object_name = 'latest_item_list'


	def get_queryset(self):
		return Items.objects.all()


class crud():


	def login(request):

		
		if not request.session.get('username'):
			
			return render(request, "home/login.html")
		else:
			items = Items.objects.all()

			return render(request, "home/admin.html",{"items":items})

	def loginsubmit(request):

		username = request.POST['username']
		password = request.POST['password']
		data = "account not exist"

		accounts = Accounts.objects.filter(username=username, password=password)

		if accounts:
			request.session['username'] = username
			return HttpResponseRedirect(reverse('home:admin'))
		else:
			return render(request, "home/login.html",{"data":data})

	def admin(request):


		if not request.session.get('username'):
			
			return render(request, "home/login.html")
		else:
			items = Items.objects.all()

			return render(request, "home/admin.html",{"items":items})

	def logout(request):

		del request.session['username']

		return HttpResponseRedirect(reverse('home:index'))

	def additem(request):

		sv = Items(itemname=request.POST['itemname'], itemprice=request.POST['itemprice'], category=request.POST['category'], image=request.FILES['image'])
		sv.save()

		items = Items.objects.all()

		return render(request, "home/admin.html", {"items":items})

	def edit(request, data_id):

		data = get_object_or_404(Items, pk=data_id)
		items = Items.objects.all()

		return render(request, "home/admin.html", {"data":data, "iid":data_id, "items":items})


	def update(request):
		ed = Items.objects.get(id=request.POST['iid'])

		imagePath = os.path.join(settings.MEDIA_ROOT, ed.image.name)

		if 'image' in request.FILES:
			ed.image = request.FILES['image']
			if os.path.isfile(imagePath):
				os.remove(imagePath)

		ed.itemname=request.POST['itemname']
		ed.itemprice=request.POST['itemprice']
		ed.category=request.POST['category']

		ed.save()

		items = Items.objects.all()

		return render(request,"home/admin.html",{"items":items})

	def delete(request, data_id):
		dl = Items.objects.get(id=data_id)

		imagePath = os.path.join(settings.MEDIA_ROOT, dl.image.name)

		if os.path.isfile(imagePath):
			os.remove(imagePath)

		dl.delete()

		items = Items.objects.all()

		return render(request, "home/admin.html",{"items":items})

	def details(request, data_id):

		items = get_object_or_404(Items, pk=data_id)

		return render(request, "home/details.html",{"items":items})

	def addtocart(request, data_id):

		if not request.session.get('cart'):
			request.session["cart"] = 1
			request.session["mycart"] = []
			item = get_object_or_404(Items, pk=data_id)
			request.session["id"] = 0
			mycartdict = {"id":request.session["id"], "itemname":item.itemname, "itemprice":item.itemprice, "quantity":"1", "category":item.category}
			request.session["mycart"].append(mycartdict)	

		else:
			request.session["cart"] += 1
			item = get_object_or_404(Items, pk=data_id)
			request.session["id"] += 1
			mycartdict = {"id":request.session["id"], "itemname":item.itemname, "itemprice":item.itemprice, "quantity":"1", "category":item.category}
			request.session["mycart"].append(mycartdict)	

		
		
		return HttpResponseRedirect(reverse('home:details', args=(data_id)))

	def cart(request):
		if not request.session.get('mycart'):
			return render(request,"home/cart.html")
		else:
			itotal = 0
			ttotal = 0
			total = 0
			for cart in request.session["mycart"]:
				itotal = int(cart["quantity"]) * int(cart["itemprice"])
				total += itotal
				
		return render(request,"home/cart.html",{"total":total})

		

	def emptycart(request):

		del request.session["mycart"]
		del request.session["cart"]


		return HttpResponseRedirect(reverse("home:cart"))


	def updatequantity(request, item_no):
		request.session["quantity"] = request.POST['quantity']
		request.session["mycart"][int(item_no)-1]["quantity"] = request.session["quantity"]

		for cart in request.session["mycart"]:
			itotal = int(request.session["quantity"]) * int(cart["itemprice"])
			request.session["total"] = itotal

		return HttpResponseRedirect(reverse("home:cart"))

	def removecart(request, item_no):

		request.session.modified = True
		request.session["cart"] = request.session["cart"] - 1
		del request.session["mycart"][int(item_no)-1]

		return render(request, "home/cart.html")



