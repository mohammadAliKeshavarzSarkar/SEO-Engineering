# Privacy, consent and analytics QA

Evaluate jurisdiction, platform terms, availability, audience age, data categories, processing and consent with accountable privacy/legal owners. Separate public marketing from authenticated or sensitive areas; session recording should not run on health, personal or restricted surfaces absent explicit suitability approval, and never on websites/apps targeting under-18s where Clarity prohibits use. No names, emails, phone numbers, free-text form inputs, health metrics or secrets in analytics, URLs, tags, recordings or public logs. Sanitize page/referrer URLs; do not rely on masking alone.

Consent Mode communicates choices, not a consent UI or legal basis. Set appropriate defaults before dependent tags, update from valid choices, honor withdrawal and test region-specific behavior. Review basic vs advanced mode with owners. Validate all third-party tags, recordings and storage/network behavior under accept, reject, partial, revisit and withdrawal. Mask sensitive regions conservatively; masking changes aren't retroactive. Limit access and retention, define incident response and avoid sharing raw playback URLs.

## Test matrix

- Fresh load, direct URL, SPA navigation, back/forward: intended page view count only.
- Failed form, server rejection, duplicate retry, accepted request: no lead except verified success, exactly once per accepted lead per contract.
- Consent denied/partial/granted/withdrawn: network and storage behave as approved; no sensitive values.
- External campaign redirects: attribution parameters survive when safe; internal links not tagged.
- Compare GA4 realtime/debug/report and CRM aggregate where permitted, noting delays and consent loss.
- Inspect masked DOM/recording across devices after redesign; stable smart-event selectors.

Document event contract and QA results. Do not claim legal compliance solely because tooling passes. Sources: [Consent Mode](https://developers.google.com/tag-platform/security/concepts/consent-mode), [Clarity masking](https://learn.microsoft.com/clarity/setup-and-installation/clarity-masking), [Clarity FAQ](https://learn.microsoft.com/clarity/faq/).
