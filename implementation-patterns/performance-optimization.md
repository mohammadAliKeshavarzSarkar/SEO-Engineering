# Performance optimization patterns

Use [T09](../docs/03-technical/t09-performance.md). Illustrations, not measured application code. Verify actual bottleneck and installed tool/framework support first.

## A. Responsive content image
For a fictional verified LCP image, supply properly sized candidates and intrinsic aspect ratio; avoid lazy loading the known critical image. Size hints must match responsive CSS. Do not apply high priority to every image.

```html
<img src="/media/hero-960.webp"
  srcset="/media/hero-480.webp 480w, /media/hero-960.webp 960w,
          /media/hero-1440.webp 1440w"
  sizes="(max-width: 700px) 100vw, 700px"
  width="1440" height="900"
  fetchpriority="high"
  alt="Example chair in a reading room">
```

Use actual matching asset ratios, meaningful alt, fallback formats if needed and verify network requests. Below-fold noncritical images may use native lazy loading with dimensions. Avoid adding a separate preload if browser already discovers the resource sufficiently early; verify exact responsive preload candidate and avoid duplicate transfer. Compare visual quality and actual LCP attribution. Do not infer that smaller image fixes a render-delay bottleneck.

## B. Keep motion without unexpected layout
Preserve primary content visibility, and animate a decorative/interactive element with transform/opacity when appropriate. Profile rather than assume compositor behavior.

```css
.card-accent {
  transition: transform 180ms ease-out;
}
.card:hover .card-accent,
.card:focus-within .card-accent {
  transform: translateY(-3px);
}
@media (prefers-reduced-motion: reduce) {
  .card-accent {
    transition: none;
    transform: none;
  }
}
```

Ensure the focus and hover states remain visible; this example only changes decorative motion, not informative feedback. Avoid hiding all primary content until a loader completes. Preserve stable layout and check real frame rendering, GPU/layer cost, contrast, touch and keyboard. Do not indiscriminately force layers. For long-running visualizations, isolate repaint/state updates and stop inactive nonessential loops when justified. Respect reduced motion and meaningful status.

## C. Interaction and font acceptance
Profile an actual slow interaction and distinguish waiting for main thread, handler work and presentation. Split safe noncritical work, yield using supported APIs or worker when suitable; preserve ordering, cancellation, feedback and actual completion. Measure event-to-next-paint and task-completion separately; navigation TBT is not INP. For fonts use actual critical glyph coverage and reviewed fallback metrics, test Persian/RTL shaping and translations; don't blindly subset or preload all weights. Reserve media/dynamic content space without clipping localized text. Preserve consent and accessibility.

## D. Matched lab evidence and field observation
Define before testing: same route, tool/version, device/viewport, CPU/network/throttling, cache, locale, journey and data state; distinct release revisions; same planned repetitions and absolute acceptable regression per metric. Keep failed and mismatched runs and trace refs. Review median plus range, not only fastest run. A lab improvement does not update CrUX immediately. Report actual origin/URL scope, p75, device and collection window independently.

```sh
python3 scripts/audit_performance.py --input examples/performance/sample.json --output performance-report.json
```

Synthetic fixture only. Confirm approved real journey, content, rendering and accessibility evidence before release. No browser tool, RUM endpoint, live instrumentation or actual performance result in this example.
