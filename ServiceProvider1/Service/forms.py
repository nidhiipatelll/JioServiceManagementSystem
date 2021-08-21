from django import forms
from .models import TblSheetDetails


class FileUpload(forms.ModelForm):
    class Meta:
        model = TblSheetDetails
        fields = [
            'uTime',
            'uDate',
            'sheet'
        ]
