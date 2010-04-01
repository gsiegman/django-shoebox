from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from uploadify.views import upload_recieved
from photologue.models import Photo

class Shoebox(models.Model):
    owner = models.ForeignKey(User, unique=True)
    
class ShoeboxUpload(models.Model):
    file = models.FileField(upload_to='holding')
    new_upload = models.BooleanField()
    
    def __unicode__(self):
        return self.file.name

class ShoeboxItem(models.Model):
    shoebox = models.ForeignKey(Shoebox)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return 'Shoebox Item: %s - %s' % (self.content_type.name, self.object_id)

def upload_received_handler(sender, data, **kwargs): 
    if file:
        new_media = ShoeboxUpload.objects.create(
            file = data,
            new_upload = True,
        )

        new_media.save()

upload_recieved.connect(upload_received_handler, dispatch_uid="shoebox.models.upload_recieved")