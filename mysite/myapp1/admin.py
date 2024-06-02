from django.contrib import admin
from . models import event, location, category,sub_location,Ticket
from . import models
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Custom Fields', {'fields': ('is_verified', 'otp', 'forget_password_token', 'last_login_time', 'last_logout_time')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Register the User model with the custom admin class
admin.site.register(User, UserAdmin)

admin.site.index_template = 'admin/base_site.html'


class locationInline(admin.StackedInline):
    model = location
    extra= 0

# class subeventinline(admin.StackedInline):
#     model= subevent
#     extra= 0

class sublocation(admin.StackedInline):
    model= sub_location
    extra=0

class has_ticket(admin.StackedInline):
    model= Ticket
    extra= 0


class eventAdmin(admin.ModelAdmin):
    #inlines= [locationInline]
    inlines = [locationInline,sublocation,has_ticket]
    add_form_template = "admin/event_change_form.html"
    # inlines= [subeventinline]
    list_display = ('name', 'hassub_event')
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     obj = self.get_object(request, object_id)
    #     if obj.hassub_event:
    #         self.inlines = [locationInline, sublocation]
    #     else:
    #         self.inlines = [locationInline]
    #     return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)
# class eventtras(admin.ModelAdmin):
    

# class clint(admin.ModelAdmin):

#     list_display_links= ("client_name",)

#     def click_me(self,obj):
#         return format_html('<a href= "#" >view</a>')
class order1(admin.ModelAdmin):
    list_display= ('name','number','email','tickettype','number_of_tickets','totalprice','eventid')
    search_fields= ('eventid','id','name')
admin.site.register(models.Payorderss2,order1)

class client(admin.ModelAdmin):
    list_display= ('event','client_name')

admin.site.register(category)
admin.site.register(event, eventAdmin)
admin.site.register(models.Employees)
admin.site.register(models.eventEmployees)
admin.site.register(models.Clients,client)
admin.site.register(models.EventTransaction)
admin.site.register(models.userqr2)


   

# from django.contrib import admin
# from .models import category, event, location, subevent

# class SubeventInline(admin.TabularInline):
#     model = subevent

# class LocationInline(admin.StackedInline):
#     model = location

# class EventAdmin(admin.ModelAdmin):
#     inlines = [LocationInline]

#     def get_inline_instances(self, request, obj=None):
#         if obj and obj.hassub_event:
            
#             return [SubeventInline(self.model, self.admin_site)]
#         else:
#             return []
            
# admin.site.register(category)
# admin.site.register(event, EventAdmin)
