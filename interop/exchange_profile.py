"""Agreed first-exchange restrictions, separate from canonical validation.

This is a local preflight, not a new WebsiteBotScroll schema or an acceptance
decision. No normalization, network access, producer verification or file edits.
"""
import json
import re
from rfc3339_validator import validate_rfc3339

from interop.validate_crawl_evidence import (
    BoundaryError, InvalidJson, constant, pairs, parse, validate, digest,
)

PROFILE_ID = "seo-crawl-evidence-exchange-profile/0.1.0"
PROFILE_AGREEMENT = "accepted_for_bounded_synthetic_exchange"
TIMESTAMP_FIELDS = {"started_at", "finished_at", "collected_at", "occurred_at"}
URL_FIELDS = {"discovered_url", "requested_url", "normalized_url", "final_url",
              "rendered_url", "request_url", "response_url", "redirect_to", "target_url"}
URL_ARRAY_FIELDS = {"seed_urls", "canonical_urls"}
SUBSECOND = re.compile(r":[0-9]{2}\.([0-9]+)")
LEAP_SECOND = re.compile(r"[Tt][0-9]{2}:[0-9]{2}:60(?:[.Zz+-])")


def profile(raw):
    """Measure conservative representation restrictions without a canonical verdict."""
    reasons = set()
    if raw.startswith(b"\xef\xbb\xbf"):
        return {"status":"outside_profile","reasons":["utf8_bom_forbidden"]}
    try:
        doc = parse(raw)
    except InvalidJson:
        return {"status": "not_assessed", "reasons": ["malformed_json"]}
    except BoundaryError as e:
        return {"status": "outside_profile", "reasons": [str(e)]}

    # All numeric fields in the pinned schema are integers. Reject decimal and
    # exponent spellings rather than trusting binary floating-point coercion.
    def decimal_token(token):
        reasons.add("non_integer_number_spelling")
        return None
    def integer_token(token):
        if token == "-0":
            reasons.add("negative_zero_spelling")
        return None
    json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
               parse_int=integer_token, parse_float=decimal_token, parse_constant=constant)

    def check_url(value):
        if isinstance(value, str) and ("\\" in value or any(ord(c) < 32 or ord(c) == 127 for c in value)):
            reasons.add("ambiguous_url_representation")

    stack = [doc]
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, dict):
            for key, value in item.items():
                if key in TIMESTAMP_FIELDS and isinstance(value, str):
                    m = SUBSECOND.search(value)
                    if m and len(m.group(1)) > 3:
                        reasons.add("timestamp_precision_exceeds_milliseconds")
                    if LEAP_SECOND.search(value):
                        reasons.add("leap_second")
                    if not validate_rfc3339(value.upper()):
                        reasons.add("timestamp_not_supported_rfc3339")
                if key in URL_FIELDS:
                    check_url(value)
                if key in URL_ARRAY_FIELDS and isinstance(value, list):
                    for url in value:
                        check_url(url)
                stack.append(value)
            if item.get("name") in ("location", "link") and isinstance(item.get("values"), list):
                for value in item["values"]:
                    if isinstance(value, str):
                        # Agreed restriction covers the entire URL-bearing header value.
                        check_url(value)
    return {"status":"outside_profile" if reasons else "within_profile",
            "reasons":sorted(reasons)}


def preflight(raw, validator):
    """Return independent local validation and profile results; never auto-accept."""
    result, _ = validate(raw, validator)
    p = profile(raw)
    return {"profile_id":PROFILE_ID, "profile_agreement":PROFILE_AGREEMENT,
            "input_sha256":digest(raw), "consumer_validation":result["status"],
            "profile":p,
            "disposition":"candidate_for_joint_review" if result["status"]=="valid"
                          and p["status"]=="within_profile" else "hold",
            "producer_validation_verified":False, "authorization_verified":False,
            "actual_exchange_verified":False, "operational_integration_approved":False}
