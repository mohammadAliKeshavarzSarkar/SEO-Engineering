#!/usr/bin/env python3
"""Optional offline consumer for the accepted WebsiteBotScroll contract.

No network, mutation, schema fallback, issue promotion or evidence collection.
Inputs are local regular files in a trusted, stable workspace.
"""
import argparse
import hashlib
import json
import math
import re
import stat
import sys
from collections import Counter
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urljoin, urlsplit, parse_qsl

PIN = Path(__file__).with_name("websitebotscroll-0.1.0-pin.json")
MAX_BYTES = 16 * 1024 * 1024
MAX_SAFE_INTEGER = 9007199254740991
SENSITIVE = re.compile(r"^(?:x-amz-(?:signature|credential|security-token)|signature|sig|token|access_token|api_?key|auth)$", re.I)
TERMINAL = {"completed", "partial", "failed", "cancelled"}


class BoundaryError(ValueError):
    """Input cannot safely be compared in this consumer; not a canonical verdict."""


class InvalidJson(ValueError):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_local(path, limit=MAX_BYTES):
    path = Path(path)
    if not stat.S_ISREG(path.lstat().st_mode):
        raise BoundaryError("input_not_regular")
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise BoundaryError("input_size_limit")
    return raw


def pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            raise InvalidJson("json.duplicate_key")
        out[key] = value
    return out


def constant(_):
    raise InvalidJson("json.nonfinite")


def check_transport(value):
    stack = [(value, 0)]
    while stack:
        item, depth = stack.pop()
        if depth > 128:
            raise BoundaryError("nesting_limit")
        if isinstance(item, dict):
            stack.extend((k, depth + 1) for k in item)
            stack.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list):
            stack.extend((v, depth + 1) for v in item)
        elif isinstance(item, str):
            try:
                item.encode("utf-8", errors="strict")
            except UnicodeError:
                raise BoundaryError("unpaired_unicode_surrogate") from None
        elif type(item) in (int, float):
            if type(item) is float and not math.isfinite(item):
                raise BoundaryError("numeric_range")
            if abs(item) > MAX_SAFE_INTEGER:
                raise BoundaryError("numeric_range")


def parse(raw):
    if len(raw) > MAX_BYTES:
        raise BoundaryError("input_size_limit")
    try:
        value = json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=pairs,
                           parse_constant=constant)
    except InvalidJson:
        raise
    except (UnicodeError, json.JSONDecodeError):
        raise InvalidJson("json.parse") from None
    except (RecursionError, ValueError):
        raise BoundaryError("parser_limit") from None
    check_transport(value)
    return value


def load_pin():
    return json.loads(PIN.read_text(encoding="utf-8"))


def load_validator(raw, pin):
    if digest(raw) != pin["contract"]["schema_sha256"]:
        raise BoundaryError("schema_checksum_mismatch")
    from jsonschema import Draft202012Validator, FormatChecker
    schema = parse(raw)
    Draft202012Validator.check_schema(schema)
    # Pinned schema has only local refs. Never fetch an external schema.
    checker = FormatChecker()
    if not {"uri", "date-time"} <= checker.checkers.keys():
        raise BoundaryError("format_checker_unavailable")
    return Draft202012Validator(schema, format_checker=checker)


def issue(code, path):
    return {"code": code, "path": path}


def pointer_resolves(root, pointer):
    current = root
    for encoded in pointer[1:].split("/"):
        segment = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", segment):
                return False
            # Avoid integer conversion limits for untrusted, absurd indices.
            if len(segment) > len(str(len(current))) or int(segment) >= len(current):
                return False
            current = current[int(segment)]
        elif isinstance(current, dict) and segment in current:
            current = current[segment]
        else:
            return False
    return True


def earlier_time(left, right):
    # Python datetime lacks RFC3339 leap seconds and nanosecond semantics.
    # Treat unsupported timestamps as a local boundary, not a successful check.
    try:
        return datetime.fromisoformat(left.replace("Z", "+00:00").replace("z", "+00:00")) < datetime.fromisoformat(right.replace("Z", "+00:00").replace("z", "+00:00"))
    except ValueError:
        raise BoundaryError("timestamp_comparison_unsupported") from None


def url_issue(raw, path, unsafe_code="semantic.unsafe_url"):
    # urllib is not a WHATWG URL implementation. Preserve strings exclusively;
    # use a conservative review boundary for ambiguous URL representations.
    if "\\" in raw or any(ord(c) < 32 for c in raw):
        raise BoundaryError("ambiguous_url_representation")
    try:
        url = urlsplit(urljoin("https://evidence.invalid/", raw))
        _ = url.port
        if url.scheme in {"http", "https"} and not url.hostname:
            return issue("semantic.url_parse_error", path)
        if url.username or url.password or any(SENSITIVE.fullmatch(k) for k, _ in parse_qsl(url.query, keep_blank_values=True, max_num_fields=10000)):
            return issue(unsafe_code, path)
    except (ValueError, UnicodeError):
        return issue("semantic.url_parse_error", path)
    return None


