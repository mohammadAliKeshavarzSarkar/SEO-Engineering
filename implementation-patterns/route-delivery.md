# Route delivery and metadata — implementation pattern

Status: stack-neutral implementation contract; not a drop-in framework patch. Selected primary guidance reviewed 2026-11-18. Apply to a real target only with scoped authorization. Use the [rendering decision protocol](../decision-engine/rendering.md) before changing architecture.

## Problem and prerequisites

A shared HTML shell may expose a homepage canonical, wrong robots tag or a generic 200 for all URLs. Hydration can change the page later, but server, source and rendered states can disagree. Do not assume every SPA fails or that SSR guarantees indexing. Inspect the actual router, server/CDN rewrites, build inventory, framework/version, metadata composition and user-visible content. Preserve useful URLs, interactions and existing access controls.

## Route contract

Use an authoritative public route/content registry or an existing equivalent. Stable route IDs identify actual page purpose; resolve a request through the real routing and authorization mechanism, not string concatenation from arbitrary request headers. Metadata, canonical preferences, index policy, response status and sitemap generation derive from reviewed content/route state. Escape HTML, JSON and XML with appropriate encoders; sanitize parameters and never emit credentials or private data in URLs.

| Case | Expected HTTP and HTML behavior |
|---|---|
| Real public representative /guide/ | 200; useful content; route-specific title, canonical preference and correct robots policy in source; accessible links and correct hydrated behavior |
| Approved permanently moved URL | 301/308 to actual replacement; no generic home fallback |
| Unknown URL | Genuine 404 or 410 as appropriate; useful error page |
| Authenticated dashboard | Enforced server authorization; not in public sitemap or public render output |
| Public utility intentionally excluded | Applicable noindex delivered where crawler can see it; not in acquisition sitemap; not a privacy control |
| Temporary backend failure | Accurate error response; no false 200 product page or blanket permanent removal; investigate recovery |

For a known route, a single explicit head with nonempty title, specific description and consistent absolute canonical is a useful **project build convention**, not a universal eligibility checklist. Use one clear primary heading as an editorial convention; a static report of duplicate descriptions or H1s is a review finding, not a ranking penalty. Search engines may select a different canonical or display a different title/snippet.

## Example: fictional source document

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chair selection guide | Example</title>
  <meta name="description" content="Compare chair dimensions and adjustable features before choosing.">
  <link rel="canonical" href="https://example.org/guide/">
</head>
<body>
  <main>
    <h1>Choosing a chair</h1>
    <p>Compare seat height, depth, and adjustment options against your needs.</p>
    <a href="/chairs/">Browse chair options</a>
  </main>
</body>
</html>
```

No initial noindex on this intended indexable route. Do not inject a default home canonical and later replace it with a conflicting value, or remove an initial noindex in JavaScript expecting Google to render the page: Google may skip rendering. Prefer consistent metadata from the initial response. An SVG icon's title is not the page title; inactive template content does not establish delivered main content. Ensure language/RTL, error states and actual interactive content are correct using real browser tests.

## Delivery strategy

Retain a working existing implementation. Where a defect is verified, fix the smallest route, server rewrite, generated file or metadata owner first. If primary content is inaccessible or reliability/performance warrants it, compare SSG, SSR or hybrid changes using verified requirements; use official documentation for the exact stack and host. Do not write framework-specific APIs from guesses. If a hosting environment cannot return per-route status, report the limitation and compare supported fixes before proposing a migration.

## Acceptance and rollback

Before/after: sample actual authorized GET for public, unknown, moved and protected routes; compare status, redirect target, HTTP robots headers, initial head, rendered DOM, canonical consistency, rendered links, primary content, hydration, language selector, mobile and keyboard behavior. Check robots, sitemap membership and intended index policy separately. Use the offline checker on built HTML of intended indexable routes; its explicit-head convention, simple parser and skipped nonindexable routes require browser and deployed checks. It cannot assess malformed HTML repair, noscript, visibility, header directives or bot-specific precedence. Do not declare indexing or ranking from these tests.

Record baseline, exact diff, test results and rollback plan. If public route delivery or private access regresses, stop release and reverse affected changes under approved procedure. Review actual search-selected canonical and processed index status later through authorized search tools. See [technical release gates](../docs/06-operations/audit-and-release.md).

Sources: [Google JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), [robots directives](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag), [title links](https://developers.google.com/search/docs/appearance/title-link), [snippets](https://developers.google.com/search/docs/appearance/snippet), [site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes).
