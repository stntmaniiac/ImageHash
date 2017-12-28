from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.views import generic,View
from .forms import ImageForm
from django.http import HttpResponse
import os
from untitled2 import settings
from .models import Images
import hashlib

@receiver (post_save, sender=Images )
def generate_hash(instance, update_fields, *args, **kwargs ):

    #generate hash value of instance image
    name = os.path.basename(instance.imagesrc.name)
    filename = os.path.join(settings.BASE_DIR, 'media/')
    hasher=hashlib.md5()
    with open(os.path.join(filename, name), 'rb') as open_file:
        content=open_file.read()
        hasher.update(content)
    value=hasher.hexdigest()

    #retrieve hashvalues from database
    e=Images.objects.all().values_list('hashvalue')
    result = []
    for t in e:
        for x in t:
            result.append(x)
    print (result)

    #checking for duplicate image
    if value in result:
        print('duplicate Image')
        Images.objects.filter(id=instance.id).delete()
        return False

    else:
        #print(value)
        print("new image")
        instance.hashvalue=value
        post_save.disconnect(generate_hash, sender=Images)
        instance.save(update_fields={'hashvalue'})
        post_save.connect(generate_hash, sender=Images)
        return True

class UploadImage(View):
    form_class=ImageForm
    template_name='image/form.html'
    fields = ['title','content','imagesrc']

    def get (self, request):
        form=self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post (self, request):
        form=self.form_class(request.POST, request.FILES)
        if form.is_valid():
           a= form.save()
           if a.hashvalue is not None:
               return redirect('image:index')
               exit()
        return HttpResponse('<h1>DUplicate Image</h1>')

class IndexView(generic.ListView):
    template_name = 'image/index.html'
    def get_queryset(self):
        return Images.objects.all()

class DetailView(generic.DetailView):
    model = Images
    template_name = 'image/details.html'