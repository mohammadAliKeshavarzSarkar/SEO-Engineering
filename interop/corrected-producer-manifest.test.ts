/** Synthetic cross-repo contract bridge. Never performs collection or authorizes a crawl. */
import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { parseEvidenceJson } from "@website-bot-scroll/evidence-contract";
import { createExchangeManifest } from "../src/exchange-manifest.js";
import { serializeEvidence } from "../src/serialize.js";
import { preflightExchangeBytes } from "../src/exchange-profile.js";
import { verifyExchangePair } from "../src/verify-exchange.js";

describe("corrected producer manifest -> independent Python consumer bridge", () => {
  it("writes one exact-byte synthetic pair with the actual producer serializer and verifier", async () => {
    const fixture = process.env.WBS_CORRECTED_SOURCE_FIXTURE;
    const output = process.env.WBS_CORRECTED_EXCHANGE_DIR;
    const commit = process.env.WBS_CORRECTED_COMMIT;
    if (!fixture || !output || !commit || !/^[0-9a-f]{40}$/.test(commit)) throw Error("required synthetic bridge inputs absent");
    const document = JSON.parse(await readFile(fixture, "utf8"));
    // The authoritative fixture is historical; only its declared synthetic
    // producer implementation revision changes. No fake collection is inferred.
    document.producer.version = commit;
    const evidence = serializeEvidence(document);
    expect(parseEvidenceJson(Buffer.from(evidence).toString("utf8")).valid).toBe(true);
    expect(preflightExchangeBytes(evidence).eligible).toBe(true);
    const evidenceFilename = "corrected-producer.synthetic.evidence.json";
    const manifestFilename = "corrected-producer.synthetic.manifest.json";
    const manifest = createExchangeManifest({
      evidenceBytes: evidence, evidenceFilename, producerCommit: commit,
      runId: document.run.id, authorizationRef: "synthetic-fixture-only",
      authorizedScope: document.run.scope, startedAt: document.run.started_at,
      finishedAt: document.run.finished_at, coverageLimitations: document.run.limitations
    });
    expect(Object.keys(manifest)).toEqual([
      "contract", "exchange_profile", "contract_source_commit", "producer_commit",
      "schema_sha256", "evidence_sha256", "checksum_algorithm", "evidence_filename",
      "evidence_bytes", "run_id", "authorization_ref", "authorized_scope",
      "started_at", "finished_at", "coverage_limitations",
      "producer_validation", "producer_preflight"
    ]);
    expect(manifest.contract).toEqual({ name: "seo-crawl-evidence", version: "0.1.0" });
    expect(manifest.evidence_sha256).toBe(createHash("sha256").update(evidence).digest("hex"));
    await mkdir(output, { recursive: true });
    const evidencePath = join(output, evidenceFilename);
    const manifestPath = join(output, manifestFilename);
    // One-time synthetic CI paths only. Never rewrite a real exchange.
    await writeFile(evidencePath, evidence, { flag: "wx" });
    await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + "\n", { flag: "wx" });
    const producerResult = await verifyExchangePair({
      evidencePath, manifestPath, expectedAuthorizationRef: "synthetic-fixture-only"
    });
    expect(producerResult.evidenceSha256).toBe(manifest.evidence_sha256);
  });
});
