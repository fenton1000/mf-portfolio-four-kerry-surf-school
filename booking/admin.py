from django.contrib import admin
from .models import Customer, Booking
from .admin_filters import CustomDateFieldListFilter


admin.site.register(Customer)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = ('lesson_date', 'lesson_time', 'ability_level', 'approved')
    list_filter = (('lesson_date', CustomDateFieldListFilter), 'approved',)
    actions = ['approve_selected_bookings', 'disapprove_selected_bookings']

    def approve_selected_bookings(self, request, queryset):
        queryset.update(approved=True)

    def disapprove_selected_bookings(self, request, queryset):
        queryset.update(approved=False)
