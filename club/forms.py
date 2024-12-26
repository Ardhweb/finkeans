from django import forms
from club.models import RecordLedgers,EntryQueue,EntryValue


class LedagerForm(forms.ModelForm):
    class Meta:
        model = RecordLedgers
        fields = "__all__"
        widgets ={'title':forms.TextInput(attrs={'class':'form-control text-center w-50 '}),}
    def __init__(self, *args, **kwargs):
        super(LedagerForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "RecordBook~ Khata Naam"

class EntryQueueForm(forms.ModelForm):
    class Meta:
        model = EntryQueue
        fields = ['column_title']
        widgets ={'column_title':forms.TextInput( attrs={'class':'  border-bottom  form-control text-center  fw-semibold ', 'placeholder': 'Column Name'}),}
    
    #Hide For All Labels from Form
    # def __init__(self, *args, **kwargs):
    #     super(EntryQueueForm, self).__init__(*args, **kwargs)
    #     # Hide labels and retain help_text
    #     for field_name, field in self.fields.items():
    #         field.label = ''  # Hide the label

    def __init__(self, *args, **kwargs):
        super(EntryQueueForm, self).__init__(*args, **kwargs)
        self.fields['column_title'].label = ""          


class EntryValueForm(forms.ModelForm):
    class Meta:
        model = EntryValue
        fields = ['entries_value']
        widgets ={'entries_value':forms.TextInput( attrs={'class':'border-0 bg-transparent h-100   form-control',}),}
    
    def __init__(self, *args, **kwargs):
        super(EntryValueForm, self).__init__(*args, **kwargs)
        self.fields['entries_value'].label = "" 