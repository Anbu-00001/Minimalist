# Submission preflight: Docker image pull/platform/size checklist

Research pass, 2026-07-09, ahead of tonight's push to `ghcr.io/anbu-00001/amda-agent:latest`
(deadline 2026-07-11 16:00 UTC). Triggered by the live Track 1 leaderboard showing **71
DID NOT QUALIFY** submissions, of which **PULL_ERROR = 13** — the second-largest failure
category after `ACCURACY_GATE_FAILED` (38). This is not a hypothetical edge case; it is a
concrete, currently-observed way real teams are losing tonight.

**Live leaderboard snapshot** (re-fetched this pass, `lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`,
154 total Track 1 submissions visible): `ACCURACY_GATE_FAILED` 38, `PULL_ERROR` 13,
`RUNTIME_ERROR` 5, `TIMEOUT` 5, `ZERO_API_CALLS` 2 (paired with accuracy-gate failure),
`INVALID_RESULTS_SCHEMA` 1, `OUTPUT_MISSING` 1, **8 submissions successfully scored**
(this last number is new/better than V20's 2026-07-08 snapshot of zero passers — noted for
context only, out of scope for this doc).

**Single most important finding of this pass**: right now, before tonight's push,
`ghcr.io/anbu-00001/amda-agent:latest` **is not resolvable on the registry at all** — see
checklist item 2, which is not hypothetical, it's the actual current state, verified live
during this research (details in §A below).

---

## THE CHECKLIST — run every item, in order, before submitting

