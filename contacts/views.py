from django.db.models.expressions import F
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
  if request.method == 'POST':
    user_id = request.POST['user_id']
    realtor_email = request.POST['realtor_email']
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    realtor_email = request.POST['realtor_email']

    if request.user.is_authenticated:
      user_id = request.user.id
      has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id).exists()
      if has_contacted:
        messages.error(request, 'You have already submitted an inquiry for this listing')
        return redirect('/listings/'+listing_id)

    contact = Contact(user_id=user_id, listing_id=listing_id, listing=listing, name=name, email=email, phone=phone, message=message)

    contact.save()

    # Send mail
    send_mail (
      'Property Listing Inquiry',
      'There has been an inquiry for ' + listing + '. Sign in to the admin panel for more info',
      'cyfeye@gmail.com',
      [realtor_email, 'cyfeye@gmail.com'],
      fail_silently=False
    )

    messages.success(request, 'Your request has been submitted')

    return redirect('/listings/'+listing_id)