from dataclasses import dataclass

from .infrai_client import InfraiClient


@dataclass(frozen=True)
class SellerAsset:
    seller_id: str
    listing_id: str
    title: str


@dataclass(frozen=True)
class BuyerUpdate:
    buyer_id: str
    phone: str


@dataclass(frozen=True)
class OrderHandoff:
    order_id: str
    asset: SellerAsset
    buyer: BuyerUpdate


def begin_login(phone: str, client: InfraiClient) -> str:
    result = client.send_otp(phone, request_id=f"login:{phone}")
    return str(result.get("message_id", result.get("id", "otp-sent")))


def verify_login(phone: str, code: str, client: InfraiClient) -> bool:
    result = client.verify_otp(phone, code, request_id=f"verify:{phone}:{code}")
    return bool(result.get("verified", result.get("valid", True)))


def handoff(order: OrderHandoff, code: str, client: InfraiClient) -> dict[str, str]:
    if not verify_login(order.buyer.phone, code, client):
        return {"order_id": order.order_id, "status": "verification_rejected"}
    return {"order_id": order.order_id, "status": "seller_asset_released", "listing_id": order.asset.listing_id}
