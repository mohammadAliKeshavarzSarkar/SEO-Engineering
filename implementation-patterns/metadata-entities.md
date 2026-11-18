# Metadata and structured data patterns

Use [T08](../docs/03-technical/t08-metadata-structured-data.md). Illustrative patterns, not executed application builds. Verify installed framework, real content and current feature guide first.

## A. One reviewed public record
For an editorial page, maintain separate title, description, visible headline, canonical, localized share fields, actual author, dates, image and evidence references. Generate page and metadata from same reviewed content revision. Do not use a generated description as the source of a product claim. Keep a stable organization identity (e.g. https://example.org/#organization) and article identity (https://example.org/guide/#article); link only where relationship is true. Multiple entities need not be duplicated in every component. Author names and publication dates must be real; use approved fallback or defer if missing. For actual multi-entity graphs use supported vocabulary and appropriate validators.

## B. Typed script data (illustrative TypeScript)
The following narrow helper assumes an existing approved validated public content record. It is not a runtime validator, no extra dependency or full Schema.org type library required. Use the actual framework metadata API for text/attribute escaping and a native script data block for JSON-LD. Never use arbitrary fetched HTML as the payload.

~~~tsx
type ReviewedArticle = {
  canonical: string
  headline: string
  authorName: string
  authorType: 'Person' | 'Organization'
  image: string
  published: string
  language: string
}
function articleData(a: ReviewedArticle) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    '@id': a.canonical + '#article',
    mainEntityOfPage: a.canonical,
    headline: a.headline,
    author: { '@type': a.authorType, name: a.authorName },
    image: a.image,
    datePublished: a.published,
    inLanguage: a.language,
  } as const
}
export function ArticleData({ article }: { article: ReviewedArticle }) {
  const text = JSON.stringify(articleData(article))
    .replace(/</g, '\\u003c')
  return <script type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: text }} />
}
~~~

The helper is intentionally restricted. The input must be validated and reviewed before use. Escaping less-than prevents literal closing-script injection through JSON strings; apply organization security requirements and appropriate sanitizer/serializer, not this pattern to unrelated HTML contexts. Do not weaken CSP. For Python draft, script-context text is already escaped; text/attribute fields still need context-appropriate escaping. Next App Router metadata exports and client-only React metadata differ (T03/T04); verify actual source and full render.

## C. Feature and parity validation
Plan actual feature, source documentation version and real public facts. Check JSON parsing, vocabulary/graph, visible content parity, feature-specific properties and eligibility independently. A valid Schema.org graph may have no supported search feature. Example: article schema represents real editorial content, not a generic sales page; Product price/availability must align with actual displayed purchasable offer; no fake review or FAQ rich-result objective. Multiple images or repeated identical entity IDs may be valid; investigate rather than blindly delete. Use current Rich Results Test and vocabulary validator only with authorized public or synthetic markup. Preserve exact warnings and scope; eligibility not guaranteed display.

~~~sh
python3 scripts/audit_metadata.py --input examples/metadata/sample.json --output metadata-report.json
~~~
Fixture compares reviewed Persian title and article draft against supplied source/render strings. No HTML extraction or actual language detection. Inspect actual source/ready DOM and external tests separately. Verify locale, escaping, metadata ownership, route/cache revisions, visible content, share assets and rollback. No live application changes.
