from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.http.response import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from datetime import datetime
from theblog.models import Profile
from datetime import timedelta
import datetime
# Create your views here.


class PaymentView(TemplateView):
    template_name = 'payment.html'


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


class SubscriptionView(TemplateView):
    template_name = 'subscribe.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/payment'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url +
                '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + '/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1NiDhOF01CkaKFwNStwM8K60',
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
        customer_id = session['customer']
        
        try:
            user_profile = Profile.objects.get(stripe_customer_id=customer_id)
            user_profile.subscription_status = 'active'
            user_profile.subscription_created = datetime.now()
            user_profile.subscription_start_date = datetime.now()
            user_profile.save()
        except Profile.DoesNotExist:
            print("I do not work")  # Handle the case where no user with the given customer ID is found

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        if subscription['status'] == 'canceled':
            customer_id = subscription['customer']
            
            try:
                user_profile = Profile.objects.get(stripe_customer_id=customer_id)
                user_profile.subscription_status = 'canceled'
                user_profile.subscription_cancel_at = datetime.now()
                user_profile.save()
            except Profile.DoesNotExist:
                print("No user profile found for the given customer ID")

    elif event['type'] == 'invoice.payment_failed':
        customer_id = event['data']['object']['customer']
        
        try:
            user_profile = Profile.objects.get(stripe_customer_id=customer_id)
            # Clear relevant fields in the user's profile
            user_profile.subscription_status = 'canceled'
            user_profile.subscription_created = None
            user_profile.subscription_start_date = None
            user_profile.subscription_session_id = None
            user_profile.subscription_price_id = None
            user_profile.stripe_customer_id = None
            user_profile.save()
        except Profile.DoesNotExist:
            print("No user profile found for the given customer ID")

    elif event['type'] == 'checkout.session.async_payment_failed':
        print("Payment was not completed by the user.")
        session = event['data']['object']
        customer_id = session['customer']

        try:
            user_profile = Profile.objects.get(stripe_customer_id=customer_id)
            user_profile.subscription_created = None
            user_profile.subscription_start_date = None
            user_profile.subscription_session_id = None
            user_profile.subscription_price_id = None
            user_profile.save()
        except Profile.DoesNotExist:
            print("Profile not found.")

    return HttpResponse(status=200)


@csrf_exempt
def create_subscription_session(request):
    if request.method == 'POST':
        user = request.user
        # Get the price ID from the frontend (you may need to use the appropriate way to retrieve it)
        price_id = request.POST.get('priceId')
        domain_url = 'http://localhost:8000/payment'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if price_id:
            try:
                customer_id = user.profile.stripe_customer_id

                # If no existing customer, create a new one
                if not customer_id:
                    customer = stripe.Customer.create(
                        email=user.email,
                        name= user.get_full_name()
                        )
                    customer_id = customer.id
                    user.profile.stripe_customer_id = customer_id
                    user.profile.save()

                session = stripe.checkout.Session.create(
                    success_url=domain_url +
                    '/payment_success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + '/payment_cancelled',
                    mode='subscription',
                    payment_method_types=['card'],
                    line_items=[{
                        'price': price_id,
                        'quantity': 1,
                    }],
                    # Add the currency parameter here
                    currency='usd',  # Replace with the appropriate currency code
                    customer=customer_id,  # Use the customer ID
                )

                user.profile.subscription_session_id = session.id
                user.profile.subscription_price_id = price_id
                user.profile.save()

                return redirect(session.url)
            except Exception as e:
                return JsonResponse({'error': {'message': str(e)}})

                

@csrf_exempt
def payment_failed(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get("session_id")

        try:
            # Retrieve user profile based on the session_id
            user_profile = Profile.objects.get(subscription_session_id=session_id)
            # Clear relevant fields in the user's profile
            user_profile.subscription_status = 'canceled'
            user_profile.subscription_created = None
            user_profile.subscription_start_date = None
            user_profile.subscription_session_id = None
            user_profile.subscription_price_id = None
            user_profile.save()

            return JsonResponse({'status': 'success'})
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'Profile not found'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def payment_success(request):
    return render(request, 'payment_success.html')

def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')

# stripe.api_key = 'sk_test_51NiC2KF01CkaKFwNwu1jgX21ji9FyNPSYDzLVMc7mqR2HOE6HdY4DkoMtUinmvG4CjTz5m7Ybby3mOQ3dqKspANM00IKsf5SDl'


def subscription_details(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    subscription_id = 'sub_1234567890'  # Replace with the actual subscription ID

    try:
        user = request.user
        profile = Profile.objects.get(user=user)  # Assuming each user has one profile
        subscription_price_id = profile.subscription_price_id
        stripe_customer_id = profile.stripe_customer_id

        subscription_session_id = profile.subscription_session_id

        checkout_session = stripe.checkout.Session.retrieve(subscription_session_id)
        subscription_id = checkout_session.subscription

        subscription = stripe.Subscription.retrieve(subscription_id)
        current_period_end_unix = subscription.current_period_end

        # Convert Unix timestamp to a datetime object
        current_period_end_datetime = datetime.datetime.fromtimestamp(current_period_end_unix)

        # Format the datetime object as a string
        current_period_end = current_period_end_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Calculate next billing date by adding one second to current_period_end
        next_billing_date_datetime = current_period_end_datetime + datetime.timedelta(seconds=1)

        # Format the next billing date as a string
        next_billing_date = next_billing_date_datetime.strftime('%Y-%m-%d %H:%M:%S')    

        context = {
            'current_period_end': current_period_end,
            'next_billing_date': next_billing_date,
        }
            
        return render(request, 'subscription_details.html', context)
    except stripe.error.StripeError as e:
        # Handle Stripe API errors
        context = {'error_message': str(e)}
        return render(request, 'subscription_error.html', context)

def create_billing_portal_session(request):
    if request.method == 'POST':
        user = request.user
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            customer_id = user.profile.stripe_customer_id  # Assuming you store the Stripe customer ID in the user's profile
            if customer_id:
                session = stripe.billing_portal.Session.create(
                    customer=customer_id,
                    return_url='http://localhost:8000/', 
                )
                return redirect(session.url)
            else:
                return JsonResponse({'error': 'Stripe customer ID missing in user profile.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': {'message': str(e)}}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

# def subscription_config(request):
#     stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#     return JsonResponse(stripe_config, safe=False)
#
# @csrf_exempt
# def subscription_webhook(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
#
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         print("Payment was successful.")
#         session = event['data']['object']  # contains a Stripe Session sub-object
#         paymentIntentId = session["payment_intent"]
#         paymentIntent = stripe.PaymentIntent.retrieve(paymentIntentId)
#         print(paymentIntent)
#         amountPaid = int((float)(paymentIntent["amount"]) * (1/100)) + float('5')
#         print(amountPaid)


