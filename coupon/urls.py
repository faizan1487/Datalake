from django.urls import path
from .views import LiveCoupons, CouponUsers


urlpatterns = [
    path("getlivecoupons/", LiveCoupons.as_view(), name='live-coupons'),
    path("coupon-users/", CouponUsers.as_view(), name="coupon-users")
]