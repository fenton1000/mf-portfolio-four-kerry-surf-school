from datetime import date
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Customer, Booking
from .admin_filters import CustomDateFieldListFilter


admin.site.register(Customer)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'lesson_date',
        'lesson_time',
        'customer_name_link',
        'customer__age',
        'ability_level',
        'approved'
    )
    ordering = [
        'lesson_date',
        'lesson_time',
        '-customer__customer__date_of_birth'
    ]
    list_filter = (('lesson_date', CustomDateFieldListFilter), 'approved',)
    actions = ['approve_selected_bookings', 'disapprove_selected_bookings']

    def approve_selected_bookings(self, request, queryset):
        queryset.update(approved=True)

    def disapprove_selected_bookings(self, request, queryset):
        queryset.update(approved=False)
    
    def customer__age(self, obj):
        born = obj.customer.customer.date_of_birth
        today = date.today()
        return today.year - born.year - (
            (today.month, today.day) < (born.month, born.day)
        )

    def customer_name_link(self, obj):
        link = reverse('admin:booking_customer_change', args=[obj.customer.id])
        return format_html(
            '<a href="{}">{}</a>',
            link, obj.customer.customer.first_name
        ) if obj.customer.customer else None
