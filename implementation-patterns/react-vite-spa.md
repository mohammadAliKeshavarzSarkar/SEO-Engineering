# React, Vite and SPA route delivery patterns

Use [T03](../docs/03-technical/t03-react-vite-spa.md), [T02](../docs/03-technical/t02-javascript-rendering.md) and the [SPA decision protocol](../decision-engine/spa-delivery.md). Examples are illustrative, not a tested React/Vite deployment. Respect exact installed versions, router mode and hosting configuration, and preserve useful UI.

## A. Plain client-side application: preserve router and URLs
For a recognized public destination, use the existing router's link component that emits an actual href, or ordinary anchors. Direct entry and refresh require a host that can serve the appropriate document; a wildcard error component only handles client UI, not the HTTP response. Maintain actual route selection, error and loading states. If primary content depends on JavaScript, apply T02 before deciding to prerender. A client-only app can use appropriate route metadata, but this is not equivalent to initial metadata.

React 19 example for a public route whose intended canonical was reviewed. Use only if the project uses React 19 and no competing head manager. Remove or reconcile conflicting static shell defaults and layout declarations; older versions require their own supported mechanism.
```tsx
export function GuideHead() {
  return <>
    <title>Chair selection guide | Example</title>
    <meta name="description" content="Compare chair dimensions and fit." />
    <link rel="canonical" href="https://example.org/guide/" />
  </>;
}
```
Metadata generated in client execution is not proof the initial response has it. Check actual source/rendered head on direct and in-app navigation. Never set canonical from untrusted Host or arbitrary location parameters. A root shared shell must not carry route-specific homepage canonical for every child.

## B. Selective prerender with React Router Framework Mode
Only if the project actually uses a compatible Framework Mode version. Current docs expose prerender in react-router.config.ts; this is not plain vite.config.ts or a drop-in BrowserRouter feature. Sample config with reviewed concrete public paths:
```ts
import type { Config } from "@react-router/dev/config";
export default {
  ssr: false,
  prerender: ["/", "/guide", "/blog/first-post"],
} satisfies Config;
```
Enumerate dynamic/locale paths from approved published registry at build time, not route placeholders or all combinations. Build loaders must not serialize credentials or private data to artifacts. No runtime SSR server in this configuration; compatible client loaders and build-time data constraints must be reviewed. In the reviewed Framework Mode version (8.5.2), prerendering / produces a separate __spa-fallback.html for other routes; without root prerender, index.html serves as the fallback. Verify real output before deploying. Do not use the prerendered homepage as the fallback for other valid paths. For a prerendered parent with a loader, cover all child paths or provide a supported clientLoader for paths rendered at runtime. Verify host status and resource routing separately. For a runtime SSR deployment the configuration and requirements differ; do not set ssr false globally if app depends on server features.

## C. Deployment routing and base
For a fictional subpath /learn/, Vite base may be "/learn/" for generated asset paths, while the router basename and actual host URL mapping must separately align. The canonical registry uses the reviewed production origin and actual public URL, not a filesystem path or staging base. Compare actual build settings and host behavior for trailing slash, direct nested routes, data/asset URLs and missing routes. Use host-specific documented configuration; no generic wildcard rewrite copied blindly.

Illustrative target request matrix (not executable host configuration):

| Requested path | Target outcome |
|---|---|
| /learn/guide/ | intended static or runtime document, 200 |
| /learn/assets/actual-chunk.js | correct JS resource; no document rewrite |
| /learn/assets/missing.js | 404, not HTML shell 200 |
| /learn/api/example | intended API response or genuine API error |
| /learn/old-guide/ | approved permanent redirect to real replacement |
| /learn/app/ | approved shell or server-authenticated route; data protected |
| /learn/unknown/ | genuine missing status and useful UI where supported |

If host cannot distinguish unknown route from valid SPA paths, evaluate narrow fallback, a real server 404 destination, or rendered noindex on known error pages per Google guidance; these are not equivalent HTTP behaviors. Maintain distinct real missing vs temporary error states. Do not use a client wildcard component to claim status changed. Use local preview only as build smoke, verify deployment separately.

## D. Acceptance: route registry to build to actual response
Use explicit local artifact plan and run:
```sh
python3 scripts/audit_spa_build.py --input examples/spa-build/sample.json --root examples/spa-build/artifacts --output spa-build-report.json
```
This hand-authored fixture exercises missing artifact, shared shell and runtime branches. For a real authorized build, use exact selected root and paths, then local HTML checker for applicable per-route documents and T02 matched observations. Test content and head, direct routes, asset/content-type responses, readiness, navigation, refresh, redirects and genuine errors, mobile/locale interactions, and authorized access constraints. Acceptance includes real host behavior and public build content review; a present file or successful offline test does not prove deployment, accessibility, indexing or protected-data safety. Review cache invalidation, rollback and preserve URL continuity. References in [T03](../docs/03-technical/t03-react-vite-spa.md).
