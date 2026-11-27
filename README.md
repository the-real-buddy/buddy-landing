# the44-landing

The static marketing site for buddy, served by Vercel at `trybuddynow.com`.
It has no build step and no packages: what is in the repo is what is served.

| path | file | what it is |
|---|---|---|
| `/` | `index.html` | the homepage: a prerendered copy of the canvas markup, then the same markup in `<template id="landing">`, which the inline script renders live over it |
| `/waitlist` | `waitlist/index.html`, `waitlist/waitlist.css`, `waitlist/waitlist.js` | the standalone request-access page (THE-44) |
| `POST /api/waitlist` | `vercel.json` rewrite | the one route the request-access form posts to |

The homepage keeps each link in BOTH copies: an edit to the prerendered
markup must be made to the template too, or it changes back when the
script runs. Its "request access" buttons go to `/waitlist`; "sign in"
goes to the app, `https://app.trybuddynow.com/app/`.

## The request-access flow, and what it depends on

This page only records a request. Everything after it lives in buddy-core
(`the44-core`), and **this repo does not show that those controls are
deployed**: check core's own status before pointing people here.

1. The homepage's "request access" opens `/waitlist`.
2. The person gives a work email, team size, the first job they'd hand
   buddy and a company or team name. The page posts them to
   `/api/waitlist` on its own origin.
3. Vercel rewrites that request to core's public `POST /waitlist`, which
   records one request per address and answers `204` with no body, for a
   first request and a repeat alike (so the form never says whether an
   address has applied). Only that `204` shows the "request received"
   screen; it promises no access and creates no account.
4. The owner approves the request by hand (core's ops/admin path).
5. An approval is for that exact email address. The person must sign in
   to the app with that address, independently verified, and is then
   allowed to create ONE team.
6. Coworkers never come through this page: they join only by an invite the
   team sends to their email, scoped to that one team.

Nothing on this page signs anyone up, redirects them into the app, or
stores anything in the browser.

### The backend contract

From core's `harness_module/members.py` (`request_access`, `TEAM_SIZES`)
and `harness_module/api.py` (`POST /waitlist`) on core PR #127's head
`92f9fe05`, inspected 2026-11-27 (not a claim about main or production):

- `POST /waitlist`, JSON `{"email", "team_size", "first_job", "team_name"}`, no session.
- `email`: required; core trims, lowercases and needs `[^\s@]+@[^\s@]+\.[^\s@]+`.
  The page also caps it at 254 characters.
- `team_size`: exactly one of `just me`, `2-5`, `6-15`, `16-50`, `51+`.
- `first_job`: 1 to 400 characters after trimming.
- `team_name`: required; core trims it, refuses an empty one with `400`, and keeps at most 120 characters, the page's own limit.
- `204` on success; `400` on a refused field; `429` when rate limited;
  errors are `{"code", "message", "retryable"}`, which the page never shows.

If core changes any of these (in particular the team sizes), change
`waitlist/index.html` and `waitlist/waitlist.js` with it.

## The Vercel route: a deployment prerequisite, not verified

`vercel.json` rewrites exactly `/api/waitlist` to
`https://app.trybuddynow.com/waitlist`, so the browser only ever talks to
`trybuddynow.com` and never has a reason to send the app's cookies. The
form also sends `credentials: "omit"`, so no cookie or auth header goes
from the page at all. This is not a generic proxy and adds no CORS.

None of this has been deployed or tried against the real host. Before
relying on it:

- **The upstream mapping is unverified.** Confirm that
  `https://app.trybuddynow.com/waitlist` reaches core's `POST /waitlist`
  (core serves its API at the app origin's root and the app under `/app`,
  but check the deployment in front of it), and that it is the core
  build with the THE-44 controls in it.
- **The method is not constrained.** `vercel.json` rewrites cannot match
  on method, so a GET to `/api/waitlist` is forwarded too; core only
  defines `POST /waitlist`, so anything else gets core's refusal. The path
  is exact, so no other core route is reachable through it.
- **Rate limiting.** Core limits `POST /waitlist` per source address
  (`quotas.auth_attempts_per_minute`, 30/min) using the connection's peer
  address. Through a Vercel rewrite that address may be Vercel's, shared
  by everyone, so legitimate people could get `429` together. Confirm
  what core sees as the client address behind Vercel (and whatever proxy
  fronts core) before launch.
- **Origin.** The browser sends `Origin: https://trybuddynow.com` on the
  POST and Vercel forwards request headers. Core does not origin-check
  `/waitlist` today (it checks only authenticated requests); if it adds an
  allowlist for this route, the landing origin must be on it.
- After deploying to a preview, check: `GET /waitlist` serves the page;
  a synthetic POST with a test address you own reaches core and answers
  `204`; a bad body answers `400`.

`vercel.json` also sets `frame-ancestors 'none'`, `nosniff` and
`no-referrer` on `/waitlist`; the page carries its own CSP in a meta tag
(`connect-src 'self'`, scripts and styles from this origin and Google
Fonts only).

## Testing locally

Serve the folder and open the page:

```sh
python3 -m http.server 8044
# http://localhost:8044/            the homepage
# http://localhost:8044/waitlist/   the request-access page
```

`python3 -m http.server` does not apply `vercel.json`, so there is no
`/api/waitlist` locally: a submit shows the "couldn't take your request"
error and keeps what was typed, which is the expected failure path. Never
point a local test at the real endpoint; intercept `/api/waitlist` in the
browser instead (the THE-44 verification harness does this with
Playwright, answering `204`, `429`, `400`, `500` and a dropped connection
synthetically).

### Repeatable offline browser smoke check

With Python Playwright and local Chromium available:

```sh
python3 tests/browser_smoke.py
```

This starts a temporary local server on a free port, blocks external HTTPS,
intercepts every application POST with synthetic responses and asserts the
homepage handoff, error/receipt handling, absent credentials/storage and
320/390/768/1440px overflow checks. It never submits to the real app.
Screenshots and JSON results are printed in a temporary evidence directory.
This does not test Vercel's deployed routing or the actual core backend.

`vercel dev` would apply the rewrite, but it sends real requests to the
real app host, so don't use it to submit the form.

## Local end-to-end check (synthetic)

buddy-core PR #78's `scripts/e2e_local/flows.py` (branch `feat/the-44-waitlist-admit`; core
PR #127 dropped it) serves this repo's files on 127.0.0.1 and stands
in for the `/api/waitlist` rewrite by forwarding it to a local core, then drives the form
in headless Chromium (receipt, repeat, and the mail outcomes core records). It proves the
page against core's real `POST /waitlist`; it does not prove the Vercel rewrite or the
client address Vercel presents, which stay unverified (above).
