from django.conf.urls.defaults import *
from photologue.models import Photo
from shoebox.forms import ShoeboxPhotoForm

urlpatterns = patterns('',
    url(r'^$', 
        'shoebox.views.shoebox_index', 
        name="shoebox_index"
    ),
    url(r'^images/$', 
        'shoebox.views.shoebox_image_gallery', 
        name="shoebox_gallery"
    ),
    url(r'^new_uploads/$',
        'shoebox.views.new_upload_holding',
        name="shoebox_new_uploads"
    ),
    url(r'^manage_new_upload/$',
        'shoebox.views.manage_new_upload',
        name="shoebox_manage_new_upload"
    ),
    url(r'^item/(?P<object_id>\d+)/$', 
        'django.views.generic.list_detail.object_detail', 
        {'queryset': Photo.objects.all(),
         'template_name': 'shoebox/shoebox_item.html'}, 
         name='shoebox_shoebox_item'
    ),
    url(r'^image_search/$',
        'shoebox.views.image_search',
        name='shoebox_image_search'
    )
)

#ajax-validation urls
urlpatterns += patterns('',
    url(r'^validate_new_uploads/$',
        'ajax_validation.views.validate',
        {'form_class': ShoeboxPhotoForm},
        name='shoebox_new_upload_validation',
    ),
)