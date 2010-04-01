
from south.db import db
from django.db import models
from shoebox.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ShoeboxItem'
        db.create_table('shoebox_shoeboxitem', (
            ('id', orm['shoebox.ShoeboxItem:id']),
            ('shoebox', orm['shoebox.ShoeboxItem:shoebox']),
            ('content_type', orm['shoebox.ShoeboxItem:content_type']),
            ('object_id', orm['shoebox.ShoeboxItem:object_id']),
        ))
        db.send_create_signal('shoebox', ['ShoeboxItem'])
        
        # Adding model 'ShoeboxUpload'
        db.create_table('shoebox_shoeboxupload', (
            ('id', orm['shoebox.ShoeboxUpload:id']),
            ('file', orm['shoebox.ShoeboxUpload:file']),
            ('new_upload', orm['shoebox.ShoeboxUpload:new_upload']),
        ))
        db.send_create_signal('shoebox', ['ShoeboxUpload'])
        
        # Adding model 'Shoebox'
        db.create_table('shoebox_shoebox', (
            ('id', orm['shoebox.Shoebox:id']),
            ('owner', orm['shoebox.Shoebox:owner']),
        ))
        db.send_create_signal('shoebox', ['Shoebox'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ShoeboxItem'
        db.delete_table('shoebox_shoeboxitem')
        
        # Deleting model 'ShoeboxUpload'
        db.delete_table('shoebox_shoeboxupload')
        
        # Deleting model 'Shoebox'
        db.delete_table('shoebox_shoebox')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shoebox.shoebox': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'shoebox.shoeboxitem': {
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shoebox': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shoebox.Shoebox']"})
        },
        'shoebox.shoeboxupload': {
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_upload': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['shoebox']
