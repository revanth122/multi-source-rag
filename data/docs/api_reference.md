# NimbusNote Pro API – Reference

Base URL: https://api.nimbusnote.example.com/v1

### Rate limits
- Authenticated requests: 1000 requests per minute per access token
- Unauthenticated requests: 60 requests per minute per IP

If you exceed the limit, the API returns HTTP 429 with a JSON error body that includes a `retry_after_seconds` field.

### Webhooks
NimbusNote Pro sends webhooks at-least-once. Your endpoint must be idempotent.
