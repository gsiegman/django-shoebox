from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from photologue.models import Photo
from shoebox.models import ShoeboxUpload
from shoebox.forms import ShoeboxPhotoForm

import shutil

def shoebox_index(request, **kwargs):
    """
    index page for shoebox
    """
    template_name = kwargs.get("template_name", "shoebox/shoebox_index.html")
	
    latest_photos = Photo.objects.all()[:10]
    
    return render_to_response(template_name, {
		"latest_photos": latest_photos
	}, context_instance=RequestContext(request))

def shoebox_image_gallery(request, **kwargs):
    """
    main image gallery
    """
    template_name = kwargs.get("template_name", "shoebox/shoebox_image_gallery.html")
    
    photos = Photo.objects.all().order_by('-date_added')
    
    return render_to_response(template_name, {
        'photos': photos
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
    
    photos = Photo.objects.filter(title__icontains=q)[:limit]
    
    #if request.is_ajax():
    #    return HttpResponse(results, 
    #        mimetype='text/plain')
    #else:
    return render_to_response(template_name, {
        'photos': photos
    }, context_instance=RequestContext(request))