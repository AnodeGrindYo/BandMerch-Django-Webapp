from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from listings.models import Band
from listings.models import Listing
from django.shortcuts import render
from listings.forms import ContactUsForm, BandForm, ListingForm
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

def band_list(request):
    bands = Band.objects.all()
    return render(
            request, 
            "listings/band_list.html",
            {"bands": bands}
        )

def band_detail(request, id):
    band = Band.objects.get(id=id)
    return render(
        request,
        'listings/band_detail.html',
        {'band': band}
    )
    
def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Band » et la sauvegarder dans la db
            band = form.save()
            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('band-detail', band.id)

    else:
        form = BandForm()
    return render(
        request,
        'listings/band_create.html',
        {'form': form}
    )

def band_update(request, id):
    band = Band.objects.get(id=id)
    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            # maj du groupe existant depuis la base de données
            form.save()
            # redirection vers la page de détail correspondant au groupe que nous venons de mettre à jour
            return HttpResponseRedirect(reverse('band-detail', kwargs={'id': band.id}))
    else:
        form = BandForm(instance=band)
    return render (
        request,
        'listings/band_update.html',
        {'form': form}
    )

def band_delete(request, id):
    band = Band.objects.get(id=id)
    if request.method == 'POST':
        band.delete()
        return HttpResponseRedirect(reverse('band-list'))
    return render(
        request,
        'listings/band_delete.html',
        {'band': band}
    )

def about(request):
    return render(
        request,
        "listings/about.html"
    )

def listings(request):
    listings = Listing.objects.all()
    return render(
        request,
        "listings/listings.html",
        {"listings" : listings}
    )

def listing_detail(request, id):
    listing = Listing.objects.get(id=id)
    return render(
        request,
        'listings/listing_detail.html',
        {'listing': listing}
    )

def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/listings/')
    else:
        form = ListingForm()
    return render(
            request,
            'listings/listing_create.html',
            {'form': form}
        )

def listing_update(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'listings/{id}/')
    else:
        form = ListingForm(instance=listing)
    return render(
        request,
        'listings/listing_update.html',
        {'form': form}
    )

def listing_delete(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == 'POST':
        listing.delete()
        return HttpResponseRedirect(reverse('listings-list'))
    return render(
        request,
        'listings/listings_delete.html',
        {'listing': listing}
    )

def contact(request):
    form = ContactUsForm()
    # print('La méthode de requête est : ', request.method)
    # print('Les données POST sont : ', request.POST)
    if request.method == 'POST':
        # crée une nouvelle instance du formuylaire et la remplit avec les données POST
        form = ContactUsForm(request.POST)
        
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via Contact Us form',
                message = form.cleaned_data['message'],
                from_email = form.cleaned_data['email'],
                recipient_list=['admin@bandmerch.xyz']
            )
            return redirect('email-sent')
    else:
        # doit être une requête GET, donc crée un formulaire vide
        form = ContactUsForm()
    return render(
        request,
        'listings/contact.html',
        {'form': form}
    )
    
def email_sent(request):
    return render(request, 'listings/email_sent.html')
