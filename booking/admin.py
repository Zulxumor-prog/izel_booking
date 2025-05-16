from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Agent, Booking, TourSchedule

class CustomAdminSite(admin.AdminSite):
    site_header = "IZEL Booking Admin"
    site_title = "IZEL Admin"
    index_title = "Xush kelibsiz!"

    def index(self, request, extra_context=None):
        yangi_bronlar = Booking.objects.filter(status='Yangi')
        if yangi_bronlar.exists():
            message = "Yangi bronlar:<br><ul>"
            for booking in yangi_bronlar:
                message += f"<li><strong>{booking.client_name}</strong> — {booking.phone} — {booking.route} — <em>Status: {booking.status}</em> — <span style='color:green'>Agent: {booking.agent.name}</span></li>"
            message += "</ul>"
            messages.info(request, mark_safe(message))
        return super().index(request, extra_context=extra_context)

custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(Booking)
custom_admin_site.register(TourSchedule)
custom_admin_site.register(Agent)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'tour', 'agent', 'agent_commission', 'status', 'created_at')
    list_filter = ('tour', 'status', 'agent')
    search_fields = ('client_name', 'phone')
    list_editable = ('status',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(status='Yangi')

    def agent_commission(self, obj):
        return obj.commission

admin.site.register(Agent)
admin.site.register(TourSchedule)
