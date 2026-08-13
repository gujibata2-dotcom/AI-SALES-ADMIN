from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import hmac
import json
import os
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from typing import Any, Mapping


@dataclass(frozen=True)
class PaymentEvent:
    event_id: str
    event_type: str
    tenant_id: str
    package_id: str
    paid: bool
    amount_baht: int
    external_reference: str
    raw: Mapping[str, Any]


class PaymentAdapter:
    configured = False
    live = False

    def checkout_url(self, tenant_id: str, package_id: str, success_url: str, cancel_url: str) -> str:
        raise RuntimeError("PAYMENT_NOT_CONNECTED")

    def verify_event(self, payload: bytes, signature: str | None) -> PaymentEvent:
        raise RuntimeError("PAYMENT_NOT_CONNECTED")


class StripePaymentAdapter(PaymentAdapter):
    configured = True
    live = True

    def __init__(self, secret_key: str | None = None, webhook_secret: str | None = None):
        self.secret_key = secret_key or os.getenv("STRIPE_SECRET_KEY")
        self.webhook_secret = webhook_secret or os.getenv("STRIPE_WEBHOOK_SECRET")
        if not self.secret_key or not self.webhook_secret:
            raise RuntimeError("PAYMENT_CONFIGURATION_REQUIRED")

    def checkout_url(self, tenant_id: str, package_id: str, success_url: str, cancel_url: str) -> str:
        if package_id != "STARTER_199":
            raise ValueError("PHASE49_CHECKOUT_ONLY_SUPPORTS_STARTER_199")
        body = urlencode({
            "mode": "subscription",
            "line_items[0][price_data][currency]": "thb",
            "line_items[0][price_data][product_data][name]": "AI Employee Starter",
            "line_items[0][price_data][unit_amount]": "19900",
            "line_items[0][price_data][recurring][interval]": "month",
            "line_items[0][quantity]": "1",
            "client_reference_id": tenant_id,
            "metadata[tenant_id]": tenant_id,
            "metadata[package_id]": package_id,
            "success_url": success_url,
            "cancel_url": cancel_url,
        }).encode()
        req = Request("https://api.stripe.com/v1/checkout/sessions", data=body, method="POST")
        req.add_header("Authorization", f"Bearer {self.secret_key}")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        return str(data["url"])

    def verify_event(self, payload: bytes, signature: str | None) -> PaymentEvent:
        if not signature:
            raise PermissionError("PAYMENT_SIGNATURE_REQUIRED")
        parts = dict(item.split("=", 1) for item in signature.split(",") if "=" in item)
        timestamp, supplied = parts.get("t"), parts.get("v1")
        if not timestamp or not supplied:
            raise PermissionError("INVALID_PAYMENT_SIGNATURE")
        if abs(time.time() - int(timestamp)) > 300:
            raise PermissionError("PAYMENT_SIGNATURE_EXPIRED")
        expected = hmac.new(self.webhook_secret.encode(), f"{timestamp}.{payload.decode()}".encode(), sha256).hexdigest()
        if not hmac.compare_digest(expected, supplied):
            raise PermissionError("INVALID_PAYMENT_SIGNATURE")
        event = json.loads(payload.decode())
        obj = event.get("data", {}).get("object", {})
        metadata = obj.get("metadata", {}) or {}
        tenant_id = metadata.get("tenant_id") or obj.get("client_reference_id")
        if not tenant_id:
            raise ValueError("PAYMENT_EVENT_MISSING_TENANT")
        event_type = str(event.get("type", ""))
        paid = event_type in {"checkout.session.completed", "invoice.paid"} and (obj.get("payment_status") in {None, "paid"} or event_type == "invoice.paid")
        amount = int(obj.get("amount_total") or obj.get("amount_paid") or 19900)
        return PaymentEvent(str(event["id"]), event_type, str(tenant_id), metadata.get("package_id", "STARTER_199"), paid, amount // 100, str(obj.get("id", "")), event)
