from src.marketplace_sms import BuyerUpdate, OrderHandoff, SellerAsset, handoff


class FakeClient:
    def verify_otp(self, phone, code, request_id):
        return {"verified": code == "246810"}


def test_verified_buyer_unlocks_seller_asset():
    order = OrderHandoff("o-1", SellerAsset("s-1", "l-1", "Desk"), BuyerUpdate("b-1", "+15550001"))
    assert handoff(order, "246810", FakeClient()) == {"order_id": "o-1", "status": "seller_asset_released", "listing_id": "l-1"}


def test_wrong_code_keeps_asset_held():
    order = OrderHandoff("o-1", SellerAsset("s-1", "l-1", "Desk"), BuyerUpdate("b-1", "+15550001"))
    assert handoff(order, "000000", FakeClient())["status"] == "verification_rejected"
