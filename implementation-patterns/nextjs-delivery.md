# Next.js delivery and cache validation patterns

Use [T04](../docs/03-technical/t04-nextjs-hybrid.md). Illustrative snippets, not independently compiled or deployed. Check exact Next version, cache mode, host and existing data contract before reuse.

## A. App Router public content and metadata (Next 15+ async params style)
For a fictional finite public article registry, use one reviewed record for page and metadata. Example assumes existing server-side getPublishedArticle(slug) returning only approved public fields, null for known missing; upstream failure throws rather than returns null. Avoid an inherited conflicting homepage canonical.

```tsx
import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { getPublishedArticle } from '@/lib/public-content'

type Props = { params: Promise<{ slug: string }> }
async function article(params: Props['params']) {
  const { slug } = await params
  const post = await getPublishedArticle(slug)
  if (!post) notFound()
  return post
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await article(params)
  return {
    title: post.title,
    description: post.summary,
    alternates: { canonical: post.reviewedCanonicalUrl },
  }
}

export default async function Page({ params }: Props) {
  const post = await article(params)
  return <main>
    <h1>{post.title}</h1>
    <p>{post.body}</p>
  </main>
}
```
This does not configure caching or guarantee one fetch; use the project's version-appropriate memoization/data layer, validated published record and stable revision. No credentials in public record/props. Actual status depends on streaming boundary. Use Server Components for public initial content and client components for controls as appropriate. For static generation add generateStaticParams with concrete published slugs from the same registry; verify mode-specific dynamic path handling and actual build. Do not invent missing slugs.

## B. Keep cache models distinct

| App previous model (version dependent) | Cache Components enabled (Next 16+) | Pages Router |
|---|---|---|
| Existing supported fetch cache/revalidate and route options | use cache / cacheLife / cacheTag for appropriate public data scope | getStaticProps and revalidate or getServerSideProps |
| Check actual route runtime and data caching defaults | Uncached/request-time content and explicit Suspense boundaries as applicable | getStaticPaths for concrete dynamic build paths |
| Version-appropriate revalidatePath/tag APIs | Version-appropriate revalidatePath/tag/updateTag semantics | Authorized on-demand revalidation in supported runtime |

A static export cannot execute runtime regeneration. Never apply one model's settings indiscriminately. Use actual installed-version documentation; preserve safe cache keys and no shared private payload. Revalidation after mutation must be authorized, narrow and observable, including related metadata/sitemap records and CDN/instance behavior. Separate timed expiry, background refresh, errors and client cache. No blind cache purge code.

## C. Synthetic freshness acceptance
Define reviewed content revision v2 due at 10:05 UTC in isolated synthetic site. Observe v1 before deadline, v1 at/after deadline, v2 after later request; each sample with correct route/locale/build/profile, timestamp and node if known. The first is not a breach, second is review, third is target observed for that sample only. If the target changes, update the project assertion and scope. Never use ETag, cache HIT or a timestamp alone as actual content revision without validated mapping. Timeout/failed request or different locale is deferred. Run the offline fixture:

```sh
python3 scripts/audit_next_delivery.py --input examples/next-delivery/sample.json --output next-delivery-report.json
```

Actual verification must use an approved runtime/build and aligned response, full stream and browser observations (T02); cross-instance/cache tests require explicit scope. Test new/deleted content, failure, true status, metadata, sitemap/robots, locale and security before release. No global cache purge or production mutation in this example. See T04 sources for exact APIs.
