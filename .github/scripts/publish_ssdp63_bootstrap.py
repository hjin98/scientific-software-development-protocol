#!/usr/bin/env python3
from pathlib import Path

B = "1484c1d3caa49d87cc15bc52a5e775399c1dae1b"


def edit(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"missing expected text in {path}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


versioning = "source/shared/references/protocol-versioning-and-compatibility.md"
edit(
    versioning,
    "The invalidated SHA remains historical implementation evidence only and **must not** be used as current Protocol 6.2 public fallback. The replacement SHA is the immutable self-reference-safe source snapshot whose source regression, canonical package build, and independent standalone package/link validation passed before this descendant published it.\n\nThe repository default branch is never a protocol-version oracle and a semantic version string is not assumed to be a Git ref.",
    f"The invalidated SHA remains historical implementation evidence only and **must not** be used as current Protocol 6.2 public fallback. The replacement SHA is the immutable self-reference-safe source snapshot whose source regression, canonical package build, and independent standalone package/link validation passed before this descendant published it.\n\nProtocol 6.3 public-source bootstrap is likewise distinct from future recovery:\n\n```text\n6.3.0 public-source bootstrap -> {B}\n```\n\nThat immutable ancestor passed repository regression, canonical package build, independent package validation and committed-distribution parity, Protocol 6.3 profile/snapshot parity, the full Orchestrator Core acceptance suite, and an exact-ref remote source/route/bootstrap realization before this descendant published the mapping. The bootstrap snapshot intentionally does not self-name; this later mapping supplies the version-to-ref authority. Protocol 6.3 recovery remains unavailable until complete qualification and independent Review close.\n\nThe repository default branch is never a protocol-version oracle and a semantic version string is not assumed to be a Git ref.",
)
edit(versioning, "| `ssdp-protocol-6.3` | 6.3.0 | 2 unless profile contract qualification proves a schema change is necessary | candidate/new only after 6.3 profile generation |", "| `ssdp-protocol-6.3` | 6.3.0 | 2 | candidate; generated and independently parity-checked |")
edit(versioning, "3. create a **public-source bootstrap** only from a source state whose required bootstrap-readiness checks already passed; later descendant mapping records that exact immutable ref—never `main`/latest/guessed version;", f"3. use public-source bootstrap `{B}` for version-bound 6.3 public fallback; that already-existing source state passed bootstrap-readiness checks before this later descendant published the exact mapping—never substitute `main`/latest/guessed version;")
edit(versioning, "Until the exact 6.3 bootstrap and recovery identities exist and their qualifying evidence is recorded, **do not insert placeholders or guessed SHAs into current fallback mappings** and do not treat the candidate profile as accepted-current. The accepted 6.2 mappings above remain operative for 6.2.", f"The exact 6.3 public-source bootstrap is now `{B}` and is usable only as the version-bound 6.3 public fallback. Recovery is still unavailable: **do not insert placeholders or guessed SHAs into recovery mappings** and do not treat the candidate profile as accepted-current. The accepted 6.2 mappings above remain operative for 6.2.")

edit("PORTABILITY.md", "6.3.0 public bootstrap -> UNAVAILABLE_PENDING_6.3_BOOTSTRAP_QUALIFICATION", f"6.3.0 public bootstrap -> {B}")
edit("PORTABILITY.md", "For Protocol 6.3, **do not** substitute the 6.2 bootstrap, current branch, repository default/latest, or a guessed `6.3.0` ref while the 6.3 mapping is unavailable. The 6.3 source candidate must first pass bootstrap-readiness checks at an immutable self-reference-safe source snapshot; only a later descendant may publish that exact SHA. Recovery is later and requires complete qualification plus independent Review. If neither compatible local source nor mapped compatible immutable public source can be read, report truthful non-closure.", f"For Protocol 6.3, version-bound public fallback now uses exactly `{B}`. Do **not** substitute the 6.2 bootstrap, current branch, repository default/latest, or a guessed `6.3.0` ref. This immutable source ancestor passed bootstrap-readiness and exact-ref remote route realization before a later descendant published the mapping. Recovery remains later and requires complete qualification plus independent Review. If neither compatible local source nor mapped compatible immutable public source can be read, report truthful non-closure.")
edit("PORTABILITY.md", "Protocol 6.2 remains accepted-current while 6.3 is a candidate. Version-bound 6.2 public fallback remains exact bootstrap `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` and accepted recovery remains `b59adc77efe6951912cfd705cc43830c58ca27d0`. Protocol 6.3 cannot displace that baseline until its own bootstrap, distinct profile/package resources, complete qualification, independent Review, recovery mapping, generated/Core parity, and lifecycle gates close.", f"Protocol 6.2 remains accepted-current while 6.3 is a candidate. Version-bound 6.2 public fallback remains exact bootstrap `5a062ebc472755607b9dc66d33a5ebbc4b7429aa` and accepted recovery remains `b59adc77efe6951912cfd705cc43830c58ca27d0`. Version-bound 6.3 public fallback is now exact bootstrap `{B}`, but this does not make 6.3 accepted-current. Protocol 6.3 cannot displace the 6.2 baseline until complete qualification, independent Review, recovery mapping, regenerated parity, and lifecycle gates close.")

prompts = "source/shared/references/development-workflow-prompts.md"
edit(prompts, "CURRENT_PUBLIC_REF = UNAVAILABLE_PENDING_6.3_BOOTSTRAP_QUALIFICATION", f"CURRENT_PUBLIC_REF = {B}")
edit(prompts, "**Protocol 6.3 pre-bootstrap state:** automatic public fallback for current 6.3 is intentionally unavailable until an already validated self-reference-safe source snapshot is designated by a later descendant. Never use repository default/latest, a guessed semantic-version ref, the current candidate branch, or the accepted 6.2 bootstrap as a substitute for a 6.3 ref. Version-bound 6.2 work continues to use exactly `5a062ebc472755607b9dc66d33a5ebbc4b7429aa`; historical 5.16/6.0/6.1 resolution remains version-bound to its own immutable mapping.", f"**Protocol 6.3 bootstrap state:** automatic public fallback for current version-bound 6.3 uses exactly immutable ref `{B}`. That source snapshot passed bootstrap-readiness and exact-ref remote route realization before a later descendant published this mapping; the bootstrap source intentionally does not self-name. Never use repository default/latest, a guessed semantic-version ref, the current candidate branch, or the accepted 6.2 bootstrap as a substitute for the 6.3 ref. Version-bound 6.2 work continues to use exactly `5a062ebc472755607b9dc66d33a5ebbc4b7429aa`; historical 5.16/6.0/6.1 resolution remains version-bound to its own immutable mapping.")

edit("README.md", "**Protocol 6.3 has no public bootstrap or recovery identity yet on this candidate branch.** The implementation intentionally refuses to guess/self-declare one. A 6.3 bootstrap may be named only after an already-existing source snapshot passes bootstrap-readiness validation; a later descendant publishes that exact SHA. Recovery is later still, after complete qualification and independent Review.", f"**Protocol 6.3 public-source bootstrap is `{B}`; Protocol 6.3 recovery remains unavailable.** The bootstrap is an already-existing self-reference-safe source snapshot that passed repository/package/profile/Core bootstrap-readiness plus exact-ref remote route realization before this later descendant published its identity. It is only the version-bound public fallback and does not make 6.3 accepted-current. Recovery remains later, after complete qualification and independent Review.")

edit("tests/test_protocol_62_representation.py", '                self.assertIn("current_public_ref = unavailable_pending_6.3_bootstrap_qualification", prompt)', f'                self.assertIn("current_public_ref = {B}", prompt)')

p = Path("tests/test_protocol_63_bootstrap.py")
text = p.read_text(encoding="utf-8")
if "from pathlib import Path\n" not in text:
    text = text.replace("import urllib.request\n", "import urllib.request\nfrom pathlib import Path\n", 1)
marker = "class Protocol63BootstrapTests(unittest.TestCase):\n"
if "test_current_public_mapping_is_exact_and_recovery_remains_unavailable" not in text:
    if marker not in text:
        raise SystemExit("missing Protocol63BootstrapTests marker")
    method = (
        marker
        + "    def test_current_public_mapping_is_exact_and_recovery_remains_unavailable(self) -> None:\n"
        + "        root = Path(__file__).resolve().parents[1]\n"
        + "        versioning = (root / 'source/shared/references/protocol-versioning-and-compatibility.md').read_text(encoding='utf-8')\n"
        + "        prompts = (root / 'source/shared/references/development-workflow-prompts.md').read_text(encoding='utf-8')\n"
        + "        portability = (root / 'PORTABILITY.md').read_text(encoding='utf-8')\n"
        + "        readme = (root / 'README.md').read_text(encoding='utf-8')\n"
        + "        self.assertIn(f'6.3.0 public-source bootstrap -> {BOOTSTRAP}', versioning)\n"
        + "        self.assertIn(f'CURRENT_PUBLIC_REF = {BOOTSTRAP}', prompts)\n"
        + "        self.assertIn(f'6.3.0 public bootstrap -> {BOOTSTRAP}', portability)\n"
        + "        self.assertIn(BOOTSTRAP, readme)\n"
        + "        self.assertIn('6.3.0 recovery -> UNAVAILABLE_PENDING_6.3_ACCEPTANCE', portability)\n"
        + "        self.assertNotIn('6.3.0  -> ' + BOOTSTRAP, versioning)\n\n"
    )
    text = text.replace(marker, method, 1)
p.write_text(text, encoding="utf-8")
