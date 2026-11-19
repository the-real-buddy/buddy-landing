/* The request-access form. It posts the four fields to /api/waitlist, which
   vercel.json rewrites to the app's public POST /waitlist, so the browser
   only ever talks to this origin. No cookies or tokens go with it, nothing
   is stored in the browser, and nothing is logged. Only a 204 is a receipt:
   every other answer, and no answer, leaves the form as it was to try again. */
(() => {
  const ENDPOINT = "/api/waitlist";
  const TIMEOUT_MS = 20000;
  // core members.TEAM_SIZES and members._EMAIL, so a request the server would refuse is caught here first.
  const TEAM_SIZES = ["just me", "2-5", "6-15", "16-50", "51+"];
  const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const form = document.getElementById("apply-form");
  const button = document.getElementById("submit");
  const formError = document.getElementById("form-error");
  const pending = document.getElementById("pending");
  const received = document.getElementById("received");
  const field = (name) => form.elements.namedItem(name);
  const LABEL = button.textContent;
  let sending = false;

  function setFieldError(name, message) {
    const input = field(name);
    const out = document.getElementById(name + "-error");
    out.textContent = message || "";
    out.hidden = !message;
    if (message) input.setAttribute("aria-invalid", "true");
    else input.removeAttribute("aria-invalid");
  }

  function setFormError(message) {
    formError.textContent = message || "";
    formError.hidden = !message;
  }

  function read() {
    const name = field("team_name").value.trim();
    return {
      email: field("email").value.trim(),
      team_size: field("team_size").value,
      first_job: field("first_job").value.trim(),
      team_name: name || null,
    };
  }

  // Returns the first field that is wrong, after marking every one that is.
  function check(body) {
    const wrong = [];
    const mark = (name, message) => { setFieldError(name, message); if (message) wrong.push(name); };
    mark("email", !body.email ? "enter your work email." : body.email.length > 254 || !EMAIL.test(body.email) ? "that email doesn't look right." : "");
    mark("team_size", TEAM_SIZES.includes(body.team_size) ? "" : "choose how many people would work with buddy.");
    mark("first_job", !body.first_job ? "tell us the first job you'd hand buddy." : [...body.first_job].length > 400 ? "keep it to 400 characters." : "");
    return wrong[0] || null;
  }

  function busy(on) {
    sending = on;
    button.setAttribute("aria-disabled", on ? "true" : "false");
    button.textContent = on ? "sending…" : LABEL;
    pending.textContent = on ? "sending your request." : "";
  }

  // What the person is told for each way a request can fail; never the server's own words.
  function failure(status) {
    if (status === 429) return "too many requests from here just now. wait a minute, then try again.";
    if (status === 400 || status === 422) return "something in the form doesn't look right. check your email and the first job, then try again.";
    if (status === null) return "we couldn't reach buddy. check your connection and try again.";
    return "we couldn't take your request just now. please try again in a moment.";
  }

  async function send(body) {
    const abort = new AbortController();
    const timer = setTimeout(() => abort.abort(), TIMEOUT_MS);
    try {
      const response = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        credentials: "omit",
        mode: "same-origin",
        cache: "no-store",
        redirect: "error",
        referrerPolicy: "no-referrer",
        signal: abort.signal,
      });
      return response.status;
    } catch {
      return null;
    } finally {
      clearTimeout(timer);
    }
  }

  function showReceived(email) {
    document.getElementById("sent-email").textContent = email;
    form.reset();
    form.hidden = true;
    received.hidden = false;
    document.getElementById("received-title").focus();
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (sending) return;
    setFormError("");
    const body = read();
    const first = check(body);
    if (first) {
      field(first).focus();
      return;
    }
    busy(true);
    const status = await send(body);
    if (status === 204) {
      busy(false);
      showReceived(body.email);
      return;
    }
    busy(false);
    setFormError(failure(status));
  });

  // A field's own message clears as soon as it is edited.
  for (const name of ["email", "team_size", "first_job"]) {
    field(name).addEventListener("input", () => setFieldError(name, ""));
  }
})();
