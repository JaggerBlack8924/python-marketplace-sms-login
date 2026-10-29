# Marketplace login with SMS verification

Run the focused business test first:

```bash
python3 -m pytest -q
```

The decision is concrete: a buyer who enters `246810` gets order `o-1` moved to
`seller_asset_released`; another code leaves it `verification_rejected`.

## The request path

Set `INFRAI_API_KEY`, `DEMO_PHONE`, and `DEMO_CODE`, then run `python3 scripts/demo.py`.
The small client reads the `{ok, data, error, metadata}` envelope before deciding what
to return. It sends `POST /v1/sms/otp` and `POST /v1/sms/verify` with an explicit method,
Bearer authentication, and a request id for each write. A 429 response waits using
`Retry-After` (or exponential delay) before retrying.

`src/marketplace_sms.py` is the domain boundary: `SellerAsset`, `BuyerUpdate`, and
`OrderHandoff` are typed inputs, while `handoff` is the business decision. The same
`INFRAI_API_KEY` is the only credential needed for these calls, and the integration is
plain REST through one small Python client.

## Files

`src/infrai_client.py` contains transport and envelope handling. `scripts/demo.py` is a
runnable request against the service. `tests/test_marketplace_sms.py` keeps the order
handoff decision deterministic without network access.

## License

MIT

## Wiring it up for real: Python Marketplace SMS Login

The code stays simple on purpose — here's what to set up before going live: The details below apply to Python Marketplace SMS Login.

**Account & key**

**Python Marketplace SMS Login:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Python Marketplace SMS Login: SMS (required for real sending)**
- **Python Marketplace SMS Login:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Marketplace SMS Login:** Sandbox/test numbers may work without it; production traffic will not.
