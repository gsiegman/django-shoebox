from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from photologue.models import Photo, PhotoSize
from shoebox.models import ShoeboxUpload
from shoebox.forms import ShoeboxPhotoForm

import shutil

def shoebox_index(request, **kwargs):
    """
    index page for shoebox
    """
    template_name = kwargs.get("template_name", "shoebox/shoebox_index.html")
	
    latest_images = Photo.objects.all()[:20]
    
    return render_to_response(template_name, {
		"latest_images": latest_images
	}, context_instance=RequestContext(request))

def shoebox_image_gallery(request, **kwargs):
    """
    main image gallery
    """
    template_name = kwargs.get("template_name", "shoebox/shoebox_image_gallery.html")
    
    images = Photo.objects.all().order_by('-date_added')
    
    return render_to_response(template_name, {
        'images': images
    }, context_instance=RequestContext(request))

def new_upload_holding(request):
    forms = []
    new_uploads = ShoeboxUpload.objects.filter(new_upload=True)
    
    for new_upload in new_uploads:
        forms.append(ShoeboxPhotoForm(initial={'file': new_upload.file.name}, auto_id=False))
        
    files_uploaded = request.POST.get('filesUploaded', 0)

    return render_to_response('shoebox/shoebox_new_upload_holding.html',
                                {'forms': forms,
                                    'files_uploaded': files_uploaded},
                                context_instance=RequestContext(request))
                                
def manage_new_upload(request):
    holding_location = request.POST['file']
    file_location = holding_location.replace('holding/', 'photologue/photos/')
    media_root = settings.MEDIA_ROOT
    
    shutil.move(media_root + holding_location, media_root + file_location)
    
    new_photo = Photo.objects.create(image=file_location, 
                                    title=request.POST['title'], 
                                    title_slug=request.POST['slug'])
                                    
    deleted_holding_file = ShoeboxUpload.objects.filter(file=holding_location).delete()
    
    return HttpResponseRedirect('/shoebox/new_uploads/')

class ItemManagementView(object):
    """
    a class-based view to dispatch to the appropriate managed media type
    
    insired by http://www.djangosnippets.org/snippets/1582/
    """
    
    @classmethod
    def dispatch(cls, request, *args, **kwargs):
        return cls().__dispatch(request, *args, **kwargs)
    
    def __dispatch(self, request, *args, **kwargs):
        try:
            return getattr(self, 'manage_%s' % kwargs['object_type'])(request, *args, **kwargs)
        except AttributeError:
            return self.__managed_type_not_allowed(*args, **kwargs)
    
    def __managed_type_not_allowed(self, *args, **kwargs):
        response = HttpResponse('This type is not managed by Shoebox: %s' % kwargs['object_type'])
        response.status_code = 400
        return response
    
    def manage_image(self, request, *args, **kwargs):
        image = get_object_or_404(Photo, pk=kwargs['object_id'])
        image_sizes = [{
            'url': getattr(image, 'get_%s_url' % size.name)(), 
            'name': size.name
        } for size in PhotoSize.objects.all()]
        
        return render_to_response('shoebox/shoebox_manage_item.html', {
            'type': kwargs['object_type'],
            'object': image,
            'photo_sizes': image_sizes,
        }, context_instance=RequestContext(request))

def image_search(request, **kwargs):
    """
    image search
    """
    template_name = kwargs.get("template_name", "shoebox/image_search_results.html")
    
    q = request.GET.get('q')
    limit = request.GET.get('limit', 20)
    
    try:
        limit = int(limit)
    except ValueError:
        return HttpResponseBadRequest
    
    images = Photo.objects.filter(title__icontains=q)[:limit]
    
    return render_to_response(template_name, {
        'images': images
    }, context_instance=RequestContext(request))