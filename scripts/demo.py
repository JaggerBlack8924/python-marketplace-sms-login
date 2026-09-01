import os

from src.infrai_client import InfraiClient
from src.marketplace_sms import BuyerUpdate, OrderHandoff, SellerAsset, begin_login, handoff


phone = os.environ.get("DEMO_PHONE")
code = os.environ.get("DEMO_CODE")
if not phone or not code:
    raise SystemExit("set DEMO_PHONE and DEMO_CODE")

client = InfraiClient()
print("otp request:", begin_login(phone, client))
order = OrderHandoff("order-42", SellerAsset("seller-7", "listing-9", "Camera"), BuyerUpdate("buyer-3", phone))
print("handoff:", handoff(order, code, client))
