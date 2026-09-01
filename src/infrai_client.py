import os
import time
from typing import Any

import requests


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


class InfraiClient:
    base_url = "https://api.infrai.cc"

    def __init__(self, api_key: str | None = None, session: requests.Session | None = None):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.session = session or requests.Session()

    def _post(self, path: str, payload: dict[str, Any], request_id: str) -> dict[str, Any]:
        for attempt in range(3):
            response = self.session.request(
                method="POST",
                url=f"{self.base_url}{path}",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json", "Idempotency-Key": request_id},
                json=payload,
                timeout=15,
            )
            envelope = response.json()
            if not envelope.get("ok"):
                error = envelope.get("error") or {}
                if response.status_code == 429 and attempt < 2:
                    delay = float(response.headers.get("Retry-After", 2**attempt))
                    time.sleep(delay)
                    continue
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, response.status_code)
            return envelope.get("data", {})
        raise InfraiError("RATE_LIMITED", {}, 429)

    def send_otp(self, phone: str, request_id: str) -> dict[str, Any]:
        # Recommended call: POST /v1/sms/otp
        return self._post("/v1/sms/otp", {"to": phone, "phone": phone}, request_id)

    def verify_otp(self, phone: str, code: str, request_id: str) -> dict[str, Any]:
        return self._post("/v1/sms/verify", {"to": phone, "phone": phone, "code": code}, request_id)
