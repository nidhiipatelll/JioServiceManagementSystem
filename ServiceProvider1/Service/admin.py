from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin


@admin.register(TblRegistration)
class ViewAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(TblCustomerDetails, TblSheetData, TblSheetDetails)
class ViewAdmin(ImportExportActionModelAdmin):
    pass


