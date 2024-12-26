from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import modelformset_factory, formset_factory,inlineformset_factory
from .forms import LedagerForm, EntryQueueForm,EntryValueForm
from .models import RecordLedgers, EntryQueue, EntryValue


from django.forms import modelformset_factory

'''
def create_new_record(request):
    EntryQueueFormSet = modelformset_factory(EntryQueue, form=EntryQueueForm, extra=0, can_delete=False)
    if request.method == 'POST':
        ledger_form = LedagerForm(request.POST)
        column_head_formset = EntryQueueFormSet(request.POST, queryset=EntryQueue.objects.none(), prefix='column_head_form')
        if ledger_form.is_valid() and column_head_formset.is_valid():
            ledger_instance = ledger_form.save()  # Save the RecordLedgers instance
            for form in column_head_formset:
                entry_queue = form.save(commit=False)
                entry_queue.record_ledgers = ledger_instance  # Manually link to the RecordLedgers instance
                entry_queue.save()
            return redirect('club:success_record_column')
    else:
        ledger_form = LedagerForm()
        column_head_formset = EntryQueueFormSet(queryset=EntryQueue.objects.none(), prefix='column_head_form')
    return render(request, 'club/create_ledager.html', {'ledager_form': ledger_form, 'column_head_formset': column_head_formset})

def add_column_head_form(request):
    total_forms = int(request.POST.get('column_head_form-TOTAL_FORMS', 0))
    EntryQueueFormSet = modelformset_factory(EntryQueue, form=EntryQueueForm, extra=total_forms, can_delete=False)
    column_head_formset = EntryQueueFormSet(queryset=EntryQueue.objects.none(), prefix='column_head_form')
    return render(request, 'club/partial_column_head_form.html', {'column_head_formset': column_head_formset, 'total_forms': total_forms})

'''

from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect

def create_new_record(request):
    EntryQueueFormSet = inlineformset_factory(
        RecordLedgers, EntryQueue, form=EntryQueueForm, extra=0, fk_name="record_ledgers", can_delete=False
    )
    if request.method == 'POST':
        ledger_form = LedagerForm(request.POST)
        column_head_formset = EntryQueueFormSet(request.POST, prefix='column_head_form')
        if ledger_form.is_valid() and column_head_formset.is_valid():
            # Save the RecordLedgers instance first
            ledger_instance = ledger_form.save()
            # Assign the saved instance to the formset
            column_head_formset.instance = ledger_instance
            # Save the formset
            column_head_formset.save()
            return redirect('club:success_record_column')
    else:
        ledger_form = LedagerForm()
        column_head_formset = EntryQueueFormSet(queryset=EntryQueue.objects.none(), prefix='column_head_form')
    return render(request, 'club/create_ledager.html', {'ledager_form': ledger_form, 'column_head_formset': column_head_formset})

def add_column_head_form(request):
    total_forms = int(request.POST.get('column_head_form-TOTAL_FORMS', 0))
    EntryQueueFormSet = inlineformset_factory(
        RecordLedgers, EntryQueue, form=EntryQueueForm, extra=total_forms, fk_name="record_ledgers", can_delete=False
    )
    column_head_formset = EntryQueueFormSet(queryset=EntryQueue.objects.none(), prefix='column_head_form')
    return render(request, 'club/partial_column_head_form.html', {'column_head_formset': column_head_formset, 'total_forms': total_forms})





def insert_databook(request, id):
    related_column_names = EntryQueue.objects.filter(record_ledgers__id=id)
    context = {'related_column_names':related_column_names,}
    return render(request ,"club/book/edit_book.html", context)

def success_record_col(request):
    last_record = RecordLedgers.objects.latest('created_at') 
    return render(request, 'club/success.html', {'last_record': last_record})


def club_dashboard(request):
    query_record_ledagers =  RecordLedgers.objects.all()
    context = {"created_book_records":query_record_ledagers,}
    return render(request, "club/club_dashboard.html", context)