def semantic(document):
    errors = []
    def add(code, path):
        errors.append(issue(code, path))
    def url(raw, path, code="semantic.unsafe_url"):
        problem = url_issue(raw, path, code)
        if problem:
            errors.append(problem)
    def unique(entries, noun):
        seen = set()
        for ident, path in entries:
            if ident in seen:
                add("semantic.duplicate_" + noun + "_id", path)
            seen.add(ident)
    run, pages, group = document["run"], document["pages"], document["diagnostics"]
    diagnostics = group["value"] or []
    page_ids = {p["id"] for p in pages}
    unique(((p["id"], f"/pages/{i}/id") for i,p in enumerate(pages)), "page")
    observations, owners, tx_ids, link_ids = [], {}, [], []
    for i,p in enumerate(pages):
        for name,o in p["observations"].items():
            observations.append((o, f"/pages/{i}/observations/{name}"))
            owners[o["id"]] = p["id"]
        for j,t in enumerate((p["observations"]["http"]["value"] or {}).get("transactions", [])):
            tx_ids.append((t["id"], f"/pages/{i}/observations/http/value/transactions/{j}/id"))
        for j,l in enumerate(p["observations"]["links"]["value"] or []):
            link_ids.append((l["id"], f"/pages/{i}/observations/links/value/{j}/id"))
    observations.append((group, "/diagnostics"))
    unique(((o["id"], path+"/id") for o,path in observations), "observation")
    unique(tx_ids, "transaction")
    unique(link_ids, "link")
    unique(((d["id"], f"/diagnostics/value/{i}/id") for i,d in enumerate(diagnostics)), "diagnostic")
    unique(((e["id"], f"/errors/{i}/id") for i,e in enumerate(document["errors"])), "error")
    by_id = {o["id"]:o for o,_ in observations}

    finished = run["finished_at"]
    if run["lifecycle"] in TERMINAL and finished is None:
        add("semantic.terminal_finished_at_required", "/run/finished_at")
    if run["lifecycle"] not in TERMINAL and finished is not None:
        add("semantic.nonterminal_finished_at_forbidden", "/run/finished_at")
    if run["lifecycle"] == "partial":
        if run["stop_reason"] is None:
            add("semantic.partial_stop_reason_required", "/run/stop_reason")
        if not run["limitations"]:
            add("semantic.partial_limitation_required", "/run/limitations")
    if finished is not None and earlier_time(finished, run["started_at"]):
        add("semantic.run_time_order_invalid", "/run/finished_at")
    c = run["coverage"]
    if c["collected"] + c["failed"] != c["attempted"]:
        add("semantic.coverage_outcome_mismatch", "/run/coverage")
    if c["attempted"] > c["discovered"]:
        add("semantic.attempted_exceeds_discovered", "/run/coverage/attempted")
    if "unattempted" in c and c["unattempted"] != c["discovered"] - c["attempted"]:
        add("semantic.unattempted_mismatch", "/run/coverage/unattempted")
    if c["collected"] != len(pages):
        add("semantic.page_count_mismatch", "/run/coverage/collected")
    for o,path in observations:
        if o["status"] == "partial" and not o["reasons"]:
            add("semantic.partial_reason_required", path+"/reasons")
        seen = []
        for i,override in enumerate(o.get("field_overrides", [])):
            ptr = override["path"]
            dest = f"{path}/field_overrides/{i}/path"
            if not pointer_resolves(o["value"], ptr):
                add("semantic.field_override_target_missing", dest)
            if ptr in seen:
                add("semantic.duplicate_field_override", dest)
            elif any(ptr.startswith(q+"/") or q.startswith(ptr+"/") for q in seen):
                add("semantic.overlapping_field_override", dest)
            seen.append(ptr)

    def page_ref(obj, field, path):
        if field in obj and obj[field] is not None and obj[field] not in page_ids:
            add("semantic.dangling_page_reference", path+"/"+field)
    def limitations(items, path):
        for i,item in enumerate(items):
            page_ref(item, "page_id", f"{path}/{i}")
    for i,d in enumerate(diagnostics):
        path = f"/diagnostics/value/{i}"
        page_ref(d, "subject_page_id", path)
        allowed = {d["subject_page_id"]}
        if d["evidence_scope"] == "cross_page":
            allowed.update(d["related_page_ids"])
        for j,pid in enumerate(d["related_page_ids"]):
            if pid not in page_ids:
                add("semantic.dangling_page_reference", f"{path}/related_page_ids/{j}")
        for j,oid in enumerate(d["observation_ids"]):
            ref = f"{path}/observation_ids/{j}"
            if oid not in by_id:
                add("semantic.dangling_observation_reference", ref)
            elif d["outcome"] == "pass":
                if by_id[oid]["status"] != "observed":
                    add("semantic.pass_requires_available_evidence", path+"/outcome")
                    add("semantic.pass_requires_observed_page_evidence", path+"/outcome")
                elif oid == group["id"]:
                    add("semantic.pass_requires_observed_page_evidence", path+"/outcome")
            if owners.get(oid) not in allowed:
                add("semantic.diagnostic_evidence_scope_mismatch", ref)
        limitations(d["limitations"], path+"/limitations")
    limitations(run["limitations"], "/run/limitations")
    for i,e in enumerate(document["errors"]):
        path = f"/errors/{i}"
        page_ref(e, "page_id", path)
        if "observation_id" in e and e["observation_id"] not in by_id:
            add("semantic.dangling_observation_reference", path+"/observation_id")

    for i,p in enumerate(pages):
        path = f"/pages/{i}"
        identity, obs = p["url_identity"], p["observations"]
        for key in ("discovered_url","requested_url","normalized_url","final_url"):
            url(identity[key], path+"/url_identity/"+key)
        for j,u in enumerate(identity["canonical_urls"]):
            url(u, f"{path}/url_identity/canonical_urls/{j}")
        for j,u in enumerate((obs["metadata"]["value"] or {}).get("canonical_urls", [])):
            url(u, f"{path}/observations/metadata/value/canonical_urls/{j}")
        for j,l in enumerate(obs["links"]["value"] or []):
            dest = f"{path}/observations/links/value/{j}"
            page_ref(l, "target_page_id", dest)
            url(l["target_url"], dest+"/target_url")
        if obs["rendering"]["value"] is not None:
            url(obs["rendering"]["value"]["rendered_url"], path+"/observations/rendering/value/rendered_url")
        http = obs["http"]["value"]
        if http is None:
            continue
        txs = http["transactions"]
        prefix = path+"/observations/http/value/transactions"
        if txs[0]["request_url"] != identity["requested_url"]:
            add("semantic.initial_request_url_mismatch", prefix+"/0/request_url")
        for j,t in enumerate(txs):
            dest = f"{prefix}/{j}"
            if earlier_time(t["finished_at"], t["started_at"]):
                add("semantic.transaction_time_order_invalid", dest+"/finished_at")
            for key in ("request_url","response_url","redirect_to"):
                if t[key] is not None:
                    url(t[key], dest)
            for k,h in enumerate(t["headers"]):
                for raw in h["values"]:
                    candidates = [raw] if h["name"] == "location" else re.findall(r"<([^>]+)>",raw) if h["name"] == "link" else []
                    for candidate in candidates:
                        url(candidate, f"{dest}/headers/{k}", "semantic.sensitive_header_url")
            if j+1 < len(txs) and t["redirect_to"] != txs[j+1]["request_url"]:
                add("semantic.redirect_discontinuity", dest+"/redirect_to")
        if http["final_transaction_id"] != txs[-1]["id"] or identity["final_url"] != txs[-1]["response_url"]:
            add("semantic.final_url_mismatch", path+"/url_identity/final_url")
    for i,u in enumerate(run["scope"]["seed_urls"]):
        url(u, f"/run/scope/seed_urls/{i}")
    return errors


