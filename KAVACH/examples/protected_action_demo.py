"""KAVACH 2.0 public protected-action reference demo.

This executable example uses the public SOFTWARE_REFERENCE runtime and bounded SDK
surface. The fixed byte strings below are local demo material only; they are not
production keys and are never presented as hardware-backed secrets.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from kavach_runtime import KAVACHRuntime, EvidenceObservation
from kavach_semantic import ProtectionRequest
from kavach_substrate.sdk import KAVACHClient


AUTHORITY_KEY = b"A" * 32
PROVIDER_KEY = b"P" * 32
EVIDENCE_KEY = b"E" * 32


def run_demo() -> dict:
    with tempfile.TemporaryDirectory(prefix="kavach-public-demo-") as temp:
        runtime = KAVACHRuntime(
            Path(temp),
            authority_key=AUTHORITY_KEY,
            provider_key=PROVIDER_KEY,
            evidence_key=EVIDENCE_KEY,
        )
        client = KAVACHClient(runtime, "client.public.demo")

        observation = EvidenceObservation(
            "evidence.demo.runtime",
            "TRUSTED",
            "a" * 64,
            {"source": "public-reference-demo"},
            True,
        )

        context = runtime.build_context(
            "reference.project",
            "reference.runtime",
            [observation],
            context_id="ctx:public-demo",
        )

        request = ProtectionRequest(
            "req:public-demo",
            "reference.project",
            "reference.runtime",
            "resource:demo",
            "reference.action.commit",
            "commit",
            context.digest,
            "b" * 64,
            "SOFTWARE_REFERENCE",
        )

        connection = client.connect()

        first = client.acquire(
            request,
            context,
            profile_ids=("KAVACH-BASE",),
            one_use=False,
        )
        if first.state != "OPEN" or first.envelope is None:
            raise RuntimeError(f"expected OPEN acquisition, got {first.state}")

        executed = client.execute(first.envelope, request, context)
        if executed.state != "OPEN":
            raise RuntimeError(f"expected OPEN execution, got {executed.state}")

        stale_candidate = client.acquire(
            request,
            context,
            profile_ids=("KAVACH-BASE",),
            one_use=False,
        )
        if stale_candidate.state != "OPEN" or stale_candidate.envelope is None:
            raise RuntimeError("failed to acquire stale-authority demonstration envelope")

        before_recovery = client.get_continuity()
        client.recover_authority("reference.project", "reference.runtime")
        after_recovery = client.get_continuity()

        stale_result = client.execute(
            stale_candidate.envelope,
            request,
            context,
        )

        if stale_result.state != "REFUSE":
            raise RuntimeError(f"expected REFUSE after recovery, got {stale_result.state}")
        if "STALE_CONTINUITY" not in stale_result.reason_codes:
            raise RuntimeError(
                "expected STALE_CONTINUITY after recovery; "
                f"got {stale_result.reason_codes}"
            )

        if not runtime.evidence.verify_chain():
            raise RuntimeError("evidence chain verification failed")

        return {
            "connection": connection["connected"],
            "assurance": runtime.provider.descriptor().profile,
            "acquire_state": first.state,
            "execute_state": executed.state,
            "recovery_before": before_recovery["recovery"],
            "recovery_after": after_recovery["recovery"],
            "old_authority_after_recovery": stale_result.state,
            "reason_codes": list(stale_result.reason_codes),
            "evidence_chain_valid": True,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run as a deterministic smoke test and print one compact PASS line.",
    )
    args = parser.parse_args()

    result = run_demo()

    if args.check:
        print(
            "PASS_KAVACH_PUBLIC_DEMO "
            f"acquire={result['acquire_state']} "
            f"execute={result['execute_state']} "
            f"after_recovery={result['old_authority_after_recovery']} "
            f"reason={','.join(result['reason_codes'])} "
            f"evidence={result['evidence_chain_valid']}"
        )
    else:
        print("KAVACH 2.0 — protected-action public reference demo")
        print(json.dumps(result, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