### 1. Build with buildx and the explicit platform flag — never a bare `docker build`
```
docker buildx build --platform linux/amd64 -t ghcr.io/anbu-00001/amda-agent:latest --push .
```
**Pass**: build completes and the final lines show a pushed digest for
`ghcr.io/anbu-00001/amda-agent:latest`.
**Fail**: any auth/network error mid-push — do not treat a partially-completed push as done.
This is the command already documented in the Dockerfile's own header comment; the risk
this guards against is real and specifically named in the Participant Guide: *"The judging
VM runs linux/amd64. Your image must include a linux/amd64 manifest or it will fail to
pull and score zero. If you build on Apple Silicon (M1/M2/M3), add `--platform linux/amd64`
to your build command."* A bare `docker build` on Apple Silicon (no buildx flag) produces a
**native arm64, single-platform image with no manifest list at all** — it runs fine on the
dev machine and fails outright on the amd64 grading VM. (This project's actual build host
is amd64 already — confirmed via `docker buildx ls`, `linux/amd64` listed as native — so
this specific trap doesn't apply to *this* machine, but always use the explicit flag anyway
since the command is what's documented as canonical and costs nothing.)

### 2. Immediately after push, verify the tag resolves on the registry — from scratch
```
docker manifest inspect ghcr.io/anbu-00001/amda-agent:latest
```
**Pass**: prints real manifest JSON (`schemaVersion`, `layers`, sizes).
**Fail**: `manifest unknown` or `not found`.

**This is not hypothetical — this is what happened when this exact command was run during
this research pass, right now, against the current tag:**
```
$ docker manifest inspect ghcr.io/anbu-00001/amda-agent:latest
manifest unknown
$ docker buildx imagetools inspect ghcr.io/anbu-00001/amda-agent:latest
ERROR: ghcr.io/anbu-00001/amda-agent:latest: not found
$ docker pull ghcr.io/anbu-00001/amda-agent:latest
Error response from daemon: failed to resolve reference "ghcr.io/anbu-00001/amda-agent:latest": ghcr.io/anbu-00001/amda-agent:latest: not found
```
A local image with that exact tag exists (`docker images` shows it, built
2026-07-09T07:57:23+05:30, linux/amd64, content size 2.53GB) and `~/.docker/config.json`
already has stored `ghcr.io` credentials — so this "not found" is with authentication
available, not an anonymous-access artifact. **As of this research pass, the image has
never been successfully pushed to this tag (or was pushed and later overwritten/removed).**
Do not assume a prior `docker buildx build --push` succeeded just because it ran without a
visible error — re-verify with this exact command after tonight's push, every time.

### 3. Verify anonymous (unauthenticated) pull works — simulates the grading VM, which has no GitHub login
```
curl -s "https://ghcr.io/token?service=ghcr.io&scope=repository:anbu-00001/amda-agent:pull"
```
**Pass**: returns a JSON object with a `token` field.
**Fail**: `{"errors":[{"code":"DENIED","message":"requested access to the resource is denied"}]}`
— this is exactly what this exact command returned during this research pass, for this
exact repository path. Note the ambiguity this reveals: GHCR's anonymous token endpoint
returns the identical `DENIED` response whether the package **doesn't exist** or **exists
but is private** — by design, to avoid leaking the existence of private repos to anonymous
callers. That means a `DENIED` here does not by itself tell you which problem you have; it
only tells you the grading VM (which pulls anonymously, with no credentials injected for
your own registry) will fail exactly the same way. Fix by doing step 1 (push) and step 4
(visibility), then re-run this curl until it returns a token.

### 4. Explicitly set the GHCR package visibility to Public — do not assume it inherits from the repo
**Where**: `https://github.com/users/Anbu-00001/packages/container/amda-agent/settings`
(adjust path if pushed under an org) → find the visibility control → set to **Public**
→ confirm.
**Pass**: the package settings page reads "Public".
**Fail**: "Private" (GHCR's default) or "Internal".
**Why this is a real, commonly-reported GHCR gotcha, not a guess**: per GitHub's own docs
(`docs.github.com/.../working-with-the-container-registry`), *"When you first publish a
package, the default visibility is private"* — and this applies **regardless of the source
repository's visibility**. A package only inherits a repo's access permissions if it was
explicitly linked to that repo (e.g. pushed from a GitHub Actions workflow using the
`GITHUB_TOKEN` in that repo's context, or manually linked after the fact); a manual
`docker push` from a laptop, which is what a hackathon submission build typically is, does
**not** auto-link. This project's own git remote is `github.com/Anbu-00001/Minimalist` —
there is no repository literally named `amda-agent` for the `amda-agent` package to link to
even if we wanted auto-linking — so manual visibility-setting is not optional here, it is
the only path to public. The generic failure users hit downstream of forgetting this step
is a plain `denied: denied` from `docker pull` (confirmed via a GHCR troubleshooting guide),
which is indistinguishable at pull time from "wrong credentials" or "doesn't exist" —
exactly the ambiguity in step 3.

### 5. Verify the manifest actually on the registry declares `linux/amd64` — don't just trust the local build
```
docker buildx imagetools inspect ghcr.io/anbu-00001/amda-agent:latest
docker manifest inspect -v ghcr.io/anbu-00001/amda-agent:latest
```
**Pass**: for a single-platform manifest (what our Dockerfile builds — one `--platform`,
no fat manifest list), `docker manifest inspect -v` output contains
`"platform": { "architecture": "amd64", "os": "linux" }` inside the `Descriptor` object.
(Verified this exact shape by running it against a known-public GHCR image,
`ghcr.io/github/super-linter:latest`, during this pass — a single, non-list manifest still
reports `Descriptor.platform.architecture`/`.os`.) If a multi-platform manifest list is ever
used instead, `docker buildx imagetools inspect` prints one `Platform:` line per
architecture (verified against `docker.io/library/python:3.12-slim`, which lists
`linux/amd64`, `linux/arm/v5`, etc. individually) — at least one of those lines must read
`linux/amd64`.
**Fail**: `architecture` reads `arm64`, or no `linux/amd64` entry exists anywhere.

### 6. Diff the exact tag string against what you're about to paste into the submission form
```
docker inspect --format '{{.RepoTags}}' ghcr.io/anbu-00001/amda-agent:latest
```
**Pass**: character-for-character match with the string in the submission form (registry
paths are case-sensitive; `:latest` pushed but a different tag typed into the form, or vice
versa, is an indistinguishable-from-PULL_ERROR failure mode).
**Fail**: any mismatch, including case or a stray tag suffix from a previous build.

### 7. Verify actual compressed size from the registry side — never trust local `docker images`
```
docker buildx imagetools inspect ghcr.io/anbu-00001/amda-agent:latest --raw \
  | jq '(([.layers[].size] | add) + .config.size) / 1024 / 1024 / 1024'
```
**Pass**: result comfortably under 10 (GiB). Command verified during this pass against a
real public image (summed to 1.87 GiB for `ghcr.io/github/super-linter:latest`, matching
the "compressed size" concept the Participant Guide caps at 10GB: *"Image compressed size
must not exceed 10GB — larger images are rejected before pulling"*).
**Fail**: result at or above 10, or uncomfortably close (treat >9 as a red flag).
Current local content-size for our image is **2.53GB** (`docker images` "CONTENT SIZE"
column) which lines up with `du -sh models/` = 2.4GB + `tools/llama-b9888/` = 39MB + Python
deps — a healthy ~4x margin *if the local number tracks the pushed number*, but this must
be re-run against the actual pushed artifact after step 1, not assumed from the local
figure, because local `docker images` size and true registry compressed size are computed
differently (local is a reconstructed/deduplicated estimate, registry is the literal sum of
gzip'd layer blobs actually transferred on pull).

### 8. Cold-start timing test — evict local cache, then time pull+run exactly like the grading VM would
```
docker rmi ghcr.io/anbu-00001/amda-agent:latest
time docker run --rm -v ./input:/input:ro -v ./output:/output \
  -e FIREWORKS_API_KEY=test -e FIREWORKS_BASE_URL=... -e ALLOWED_MODELS=... \
  ghcr.io/anbu-00001/amda-agent:latest
```
(`docker run` on a locally-absent tag auto-pulls first, so this measures pull+start
together, same as the harness will experience on its first-ever pull of your image.)
**Pass**: total wall time from pull start to the entrypoint's readiness signal is
comfortably under 60s.
**Fail / risk to mitigate**: `docker/entrypoint.sh`'s model-wait loop can spend up to 40
seconds (40 iterations × 1s sleep) polling `llama-server`'s `/health` endpoint before it
even `exec`s `agent.main` — and that 40s budget is entirely on top of however long the pull
itself takes. This stacking (pull latency + entrypoint's own 40s ceiling) is a real,
previously-undocumented interaction: `research/VERDICTS.md` V20 covers the entrypoint's
internal model-load timing in isolation, but nothing in the repo's research previously
combined it with pull latency against the 60s wall clock. If this test shows less than
~15-20s of margin, shrink the wait-loop ceiling (e.g. 40→20 iterations) — `entrypoint.sh`
already treats a dead/slow local server as a safe degrade to remote-only Fireworks routing,
so losing local-token savings on a slow cold start is far cheaper than a `TIMEOUT` zero.

### 9. Push well ahead of the deadline; do one throwaway pull yourself before submitting
```
# after step 1's push completes:
docker rmi ghcr.io/anbu-00001/amda-agent:latest   # evict local cache again
docker pull ghcr.io/anbu-00001/amda-agent:latest  # warm the registry/CDN path
```
**Pass**: this warm-up pull completes at normal speed.
**Why**: documented, reported GHCR behavior is that a freshly-pushed image's blobs can be
slow on the *first* pull while they propagate across GHCR's CDN edge (Fastly) — "if you
push an image, the first few GBs are fast, then it becomes very slow" and "the first node to
pull an image still has to wait for GHCR; every subsequent node gets the cached version" are
both reported patterns (GitHub community discussions on ghcr.io performance, cited below).
If the grading harness's pull is the literal first pull after your push, you've stacked an
unknown CDN cold-pull penalty on top of item 8's 60s budget for no reason — submitting
minutes after pushing needlessly makes your image "cold" for the harness. Do the warm-up
pull yourself first; it costs nothing and removes this variable entirely.

### 10. Final smoke test: exit code and `/output/results.json` contract
```
echo $?   # after the container run in item 8, must be 0
jq . /output/results.json >/dev/null && echo "valid JSON"
```
against the 8 official practice tasks (`test_io/practice_tasks.json`, per V20). **Pass**:
exit code 0, `jq` parses cleanly, one result per input `task_id`. **Fail**: non-zero exit
or malformed JSON — the guide is explicit these score zero regardless of pull success:
*"Exit code 0 on success, non-zero on failure"* and *"/output/results.json must be valid
JSON, malformed output scores zero."* These are a different failure family than
`PULL_ERROR` but account for `RUNTIME_ERROR` (5) + `INVALID_RESULTS_SCHEMA` (1) +
`OUTPUT_MISSING` (1) = 7 more of the current 71 DID NOT QUALIFY, cheap to rule out in the
same pass since you're already running the container end-to-end for item 8.

---

## Supporting research

### A. Current, verified state of `ghcr.io/anbu-00001/amda-agent:latest` (right now, pre-push)

Run live during this research pass:
- `git remote -v` → `origin https://github.com/Anbu-00001/Minimalist` — the git repo backing
  this codebase is named `Minimalist`, **not** `amda-agent`. There is no GitHub repository
  named `amda-agent` for the `ghcr.io/anbu-00001/amda-agent` package to auto-link to, which
  is directly relevant to checklist item 4 (visibility does not and cannot inherit from a
  same-named repo here).
- `docker images` shows a local image tagged `ghcr.io/anbu-00001/amda-agent:latest`,
  built 2026-07-09T07:57:23+05:30, `linux/amd64` (confirmed via `docker image inspect
  --format '{{.Os}}/{{.Architecture}}'`), content size 2.53GB, disk usage 5.26GB (disk usage
  includes build-cache overhead the registry never sees; content size is the closer proxy
  for what gets pushed, but is still not the authoritative compressed-size figure — see
  item 7).
- `~/.docker/config.json` already has a stored `ghcr.io` auth entry (present, not empty) —
  so the following failures are *not* explained by missing local credentials:
  - `docker manifest inspect ghcr.io/anbu-00001/amda-agent:latest` → `manifest unknown`
  - `docker buildx imagetools inspect ghcr.io/anbu-00001/amda-agent:latest` → `not found`
  - `docker pull ghcr.io/anbu-00001/amda-agent:latest` → `failed to resolve reference ...: not found`
  - Fully anonymous (`curl` to the GHCR token endpoint, no docker config involved) →
    `{"errors":[{"code":"DENIED","message":"requested access to the resource is denied"}]}`
- Interpretation: the currently-tagged local image has **not** been successfully pushed to
  this tag on GHCR (or was pushed and no longer resolves). Tonight's actual `docker buildx
  build --platform linux/amd64 --push .` (checklist item 1) has not yet happened as of this
  research pass, or did not complete. This is the concrete reason checklist item 2 exists
  and must be re-run after every push, not assumed.

### B. GHCR package visibility defaults to private, independent of repo visibility

Source: GitHub Docs, *Working with the Container registry*
(`docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry`),
fetched directly this pass: *"When you first publish a package, the default visibility is
private."* This applies regardless of whether the source repository is public — a package
only takes on a repo's permissions if explicitly linked, and a plain `docker push` from a
local machine does not create that link automatically. Corroborated by a second source
(`niklasmtj.de` / `dev.to` write-up on GHCR + GitHub Actions visibility, found via search)
describing the same default-private behavior as a common point of confusion, and by a GHCR
troubleshooting page (`w3tutorials.net`) documenting the exact downstream symptom: an
anonymous `docker pull` of a still-private package returns the generic `denied: denied`,
which gives no hint that "set visibility to Public" is the fix. This matches this project's
situation exactly (§A): once pushed, the package must be manually flipped to Public via its
package settings page before any anonymous pull — including the grading harness's — will
succeed.

### C. The `linux/amd64` manifest requirement, and how to check it before trusting it

Participant Guide (verbatim, `Participant Guide_ AMD Developer Hackathon (ACT II).pdf`,
read directly from the repo root):
> "The judging VM runs linux/amd64. Your image must include a linux/amd64 manifest or it
> will fail to pull and score zero. If you build on Apple Silicon (M1/M2/M3), add
> `--platform linux/amd64` to your build command: `docker buildx build --platform
> linux/amd64 --tag your-image:latest --push .` Standard linux/amd64 builds (e.g. built on
> Intel/AMD or GitHub Actions) are fine without any [changes]."

Failure mode if this is skipped: a bare `docker build` (the classic, non-buildx builder) on
an ARM host (Apple Silicon, or an ARM cloud dev box) produces a **native, single-platform
arm64 image** — it has no manifest list, just one arch, and that arch is wrong for the
judging VM. It runs perfectly on the dev machine (same arch) and looks completely fine
locally (`docker run` works, tests pass) right up until the grading VM tries to pull and run
it, at which point it fails outright with no local symptom ever having warned you. Confirmed
via `docker/buildx` GitHub issues (#2168, #1101) that cross-arch buildx builds can also fail
in non-obvious ways (QEMU emulation gaps, compiler segfaults) — another reason to always
build to the target platform explicitly and then verify server-side rather than trust the
build step alone.

Verification commands (both validated against real public images during this pass, exact
output shapes shown in the checklist above):
- `docker buildx imagetools inspect <ref>` — for manifest **lists**, prints one `Platform:`
  line per architecture (validated against `docker.io/library/python:3.12-slim`, which
  listed `linux/amd64`, `linux/arm/v5`, plus attestation manifests).
- `docker manifest inspect -v <ref>` — for **single-platform** manifests (what this project
  actually builds — one `--platform linux/amd64`, no fat manifest), the platform lives in
  `Descriptor.platform.architecture` / `.os`, not in a `Platform:` line (validated against
  `ghcr.io/github/super-linter:latest`, itself a single, non-list manifest).
- Both commands work anonymously against public images with no `docker login` required —
  confirmed by successfully running both against `ghcr.io/github/super-linter:latest`
  without any GHCR credentials.

### D. Image size: what counts, and how to check it without trusting `docker images`

Participant Guide, verbatim (appears twice, Track 1 and Track 2 rules sections):
> "Image compressed size must not exceed 10GB — larger images are rejected before pulling."

"Compressed" here is the standard OCI/Docker registry meaning: the sum of the gzip'd layer
blobs (plus the small config blob) that the registry actually stores and transfers — this is
what `docker manifest inspect` / `docker buildx imagetools inspect --raw` report per-layer
via each layer's `size` field, and it is **not** the same number `docker images` shows
locally (which is either an uncompressed filesystem estimate or, in this Docker CLI version,
a deduplicated "content size" that may undercount or overcount relative to what was actually
pushed, depending on layer-sharing with other local images). The only authoritative check is
against the pushed artifact:
```
docker buildx imagetools inspect <ref> --raw | jq '(([.layers[].size] | add) + .config.size)'
```
validated during this pass by running it against `ghcr.io/github/super-linter:latest` (summed
to ~1.87 GiB, a plausible compressed size for that image) and by inspecting the raw manifest
JSON directly to confirm every layer has a `size` field with the gzip'd (not raw tar) byte
count, per the `mediaType: application/vnd.docker.image.rootfs.diff.tar.gzip` on every layer
entry. (`crane` and `skopeo` are commonly recommended alternatives for the same job but were
not installed in this environment — `docker buildx imagetools` + `jq`, both already present,
cover the same ground with no new dependency.)

This project's current on-disk footprint (`du -sh models/` = 2.4GB, `tools/llama-b9888/` =
39MB, plus a 3-line `requirements.txt`'s worth of Python deps) lines up with the local
`docker images` content-size reading of 2.53GB for the built-but-unpushed image — a
comfortable ~4x margin under the 10GB cap if the pushed number tracks the local one, but
per checklist item 7 this must be re-confirmed against the actual registry artifact, not
assumed from the local figure.

### E. Cold-pull latency and CDN propagation — a real, separate risk from entrypoint timing

Multiple independent GitHub community discussions (`orgs/community/discussions/173607`,
`orgs/community/discussions/177907`, `orgs/community/discussions/31175`, all found via
search and read via their search-result summaries) describe recurring ghcr.io performance
issues:
- Regional/CDN routing sends some pulls to a distant Fastly edge node, producing very slow
  transfers from certain regions.
- A commonly reported pattern: "if you push an image, the first few GBs are fast, then it
  becomes very slow" — consistent with cache-miss behavior on a freshly-pushed blob before
  it's propagated to the edge node serving the puller.
- "The first node to pull an image still has to wait for GHCR. Every subsequent node gets
  the cached version" — i.e., the very first pull after a push is structurally the slowest
  one, and if the grading harness's pull is that first pull, you inherit that penalty with
  zero warning from anything you tested locally (your own local pulls after your own push
  from the same network path may hit a warm edge that the harness's VM, likely in a
  different region/network, does not).

This has not previously been connected in this repo's research to the 60-second
container-ready budget. `research/VERDICTS.md` V20 documents `docker/entrypoint.sh`'s
*internal* timing (up to 40s spent polling `llama-server` health before `exec python -m
agent.main`), but that is entirely separate from, and additive with, whatever the pull
itself costs — and the Participant Guide's *"Your container must start and be ready within
60 seconds"* does not specify whether the pull is inside or outside that 60s window. Given
that ambiguity, the conservative assumption (pull time counts against the budget) is the
only safe one, which is why checklist items 8 and 9 exist: measure the real stacked
pull+entrypoint time on a cold cache, and warm the registry path yourself before the harness
ever touches it.

**Rate limits**: search results for GHCR anonymous-pull rate limits were inconsistent — one
source claimed "60 requests/hour" for anonymous users (unclear if this figure was actually
about GHCR or conflated with Docker Hub's well-documented anonymous-pull limit, which is a
different, much more widely-documented number for a different registry), while a GitHub
community discussion thread and GitHub's own docs describe GHCR as billing by storage/data
transfer rather than by request count, with "no usage rate limit for public registries"
noted by one community researcher. **This could not be confirmed to a specific number for
GHCR and should be treated as a genuine unknown**, not asserted as fact — the practical
mitigation (item 9: authenticate/pre-warm, and don't rely on many rapid re-pulls) covers the
risk either way without needing the exact number.

### F. Hackathon/competition-specific Docker postmortems

Searched directly for prior hackathon postmortems describing Docker submission failures
(distinct from generic Docker documentation). **No hackathon-specific postmortem document
was found** covering this exact grading-harness-pulls-your-image pattern; search results
returned only generic Docker/CI troubleshooting docs, unrelated hackathon postmortems (game
jams, unrelated software projects), and generic Harness CI/CD product documentation (a
same-named but unrelated product, "Harness.io"). This should be stated plainly as a gap, not
papered over: item **5** of the original research ask (search for prior hackathon
postmortems specifically) came back empty. The concrete, verifiable failure modes in this
document (§A–E) are drawn from GHCR's own documented behavior and this project's own
live-tested current state, not from a hackathon postmortem, because none surfaced.

---

## Sources consulted this pass

- `Participant Guide_ AMD Developer Hackathon (ACT II).pdf` (repo root, read directly via
  `pdftotext -layout`, full text)
- `research/VERDICTS.md` V20 (grading environment constraints, entrypoint timing context)
- `research/zero_token_championship.md` §1.3 (prior leaderboard snapshot, PULL_ERROR counts)
- `https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live` (via `r.jina.ai`
  proxy fetch, re-fetched this pass for current counts)
- `Dockerfile`, `docker/entrypoint.sh` (repo root / `docker/`, read directly)
- Live commands run against this repo's actual Docker state and against
  `ghcr.io/anbu-00001/amda-agent:latest` (§A)
- Live commands run against known-public reference images to validate command syntax/output
  shape before trusting it: `ghcr.io/github/super-linter:latest`,
  `docker.io/library/python:3.12-slim`
- [Configuring a package's access control and visibility — GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility)
- [Working with the Container registry — GitHub Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [GitHub Actions workflows in combination with GHCR Package Visibility — niklasmtj.de](https://niklasmtj.de/blog/gh-actions-workflows-combination-with-ghcr/)
- [Troubleshooting: Unable to Pull Public/Private Images from GHCR — w3tutorials.net](https://www.w3tutorials.net/blog/unable-to-pull-image-from-github-container-registry-ghcr/)
- [Possible rate limits for pulling images from ghcr.io? — GitHub community discussion #49671](https://github.com/orgs/community/discussions/49671)
- [Cannot pull public image from GHCR anonymously — k3s-io/k3s#2401](https://github.com/k3s-io/k3s/issues/2401)
- [Unable to build for platform linux/amd64 on ARM — docker/buildx#2168](https://github.com/docker/buildx/issues/2168)
- [Error building arm64 image on x86-64 machine — docker/buildx#1101](https://github.com/docker/buildx/issues/1101)
- [Degraded performance with ghcr.io — GitHub community discussion #173607](https://github.com/orgs/community/discussions/173607)
- [GHCR docker push hangs mid-upload — GitHub community discussion #177907](https://github.com/orgs/community/discussions/177907)
- [Push docker images too slow — GitHub community discussion #31175](https://github.com/orgs/community/discussions/31175)
- `docker manifest`, `docker buildx imagetools inspect` CLI reference (docs.docker.com,
  behavior additionally validated directly by running both this pass)
