from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import FAQ, ContactUs, StaticPages


@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('question', 'answer', 'order')
    list_editable= ('order', )

@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    pass 

@admin.register(StaticPages)
class StaticPagesAdmin(ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)} 
