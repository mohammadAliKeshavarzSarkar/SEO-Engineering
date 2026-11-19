# Privacy, consent and analytics QA

Evaluate jurisdiction, platform terms, availability, audience age, data categories, processing and consent with accountable privacy/legal owners. Separate public marketing from authenticated or sensitive areas; session recording should not run on health, personal or restricted surfaces absent explicit suitability approval, and never on websites/apps targeting under-18s where Clarity prohibits use. No names, emails, phone numbers, free-text form inputs, health metrics or secrets in analytics, URLs, tags, recordings or public logs. Sanitize page/referrer URLs; do not rely on masking alone.

Consent Mode communicates choices, not a consent UI or legal basis. Set appropriate defaults before dependent tags, update from valid choices, honor withdrawal and test region-specific behavior. Review basic vs advanced mode with owners. Validate all third-party tags, recordings and storage/network behavior under accept, reject, partial, revisit and withdrawal. Mask sensitive regions conservatively; masking changes aren't retroactive. Limit access and retention, define incident response and avoid sharing raw playback URLs.

## Consent-state contract

Google documents two modes: basic mode prevents supported Google tag transmission before consent and on denial; advanced mode can send limited measurements without cookies under denied storage settings. Cookieless is not equivalent to no transmission, anonymous, or lawful. Select modes with accountable owners based on actual legal basis, platform terms, audience and data scope; do not select advanced by default for modeling benefit. Explicitly map analytics_storage, ad_storage, ad_user_data and ad_personalization independently to actual choices; other consent types may be relevant. Test defaults before tag execution, consent update before route changes, persisted settings, region precedence, revocation and non-Google/custom tags. Do not rely on a UI checkbox, built-in checks alone or a GTM preview to infer actual network/storage behavior. Review any URL passthrough, click identifiers and redaction separately; never enable by default on sensitive routes. Do not use server-side collection or Measurement Protocol to bypass a denied or unknown permission state. Do not resend historical declined events when consent changes without separately approved policy.

Clarity documents consent-signal enforcement for visits originating in EEA, UK and Switzerland beginning October 31, 2025. ConsentV2 is the recommended API; distinguish ad and analytics consent states. Denied consent can still allow limited no-cookie tracking; where no recording or transmission is allowed, block initialization and verify actual behavior rather than assume a denied cookie state stops collection. Review current supported regions and actual CMP interaction. Masking changes apply to future recordings and are not retroactive; DOM masking does not establish that URLs, custom metadata, third-party scripts or other collection paths are safe. Keep health/personal surfaces out of recording by default. Maintain the existing prohibition on deploying Clarity to sites/apps targeting under-18s. A synthetic test, cookie absence or masked playback is not a legal compliance determination.

References (2026-11-19): [Google consent mode](https://developers.google.com/tag-platform/security/concepts/consent-mode), [consent implementation](https://developers.google.com/tag-platform/security/guides/consent), [Clarity ConsentV2](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-consent-api-v2), [Clarity masking](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-masking).

## Test matrix

- Fresh load, direct URL, SPA navigation, back/forward: intended page view count only.
- Failed form, server rejection, duplicate retry, accepted request: no lead except verified success, exactly once per accepted lead per contract.
- Consent denied/partial/granted/withdrawn: network and storage behave as approved; no sensitive values.
- External campaign redirects: attribution parameters survive when safe; internal links not tagged.
- Compare GA4 realtime/debug/report and CRM aggregate where permitted, noting delays and consent loss.
- Inspect masked DOM/recording across devices after redesign; stable smart-event selectors.

Document event contract and QA results. Do not claim legal compliance solely because tooling passes. Sources: [Consent Mode](https://developers.google.com/tag-platform/security/concepts/consent-mode), [Clarity masking](https://learn.microsoft.com/clarity/setup-and-installation/clarity-masking), [Clarity FAQ](https://learn.microsoft.com/clarity/faq/).

## Expanded evidence checklist

For each approved synthetic scenario record expected event and collection permit, runtime/version, route and tag owner, consent state, observed network and storage behavior, sanitized event names/counts, test timestamp, report reconciliation and result (pass/fail/blocked). Test multiple active emitters, purchase retry with same transaction vs two distinct orders, lead server rejection vs verified acceptance, unavailable provider, tag delay, browser back/forward and revocation. Use test properties or approved isolated debug traffic; no live customer payloads, no false lead or purchase submissions, no public debug exports. Explicitly distinguish expected no collection from unobserved collection. Remove sensitive values before preserving evidence; if exposure is suspected, stop collection/distribution within authorization and escalate privately.
