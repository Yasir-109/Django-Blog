from django.urls import path
from . import views

urlpatterns = [

    path('', views.PaymentView.as_view(), name='payment'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancelled/', views.CancelledView.as_view(), name="cancelled"),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),

    path('subscribe/', views.SubscriptionView.as_view(), name="subscribe"),
    path('create-subscription-session/', views.create_subscription_session, name='create_subscription_session'),

    
    path('create-billing-portal-session/', views.create_billing_portal_session, name='create_billing_portal_session'),
    path('subscription_details/', views.subscription_details, name='subscription_details'),
    path('payment_success/', views.payment_success),
    path('payment_cancelled/', views.payment_cancelled),

    # path('subscription-success/', views.SubscriptionSuccessView.as_view(), name='subscription_success'),
    # path('subscription-cancelled/', views.SubscriptionCancelledView.as_view(), name='subscription_cancelled'),
    # path('subscription-config/', views.subscription_config, name='subscription_config'),
    # path('subscription-webhook/', views.subscription_webhook, name='subscription_webhook'),
]