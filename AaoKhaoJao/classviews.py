from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.core.urlresolvers import reverse,reverse_lazy
from AaoKhaoJao.models import Restaurants,Menu
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponse

class restaurantcreateview(CreateView):
    model = Restaurants
    fields = ('name','location')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(restaurantcreateview, self).form_valid(form)

    def get_success_url(self):
        return reverse("list")


class restaurantupdateview(UpdateView):
    model = Restaurants
    fields = ('name','location')

    def get_success_url(self):
        return reverse("list")

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        result = Restaurants.objects.all().get(id=id)
        return result

class restaurantdeleteview(DeleteView):
    model = Restaurants
    fields = ('name','location')

    def get_success_url(self):
        return reverse_lazy("list")

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        result = Restaurants.objects.all().get(id=id)
        return result

def list(request):
    result = Restaurants.objects.filter(owner=request.user.id)
    template = get_template("page.html")
    return HttpResponse(template.render(context={'list': result}, request=request))

class menucreateview(CreateView):
    model=Menu
    fields = {'item','price'}

    def form_valid(self, form):
        form.instance.restaurant_id = Menu.objects.get(id=self.kwargs.get('pk'))
        return super(menucreateview, self).form_valid(form)

    def get_success_url(self):
        return reverse("posts", kwargs={'pk': self.kwargs.get('pk')})

class menuupdateview(UpdateView):
    model = Menu
    fields = {'item','price'}

    def get_success_url(self):
        return reverse("posts", kwargs={'pk': self.kwargs.get('id')})

class menudeleteview(DeleteView):
    model = Menu
    fields = {'item','price'}

    def get_success_url(self):
        return reverse("posts", kwargs={'pk': self.kwargs.get('id')})

def menus(request,pk):
    result=Menu.objects.filter(restaurant_id = pk)
    template = get_template("menu.html")
    return HttpResponse(template.render(context={'list': result,'id':pk}, request=request))
