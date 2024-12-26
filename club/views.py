from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import modelformset_factory, formset_factory,inlineformset_factory
from .forms import LedagerForm, EntryQueueForm,EntryValueForm
from .models import RecordLedgers, EntryQueue, EntryValue

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
    # Get related EntryQueue instances (these are the "columns")
    related_column_names = EntryQueue.objects.filter(record_ledgers__id=id)
    total_related_columns = related_column_names.count()

    # Create the formset factory for EntryValue forms (these are the "rows")
    formset = inlineformset_factory(EntryQueue, EntryValue, form=EntryValueForm, extra=4, fk_name="column", can_delete=False)

    if request.method == 'POST':
        # Create and bind formset with POST data
        formset_instance = formset(request.POST)
        
        # Assign each form in the formset to its respective EntryQueue column
        for i, form in enumerate(formset_instance):
            # Ensure we link each form to the correct EntryQueue (column)
            form.instance.column = related_column_names[i]  # Link form to the appropriate column

        if formset_instance.is_valid():
            formset_instance.save()  # Save all valid forms (rows)

        return redirect('club:success_record_column')

    else:
        # Initialize empty formset for GET request, passing queryset of EntryQueue instances
        formset_instance = formset(queryset=related_column_names)

        context = {
            'related_column_names': related_column_names,
            'total_related_columns': total_related_columns,
            'formset': formset_instance
        }
        return render(request, "club/book/edit_book.html", context)


def success_record_col(request):
    last_record = RecordLedgers.objects.latest('created_at') 
    return render(request, 'club/success.html', {'last_record': last_record})


def club_dashboard(request):
    query_record_ledagers =  RecordLedgers.objects.all()
    context = {"created_book_records":query_record_ledagers,}
    return render(request, "club/club_dashboard.html", context)