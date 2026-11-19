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

## Event ownership and conversion integrity

Map every event to the real business or user action, emitter (browser, GTM, server), trigger identity, required sanitized parameters, consent gate, duplicate/retry policy, responsible owner and acceptance evidence. Inspect existing code, container triggers, enhanced measurement and actual stream configuration before adding tags. One intended route view is a project contract, conditional on approved collection; not every application state update, hash change, modal, hydration or URL replacement is a meaningful new page. Choose and verify a single measurement owner for initial and subsequent views. Google's SPA guidance describes enhanced measurement for History API navigation or custom events where appropriate; with GTM-managed SPA history tracking, disable overlapping GA automatic history tracking. A manual router hook alone does not disable default page-load or history events. Test initial tag configuration, back/forward, same-route query updates, redirects, lazy boundaries, component remounts and consent transitions. In test captures compare page_location, page_title and prior meaningful page_referrer; do not emit sensitive URLs or stale prior-route metadata.

Separate business outcome, recorded analytics event, marked key event and attributed credit. GA4 offers once-per-event and once-per-session key-event counting; changing counting method affects future events only. Neither method establishes application-level idempotency. For an accepted lead, use the backend's approved unique action identity and retry-safe business transaction, with privacy-reviewed delivery state internal to the application. Browser confirmation reload, duplicate callbacks and retries must not create extra business outcomes. Never send a local CRM identity or sensitive payload simply to deduplicate. A network timeout creates uncertain provider receipt; document at-least-once/at-most-once delivery tradeoffs, rather than claim exactly-once ingestion. For purchases GA4 documents transaction_id deduplication; use a nonempty unique transaction ID without customer identifying information. This is purchase-specific behavior, not a generic guarantee for generate_lead or other custom events. Verify actual receipt and counts separately. The default event contract uses accepted backend outcomes, not provider counts, as business truth.

Use documented [SPA measurement](https://developers.google.com/analytics/devguides/collection/ga4/single-page-applications), [key-event counting](https://support.google.com/analytics/answer/13366706), and [purchase deduplication](https://support.google.com/analytics/answer/12313109).

UTMs identify external campaigns. Use controlled lowercase names; preserve safe parameters through redirects. Avoid UTMs internally: GA4 does not automatically start a new session when campaign fields change mid-session, but event-level attribution can be affected. Use internal interaction events instead.

## Attribution scope and reporting reconciliation

Distinguish first-user traffic dimensions, session traffic dimensions and event-scoped attribution dimensions. Google's reporting attribution setting can change attribution of historical and future event-scoped key events and revenue, including fractional credit, without changing user/session-scoped traffic dimensions. The attribution lookback window is a separate setting; its changes apply prospectively and can also affect session attribution. Record model, lookback window, key-event counting method, property/stream, timezone, report dimensions and filters, consent regime, reporting identity, collection revision, extraction time and data freshness before comparisons. Never describe organic attributed key events as unique verified organic customers. Direct visits, non-direct attribution and original acquisition are distinct.

GA4 reports, explorations, Data API and BigQuery export are different reporting surfaces. Exported events do not automatically include reporting-layer modeled/attributed values and may have different filters, delayed collection or export limits. Fresh intraday tables can be incomplete; daily tables may receive late arrivals. Compare equivalent timezones, streams, dimensions, exclusions, identity and finalized windows before interpreting differences. Record sampling, thresholding, high-cardinality aggregation and modeling where applicable. Do not silently substitute raw-export counts for report metrics or join Search Console query records to identifiable visitors.

References: [attribution settings](https://support.google.com/analytics/answer/10597962), [reporting surfaces](https://support.google.com/analytics/answer/13644080), [BigQuery Export](https://support.google.com/analytics/answer/9358801).

Measurement Protocol supplements standard tagging; protect API secrets server-side, use HTTPS and validation endpoints, consent and identity rules, include session/engagement context when required for report behavior. A 2xx response is not evidence of correct ingestion. Verify actual results in appropriate reporting/debug tools and compare known transactions.

Clarity: after privacy and eligibility approval, use recordings, heatmaps, funnels and stable smart events to explain friction, not to infer population rates from anecdotes. Pair qualitative hypotheses with funnel counts. Check consent, masking, access and GA4 linkage/quota before integration; expect totals to differ. Do not install on sites/apps targeting under-18s per Microsoft's FAQ.

Sources: [GA4 events](https://support.google.com/analytics/answer/9267735), [campaign attribution](https://support.google.com/analytics/answer/11242841), [Search Console linking](https://support.google.com/analytics/answer/10737381), [Measurement Protocol](https://developers.google.com/analytics/devguides/collection/protocol/ga4), [Clarity](https://learn.microsoft.com/clarity/), [Clarity FAQ](https://learn.microsoft.com/clarity/faq/).

## Worked measurement reconciliation (fictional)

| Metric | Before | After | Interpretation |
|---|---:|---:|---|
| Search Console clicks | 1,000 | 1,000 | No observed click growth on matched report |
| Recorded organic sessions | 800 | 800 | No observed session growth |
| GA4 generate_lead event count | 40 | 60 | Investigate instrumentation and count semantics |
| Verified accepted leads (same approved cohort) | 40 | 40 | No verified lead growth |

In this synthetic example the 50% event-count increase does not prove SEO or conversion improvement. Review duplicate emitters, changed key-event/counting settings, attribution and consent; verify actual trigger traces and aggregate backend reconciliation. Do not invent a discrepancy's cause from these counts alone. Keep measurement repairs separate from acquisition experiments.
