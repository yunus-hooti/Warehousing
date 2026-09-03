from django.contrib import admin
import openpyxl
from django.http import HttpResponse

from .models import EntryExit


# Register your models here.


def exal(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exal.xlsx"'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Departures and arrivals"
    columns = ['کالا', 'تامین کننده', 'نوع', 'تعداد', 'زمان ثبت']
    ws.append(columns)
    for i in queryset:
        created = i.created_at.replace(tzinfo=None)
        # created = order.created.replace(tzinfo=None) if order.created else ''

        ws.append([i.good.name, i.supplier_good.name
                      , i.type_of_operation, i.number, created])
    wb.save(response)
    return response


exal.short_description = 'خروجی اکسل از گزارشات'


@admin.register(EntryExit)
class EntryExitAdmin(admin.ModelAdmin):
    list_display = ['good', 'supplier_good', 'type_of_operation', 'created_at']
    list_filter = ['supplier_good', 'type_of_operation']
    actions = [exal]