def validate(raw, validator):
    """Return a sanitized result and untouched parsed document on valid input."""
    try:
        doc = parse(raw)
        errors = []
        # Do not echo validator messages, which may contain private input values.
        for e in validator.iter_errors(doc):
            errors.append(issue("schema."+e.validator, "/"))
            if len(errors) >= 100:
                break
        if not errors:
            errors = semantic(doc)
        if errors:
            return {"status":"invalid","issues":errors[:100]}, None
        return {"status":"valid","issues":[]}, doc
    except InvalidJson as e:
        return {"status":"invalid","issues":[issue(str(e),"/")]},None
    except BoundaryError as e:
        return {"status":"blocked","issues":[issue("consumer."+str(e),"/")]},None
    except RecursionError:
        return {"status":"blocked","issues":[issue("consumer.recursion_limit","/")]},None


def receipt(raw, validator, pin):
    result, doc = validate(raw, validator)
    out = {**result, "method":"websitebotscroll-consumer-dev.1",
           "contract_version":pin["contract"]["version"],
           "schema_sha256":pin["contract"]["schema_sha256"],
           "contract_source_commit":pin["producer_commit"],"input_sha256":digest(raw),
           "input_bytes":len(raw), "python":sys.version.split()[0], "jsonschema":version("jsonschema"),
           "authorization_verified":False,"provenance_verified":False,"actual_exchange_verified":False,
           "strategic_interpretation_performed":False,"deployment_authorized":False}
    if doc is not None:
        counts = Counter(o["status"] for page in doc["pages"] for o in page["observations"].values())
        counts[doc["diagnostics"]["status"]] += 1
        out["summary"] = {"lifecycle":doc["run"]["lifecycle"],"declared_coverage":doc["run"]["coverage"],
                          "observation_status_counts":dict(sorted(counts.items()))}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--schema",type=Path,required=True)
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        pin=load_pin()
        validator=load_validator(read_local(args.schema),pin)
        raw=read_local(args.input)
        report=receipt(raw,validator,pin)
        with args.output.open("x",encoding="utf-8") as stream:
            json.dump(report,stream,indent=2,ensure_ascii=True,allow_nan=False)
            stream.write("\n")
        return {"valid":0,"invalid":2,"blocked":3}[report["status"]]
    except (OSError, ValueError, ImportError, RecursionError):
        print("Consumer setup/input/output failed; no acceptance inferred.",file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
