# GA4, Clarity and conversion engineering

Create a measurement plan before tags. Define questions, event names/parameters, scopes, responsible owners, consent, QA and action. GA4 session acquisition describes current session origin; first-user acquisition describes original acquisition. Link compatible Search Console property/web stream where useful; compare page-group aggregates, not individual searchers. Clicks and sessions differ due to definitions, processing, consent and blockers. Treat direct traffic as unattributed where appropriate, not guaranteed brand demand.

| Event | Trigger | Example parameters |
|---|---|---|
| page_view | Exactly one per intended route view | sanitized page_location/title/referrer |
| select_content | User opens a resource | content_type, content_id |
| demo_form_start | First meaningful form interaction | form_id, page_group |
| form_error | Validation failure | error_category, never input |
| generate_lead | Accepted server-confirmed lead | form_id, page_group |
| contact_click | Actual contact channel selection | method, placement |

Configure key events for meaningful business outcomes. Use GA4 recommended names when semantics fit. Explicitly test SPA history navigation and automatic/enhanced measurement to prevent duplicate page views. Count server-accepted success, not submit clicks. Deduplicate client/server delivery using an application-level event contract. Reconcile aggregate accepted lead counts with CRM where permitted. Never send PII or health data.

UTMs identify external campaigns. Use controlled lowercase names; preserve safe parameters through redirects. Avoid UTMs internally: GA4 does not automatically start a new session when campaign fields change mid-session, but event-level attribution can be affected. Use internal interaction events instead.

Measurement Protocol supplements standard tagging; protect API secrets server-side, use HTTPS and validation endpoints, consent and identity rules, include session/engagement context when required for report behavior. A 2xx response is not evidence of correct ingestion. Verify actual results in appropriate reporting/debug tools and compare known transactions.

Clarity: after privacy and eligibility approval, use recordings, heatmaps, funnels and stable smart events to explain friction, not to infer population rates from anecdotes. Pair qualitative hypotheses with funnel counts. Check consent, masking, access and GA4 linkage/quota before integration; expect totals to differ. Do not install on sites/apps targeting under-18s per Microsoft's FAQ.

Sources: [GA4 events](https://support.google.com/analytics/answer/9267735), [campaign attribution](https://support.google.com/analytics/answer/11242841), [Search Console linking](https://support.google.com/analytics/answer/10737381), [Measurement Protocol](https://developers.google.com/analytics/devguides/collection/protocol/ga4), [Clarity](https://learn.microsoft.com/clarity/), [Clarity FAQ](https://learn.microsoft.com/clarity/faq/).
