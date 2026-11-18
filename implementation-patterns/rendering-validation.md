# JavaScript rendering repair and validation patterns

Use [T02](../docs/03-technical/t02-javascript-rendering.md) and [T01](../docs/03-technical/t01-architecture-detection.md). These are stack-neutral patterns and an illustrative local browser test, not tested framework deployments. No browser dependency is bundled.

## Pattern A — preserve semantic navigation while enhancing it

Fictional before (navigation depends on JS):
```html
<button type="button" onclick="goToCatalog()">Browse catalog</button>
```
For a destination rather than an action, render:
```html
<a href="/catalog/">Browse catalog</a>
```
The application may progressively enhance ordinary same-origin navigation, preserving real href, keyboard activation, modifier keys, new tabs, back/forward and direct/reload behavior. Use the project's established router instead of inventing a global click handler. Keep actual action buttons as buttons. The destination must implement its own correct response status and content. Verify actual anchors in source or ready DOM and direct navigation. A link alone is not proof the target is crawlable or indexable.

## Pattern B — route-specific initial content and metadata
If a generic shell contains a wrong canonical or noindex while JS replaces it, fix metadata generation at the real owner (server, generated build, route metadata or edge). Prefer consistent initial and final canonical declarations; if canonical cannot be generated initially, Google allows a single JS-added canonical without conflicting initial declaration. Do not rely on removing initial noindex. Preserve intended access/exclusions. If source shows useful text but DOM replaces it with a loader, use matched initial data and client state to retain real content until a successful refresh; show honest error or stale-state UI as applicable. Do not hide a failed data fetch behind a synthetic 200 product page. Use route-specific error/empty states. Test actual direct GET and client route transitions, hydration and useful interactions; don't claim indexation.

## Pattern C — readiness-aware browser acceptance
Only run against a verified authorized synthetic local app with a permitted isolated browser, no sensitive session, and restricted network (including subresources, redirects and DNS); use an existing configured test environment, not this skill as a network runner. This illustrative Playwright Test case expects a fictional app under http://127.0.0.1:4173/ with an instrumented readiness marker that represents data processing completion independently of the required-content assertion. Exact selectors and status expectations come from the project's reviewed contract. Check installed Playwright version. The code is an example, not an executed test. Retain evidence privately; redact URLs/logs and never expose full response bytes by default.

```ts
import { test, expect } from '@playwright/test';

test('guide has consistent public delivery', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:4173/guide/', {
    waitUntil: 'domcontentloaded', timeout: 10000,
  });
  expect(response).not.toBeNull();
  expect(response!.status()).toBe(200);
  expect(page.url()).toBe('http://127.0.0.1:4173/guide/');
  // Capture source from this navigation response before comparing with DOM.
  // In a real harness use bounded collection; parse source inertly and record
  // headers/redirects separately. Never execute response text in a parser.
  // Readiness is distinct from the required content assertion.
  await expect(page.getByTestId('route-state')).toHaveAttribute(
    'data-state', 'ready', { timeout: 10000 },
  );
  await expect(page.getByRole('heading', { name: 'Choosing a chair' })).toBeVisible();
  await expect(page.getByTestId('guide-body')).toContainText('Compare seat height');
  const catalog = page.getByRole('link', { name: 'Browse chair options' });
  await expect(catalog).toHaveAttribute('href', '/chairs/');
  // The fixture's intended canonical is a production URL, not derived
  // from an arbitrary Host header.
  await expect(page.locator('head link[rel="canonical"]')).toHaveCount(1);
  await expect(page.locator('head link[rel="canonical"]')).toHaveAttribute(
    'href', 'https://example.org/guide/',
  );
});
```

This assertion example covers final DOM and direct status only, not actual source extraction, robots applicability, privacy, network isolation, or full target acceptance. A real harness must obtain those independent observations and compare with the local QA utility when appropriate. Use web assertions with bounded time; do not use networkidle as the only readiness criterion. Record failed readiness separately from content assertions; a timeout does not certify absence. Do not scroll/click to manufacture no-interaction evidence. Run interaction tests separately.

Also test: wrong initial noindex preserved as a finding even when DOM removes it; unrelated redirect/missing route status; JS asset or data failure; hydration mismatch; slow completion with bounded timeout; mobile viewport/locale; preserved controls, accessible navigation and protected routes in authorized synthetic access tests. If a regression is credible, stop release, isolate owner and use approved rollback. Sources: [Google JavaScript guidance](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), [crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable), [Playwright page API](https://playwright.dev/docs/api/class-page), [auto-waiting](https://playwright.dev/docs/actionability).
