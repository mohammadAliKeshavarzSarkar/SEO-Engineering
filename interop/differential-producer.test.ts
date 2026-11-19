// Test-only bridge copied into the pinned producer's test folder in CI.
// Does not alter its validator or publish any producer source.
import { readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";
import { isDeepStrictEqual } from "node:util";
import { it, expect } from "vitest";
import { parseEvidenceJson } from "../src/validate.js";

it("records actual producer outcomes on the shared synthetic input bytes", () => {
  const work = process.env.WBS_DIFF_WORK;
  const output = process.env.WBS_DIFF_TS_OUTPUT;
  if (!work || !output) throw new Error("missing differential paths");
  const manifest = JSON.parse(readFileSync(join(work, "manifest.json"), "utf8")) as {
    cases: Array<{id: string; file: string; sha256: string}>;
  };
  const results: Record<string, unknown> = Object.create(null);
  for (const c of manifest.cases) {
    const raw = readFileSync(join(work, c.file));
    const sha256 = createHash("sha256").update(raw).digest("hex");
    expect(sha256).toBe(c.sha256);
    try {
      const value = new TextDecoder("utf-8", {fatal:true}).decode(raw);
      const result = parseEvidenceJson(value);
      if (result.valid) {
        results[c.id] = {sha256, status:"valid", document:result.document,
          preservation:isDeepStrictEqual(result.document, JSON.parse(value))};
      } else {
        results[c.id] = {sha256, status:"invalid", codes:result.errors.map(e=>e.code)};
      }
    } catch {
      // Unexpected producer exception is a distinct outcome, never invalid.
      results[c.id] = {sha256, status:"exception", codes:["producer.exception"]};
    }
  }
  writeFileSync(output, JSON.stringify({node:process.version, results}, null, 2), {flag:"wx"});
});
