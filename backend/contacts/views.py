from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Contact
from .forms import ContactForm


@login_required
def contact_list(request):
    query = request.GET.get('q', '')
    contacts = Contact.objects.filter(user=request.user)
    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(email__icontains=query) | Q(phone_number__icontains=query) |
            Q(company__icontains=query)
        )
    return render(request, 'contacts/list.html', {'contacts': contacts, 'query': query})


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    return render(request, 'contacts/detail.html', {'contact': contact})


@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, "Contact ajouté avec succès.")
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Nouveau Contact'})


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact modifié avec succès.")
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Modifier le contact'})


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Contact supprimé.")
        return redirect('contact_list')
    return render(request, 'includes/confirm_delete.html', {
        'object': f"{contact.first_name} {contact.last_name}",
        'type': 'contact',
        'cancel_url': reverse('contact_list')
    })


@login_required
def contact_import(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            contacts_data = data.get('contacts', [])
            count = 0
            
            for item in contacts_data:
                # Basic validation
                name = item.get('name', [])
                tels = item.get('tel', [])
                
                # Navigator.contacts returns arrays for properties
                first_name = name[0] if name else "Inconnu"
                phone_number = tels[0] if tels else None
                
                if phone_number:
                    # Check for duplicates
                    if not Contact.objects.filter(user=request.user, phone_number=phone_number).exists():
                        Contact.objects.create(
                            user=request.user,
                            first_name=first_name,
                            phone_number=phone_number,
                            relationship_type='OTHER'
                        )
                        count += 1
            
            return JsonResponse({'status': 'success', 'count': count})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
