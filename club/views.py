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
    related_column_names = EntryQueue.objects.filter(record_ledgers__id=id)
    formset = inlineformset_factory(EntryQueue, EntryValue, form=EntryValueForm, extra=4, fk_name="column", can_delete=False)
    if request.method == 'POST':
        total_forms_count = request.POST.get('entryvalue_set-TOTAL_FORMS') 
        print(formset)
        for name in related_column_names:
            column_title = name.column_title  # Assuming `name` has a `column_title` attribute
            values = request.POST.getlist(f'{column_title}-columns')  # Fetch list of values
            print(values)
            for value in values:
                EntryValue.objects.create(entries_value=value, column=name)
        formset_instance = formset(request.POST)
        if formset_instance.is_valid():
            '''for form in formset_instance:
                print(form)  # Prints the form representation
                print(form.as_table())'''  # Prints the HTML representation of the form
            print(formset.forms)
            formset_instance.save(commit=False)
        return redirect('club:success_record_column')
    else:
        formset_instance = formset(queryset=related_column_names)
        for i, form in enumerate(formset_instance):
            print(f"Form Index: {i}, Name Field: {form.fields.get('name')}")
        context = {'related_column_names': related_column_names, 'formset': formset_instance}
        return render(request, "club/book/edit_book.html", context)



def view_databook(request, id):
    related_column_names = EntryQueue.objects.filter(record_ledgers__id=id)
    combined_data = []
    for entry_queue in related_column_names:
        # Fetching all EntryValue objects related to the current EntryQueue
        books_by_author = entry_queue.entryvaluechild.all()
        combined_data.append({
            'entryQueueName': entry_queue.column_title,  # The name of the EntryQueue
            'values': [value.entries_value for value in books_by_author]  # List of EntryValue values
        })
    # Transpose combined_data so that each row corresponds to a set of values from each EntryQueue
    max_length = max(len(item['values']) for item in combined_data)
    transposed_data = []
    for i in range(max_length):
        row = []
        for item in combined_data:
            row.append(item['values'][i] if i < len(item['values']) else None)
        transposed_data.append(row)
    context = {
        'combined_data': transposed_data,  # Transposed data to match the table format
        'related_column_names': related_column_names , # Column titles (EntryQueue names)
        "id":id,
    }
    # 5. Render the template with the context
    return render(request, "club/book/view-book.html", context)



def success_record_col(request):
    last_record = RecordLedgers.objects.latest('created_at') 
    return render(request, 'club/success.html', {'last_record': last_record})


def club_dashboard(request):
    query_record_ledagers =  RecordLedgers.objects.all()
    context = {"created_book_records":query_record_ledagers,}
    return render(request, "club/club_dashboard.html", context)