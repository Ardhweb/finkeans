from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import modelformset_factory, formset_factory,inlineformset_factory
from .forms import LedagerForm, EntryQueueForm,EntryValueForm
from .models import RecordLedgers, EntryQueue, EntryValue


def create_new_record(request):
    if request.method == 'POST':
        # Handle the Ledager form
        ledager_form = LedagerForm(request.POST)
        
        # Handle the formset for EntryQueue using modelformset_factory
        total_forms = int(request.POST.get('column_head_form-TOTAL_FORMS', 0))
        
        # Create the EntryQueue formset with 'extra' as total_forms (if any)
        EntryQueueFormSet = modelformset_factory(EntryQueue, form=EntryQueueForm, extra=total_forms)
        
        # Initialize the formset with POST data and prefix for EntryQueue
        column_head_formset = EntryQueueFormSet(request.POST, prefix='column_head_form')
        print("Formset is valid:", column_head_formset.is_valid())
        for idx, form in enumerate(column_head_formset):
            print(f"Form {idx} is valid: {form.is_valid()}")
            if not form.is_valid():
                print(f"Form {idx} errors: {form.errors}")
        # Now check if both the Ledager form and the EntryQueue formset are valid
        if ledager_form.is_valid() and column_head_formset.is_valid():
            # Save the Ledager form
            ledager_instance = ledager_form.save()
            print('Formset:', column_head_formset)

            # Save each valid form in the EntryQueue formset
            for form in column_head_formset:
                print('Form:',form)
                if form.is_valid():  # Only save valid forms
                    entry_queue_instance = form.save(commit=False)
                    entry_queue_instance.record_ledgers = ledager_instance  # Link the EntryQueue to the RecordLedgers
                    entry_queue_instance.save()
            return redirect('club:success_record_column')  # Redirect to success page after saving
        else:
            # Debugging: Print the errors in case of validation failure
            print("Ledager form errors:", ledager_form.errors)
            for form in column_head_formset:
                print("EntryQueue form errors:", form.errors)

            return HttpResponse("Error: Form validation failed. Check the console for details.")

    else:
        # Initialize the Ledager form
        ledager_form = LedagerForm()

        # Create the EntryQueue formset with no extra forms initially
        EntryQueueFormSet = modelformset_factory(EntryQueue, form=EntryQueueForm, extra=0)
        
        # Initialize the formset with an empty queryset (no existing EntryQueue instances)
        column_head_formset = EntryQueueFormSet(queryset=EntryQueue.objects.none(), prefix='column_head_form')

        return render(request, 'club/create_ledager.html', {
            'ledager_form': ledager_form,
            'column_head_formset': column_head_formset,
        })
from django.forms import modelformset_factory
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import EntryQueue
from .forms import EntryQueueForm  # Adjust if necessary

def build_new_formset(formset, total):
    """
    Returns the HTML for a new form in the formset with the correct prefix for dynamic forms.
    """
    html = ""
    
    # Loop over the formset's forms
    for form in formset.forms:
        # Replace the `__prefix__` placeholder with the actual new index
        form_html = str(form).replace('__prefix__', str(total))
        html += form_html

    return mark_safe(html)


def add_column_head_form(request):
    """
    Returns the HTML for a new EntryQueue form (for the column head) to be added via HTMX.
    """
    # Get the current total number of forms already in the formset (from the request or session)
    total_forms = int(request.POST.get('column_head_form-TOTAL_FORMS', 0))

    # Increment the total forms count
    total_forms += 1

    # Create the EntryQueue formset class with no initial data (empty formset)
    EntryQueueFormSet = modelformset_factory(EntryQueue, form=EntryQueueForm)

    # Initialize the formset with the correct number of forms (empty queryset)
    column_head_formset = EntryQueueFormSet(queryset=EntryQueue.objects.none(), prefix='column_head_form')

    # Build the form HTML
    total_formset = build_new_formset(column_head_formset, total_forms)

    # Optionally pass specific forms if needed (e.g., the 3rd form)
    head_set = column_head_formset.forms[2] if len(column_head_formset.forms) > 2 else None

    # Return the form HTML for the new form
    return render(request, 'club/partial_column_head_form.html', {
        'column_head_formset': total_formset,
        'total_forms': total_forms,
        'index_set': str(total_forms),
        'head_set': head_set
    })







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