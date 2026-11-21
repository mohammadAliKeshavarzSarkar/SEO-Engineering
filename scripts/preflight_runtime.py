#!/usr/bin/env python3
"""Verify a *local* project installation and detect CLI presence without running agents.

Maintainer-side tool: no inference, login, skill discovery, isolation or permission checks.
The installed skill must be a trusted, separately reviewed exact ZIP source match.
"""
import argparse
import json
import shutil
from pathlib import Path

if __package__:
    from .build_skill import ROOT
    from .verify_package import verify, verify_installed
else:
    from build_skill import ROOT
    from verify_package import verify, verify_installed

PLACES = {
    "codex": (".agents", "skills", "seo-engineering"),
    "cursor": (".cursor", "skills", "seo-engineering"),
}
BINARIES = {"codex": ("codex",), "cursor": ("agent", "cursor-agent")}


def inspect(root, archive, installed, runtime, which=shutil.which):
    """Inspect trusted local paths; CLI presence is NOT runtime activation."""
    root = Path(root).resolve()
    installed = Path(installed)
    if runtime not in PLACES:
        raise ValueError("unsupported runtime label")
    if tuple(installed.parts[-3:]) != PLACES[runtime]:
        raise ValueError("installation not at selected project skill path")
    if installed.resolve().is_relative_to(root):
        raise ValueError("project installation must be outside source checkout")
    verified = verify(root, Path(archive))
    installation = verify_installed(installed, verified)
    found = [(name, which(name)) for name in BINARIES[runtime]]
    available = [name for name, loc in found if loc is not None]
    return {
        "schema_version": "1",
        "kind": "local_runtime_installation_preflight",
        "runtime": runtime,
        "installed_skill": "seo-engineering",
        "installed_layout": "/".join(PLACES[runtime]),
        "archive_sha256": verified["archive_sha256"],
        "installed_file_count": installation["file_count"],
        "exact_installed_bytes_checked": True,
        "command_names_on_path": available,
        "cli_detected": bool(available),
        "status": "ready_for_operator_activation_probe" if available else "blocked_cli_not_found",
        "cli_version_verified": False,
        "skill_discovery_observed": False,
        "skill_activation_observed": False,
        "read_isolation_verified": False,
        "tool_permissions_verified": False,
        "model_inference_performed": False,
        "manual_content_privacy_approved": False,
        "release_approved": False,
        "limitations": "PATH detection and source-matched installed bytes only. Operator must verify exact CLI version, configuration, duplicate skill installations, isolation, auth, model and actual unscored discovery in a fresh runtime. No inference or release decision."
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime", choices=sorted(PLACES), required=True)
    p.add_argument("--archive", type=Path, required=True)
    p.add_argument("--installed", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True, help="New private report file")
    args = p.parse_args()
    try:
        if args.out.exists() or args.out.is_symlink():
            raise ValueError("output must not exist")
        report = inspect(ROOT, args.archive, args.installed, args.runtime)
        with args.out.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, allow_nan=False, indent=2)
            handle.write("\n")
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        print("Local installation preflight failed:", exc)
        return 1
    print("Installation bytes checked; external activation and isolation remain unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
