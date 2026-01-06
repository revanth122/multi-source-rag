# Integrating NimbusNote Pro with Your Stack

NimbusNote Pro exposes a REST API and outgoing webhooks.

Best practices:
- Always handle HTTP 429 by waiting `retry_after_seconds`.
- Make webhook handlers idempotent and log every event.
- Store note IDs in your own database for cross-linking.
