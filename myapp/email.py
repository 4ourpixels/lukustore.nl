from django.core.mail import EmailMessage
import os
from django.conf import settings


def send_email_with_inline_logo(email, first_name, ticket_number):
    subject = 'Your Spectra Talks with Luku Store.nl & WhoWhatWhereKE Confirmation 🎉'
    message = f"Hi {first_name},\n\nGreat news! You're officially registered for the Spectra Talks with Luku Store.nl & WhoWhatWhereKE 🎶\n\n📅 Date: 05th Jan 2024\n🕒 Time: 3:00 PM - 12:00 AM\n📍 Venue: To be confirmed\n\n\nYour Ticket: {ticket_number}\n\nGet ready for an industry panel talk engaging the various stakeholders in the fashion and music industry!\n\nThis panel follows our most recent partnership Spectra, a community building gathering that seamlessly intertwined locally produced music and art.\nSee you there,\n\nLuku Store.nl & WhoWhatWhereKE\ninfo@lukustore.nl"
    from_email = settings.EMAIL_HOST_USER
    cc_email = settings.EMAIL_HOST_CC
    recipient_list = [email, cc_email]

    # Create an EmailMessage instance
    email_message = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
    )

    # Attach the logo inline
    logo_path = os.path.join(os.path.dirname(
        __file__), 'static/Spectra-Talks-with-Luku-Store-nl-and-WhoWhatWhereKE.jpg')
    with open(logo_path, 'rb') as logo_file:
        # Adjust content type if needed
        email_message.attach(logo_file.name, logo_file.read(), 'image/png')

    # Send the email
    email_message.send()
