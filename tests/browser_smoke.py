"""Independent local-only browser review. Endpoint and fonts intercepted; no real submit."""

import json
import shutil
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(tempfile.mkdtemp(prefix="buddy-landing-browser-"))
OUT.mkdir(exist_ok=True)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path == "/waitlist":
            self.path = "/waitlist/index.html"
        super().do_GET()


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{server.server_port}"
checks = []


def check(label, condition):
    assert condition, label
    checks.append(label)


try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=shutil.which("chromium"), args=["--no-sandbox"]
        )
        errors = []
        for js in [False, True]:
            ctx = browser.new_context(java_script_enabled=js)
            ctx.route("https://**/*", lambda r: r.abort())
            page = ctx.new_page()
            page.goto(BASE + "/")
            if js:
                page.wait_for_timeout(300)
            links = page.get_by_role("link", name="request access", exact=False)
            check(
                f"homepage request-access links js={js}",
                links.count() >= 2
                and all(
                    links.nth(i).get_attribute("href") == "/waitlist"
                    for i in range(links.count())
                ),
            )
            sign = page.get_by_role("link", name="sign in", exact=True)
            check(
                f"homepage app sign-in js={js}",
                sign.count() >= 1
                and sign.first.get_attribute("href")
                == "https://app.trybuddynow.com/app/",
            )
            ctx.close()
        ctx = browser.new_context()
        ctx.route("https://**/*", lambda r: r.abort())
        page = ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        requests = []
        mode = {"status": 204}

        def endpoint(route):
            req = route.request
            requests.append(
                {
                    "method": req.method,
                    "headers": req.headers,
                    "body": req.post_data_json,
                }
            )
            if mode["status"] == "network":
                route.abort()
            else:
                route.fulfill(
                    status=mode["status"],
                    body=""
                    if mode["status"] == 204
                    else '{"message":"do not display internal server words"}',
                    headers={"content-type": "application/json"},
                )

        ctx.route("**/api/waitlist", endpoint)
        for status in [200, 400, 422, 429, 503, "network", 204]:
            mode["status"] = status
            page.goto(BASE + "/waitlist")
            page.locator("#email").fill("review@synthetic.invalid")
            page.locator("#team_size").select_option("2-5")
            page.locator("#first_job").fill("Synthetic browser fixture; no real email")
            page.locator("#team_name").fill("Synthetic team")
            page.locator("#submit").click()
            page.wait_for_function(
                "document.querySelector('#submit').getAttribute('aria-disabled') === 'false'"
            )
            check(
                f"status {status}: receipt iff204",
                page.locator("#received").is_visible() == (status == 204),
            )
            if status != 204:
                check(
                    f"status {status}: retains inputs",
                    page.locator("#email").input_value() == "review@synthetic.invalid",
                )
                check(
                    f"status {status}: user-facing error",
                    page.locator("#form-error").is_visible()
                    and "internal server words"
                    not in page.locator("#form-error").inner_text(),
                )
            check(
                f"status {status}: no persistent browser state",
                page.evaluate("localStorage.length===0 && sessionStorage.length===0"),
            )
        check("endpoint only public POST", all(r["method"] == "POST" for r in requests))
        check(
            "no auth/cookie headers",
            all(
                "cookie" not in r["headers"] and "authorization" not in r["headers"]
                for r in requests
            ),
        )
        for width in [320, 390, 768, 1440]:
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(BASE + "/waitlist")
            check(
                f"width{width}: no horizontal overflow",
                page.evaluate("document.documentElement.scrollWidth<=innerWidth"),
            )
            page.screenshot(path=str(OUT / f"waitlist-{width}.png"), full_page=True)
        check("no page errors", not errors)
        ctx.close()
        browser.close()
        (OUT / "results.json").write_text(
            json.dumps(
                {
                    "checks": checks,
                    "count": len(checks),
                    "page_errors": errors,
                    "scope": "local static page + intercepted synthetic public API; no actual Vercel routing/backend verification",
                },
                indent=2,
            )
        )
        print(
            "PASS",
            len(checks),
            "independent browser assertions. No real submissions. Evidence:",
            OUT,
        )
finally:
    server.shutdown()
    server.server_close()
