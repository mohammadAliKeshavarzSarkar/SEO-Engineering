# Use this SEO skill on another project

## Candidate version

Current development version: 0.3.0-dev.5. See [version metadata](distribution-version.json) and the [technical roadmap](../03-technical/technical-roadmap.md). The previous candidate 0.2.0-rc.1 is historical: use its pinned commit 0483ff33d73687adccd11408ec26318c880ceddf, not current main, for the [candidate notes](release-candidate.md) and reproduction. Pin exact source revision for any build. External activation and independent behavioral evaluation remain pending. Review actual archive contents and reuse permissions before sharing.

## Repository mode

Clone or otherwise grant the agent read access to the complete SEO Engineering library, ideally pinned to a reviewed commit. Open the new website separately and provide exact authorized target and task. Read the master file at skills/seo-engineering/SKILL.md and the linked router. The library and website are different workspaces; never edit the library to store private target data.

## Portable package mode

From a trusted checkout, run (Python 3.10+):
```sh
python3 scripts/build_skill.py --out seo-engineering-0.3.0-dev.5.zip
```
Run `python3 scripts/verify_package.py --archive seo-engineering-0.3.0-dev.5.zip --report seo-engineering-0.3.0-dev.5-receipt.json` against this trusted checkout. See [portable skill acceptance](portable-skill-acceptance.md) for the integrity and new-project acceptance process. Inspect ZIP contents, especially the public documents and scripts, before sharing. Extract the contained seo-engineering folder into the skill location supported by your runtime; for Codex this may be a project .agents/skills directory or user-level skill directory. Other runtimes may require manual loading or a different installation procedure. Do not install two copies with the same skill name unless the runtime's precedence is understood.

The packaged SKILL.md uses references/library as its library root; this is a generated snapshot of allowlisted docs, templates, decision protocols, workflows, patterns, evaluations, examples and selected standalone audit scripts. No projects/, private/, repository history or credentials are intentionally included. The builder is not a content-level secret scanner: review and sanitize allowed resources before release. Rebuild after library updates; record the source commit and archive SHA-256 alongside the distributed archive. Compare two builds in the same pinned Python/zlib runtime for byte reproducibility; inspect the actual archive contents.

## Verify installation

From the full trusted checkout, run `python3 scripts/verify_release.py` and record actual results. Use the [release review](../../templates/skill-release-review.md). A diagnostic pass does not establish external model behavior or privacy review.

- Confirm the runtime recognizes seo-engineering, or explicitly load its SKILL.md.
- Ask for a read-only audit of a synthetic or authorized project; require relevant reference paths, evidence, scope and limitations.
- Confirm references resolve from the packaged library. Run check_docs.py from references/library/scripts with Python; it checks relative file links, explicit skill routing paths and packaged entry points; it does not check external links, anchors or semantic accuracy.
- Confirm the agent has the necessary tools and permissions for the intended task. Skills do not provide connectors, credentials, scheduled monitoring or automatic execution.
- Evaluate against the cases in evaluations/README.md (relative to the library root); compare model, tools, prompt and source commit. Report results, not assumptions.

For updates, replace the installed package with a reviewed newer version; do not expect remote GitHub edits to synchronize a copied ZIP automatically. Preserve target project evidence separately.

Sources: [OpenAI skill concepts](https://developers.openai.com/plugins/concepts/skills), [OpenAI skill testing guidance](https://developers.openai.com/blog/eval-skills), [installation paths example](https://developers.openai.com/api/reference/cli), checked 2026-11-18. Check the current target runtime's documentation for exact installation paths.
