from __future__ import annotations

import json
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")


def run_node_harness(harness: str, source_path: Path, scenario: dict | None = None) -> dict:
    """Execute a repository JavaScript file against a minimal, deterministic DOM."""
    command = [NODE, "-e", textwrap.dedent(harness), str(source_path)]
    if scenario is not None:
        command.append(json.dumps(scenario))

    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return json.loads(completed.stdout)


FORGOT_PASSWORD_HARNESS = r"""
    const fs = require('node:fs');
    const vm = require('node:vm');

    const sourcePath = process.argv[1];
    const scenario = JSON.parse(process.argv[2]);
    const calls = [];
    const alerts = [];
    let handler = null;
    let prevented = false;

    const form = {
        addEventListener(type, callback) {
            if (type === 'submit') handler = callback;
        },
    };
    const emailInput = { value: scenario.email };

    global.window = { location: { href: scenario.locationHref } };
    global.document = {
        getElementById(id) {
            if (id === 'forgotPasswordForm') {
                return scenario.formPresent ? form : null;
            }
            if (id === 'email') {
                return scenario.emailInputPresent ? emailInput : null;
            }
            return null;
        },
    };
    global.alert = (message) => alerts.push(message);
    global.supabaseClient = {
        auth: {
            async resetPasswordForEmail(email, options) {
                calls.push({ email, options });
                return {
                    error: scenario.errorMessage === null
                        ? null
                        : { message: scenario.errorMessage },
                };
            },
        },
    };

    vm.runInThisContext(fs.readFileSync(sourcePath, 'utf8'), {
        filename: sourcePath,
    });

    (async () => {
        if (handler) {
            await handler({ preventDefault() { prevented = true; } });
        }
        process.stdout.write(JSON.stringify({
            calls,
            alerts,
            prevented,
            listenerRegistered: handler !== null,
        }));
    })().catch((error) => {
        console.error(error);
        process.exitCode = 1;
    });
"""


def run_forgot_password(
    email: str = "user@example.test",
    *,
    error_message: str | None = None,
    form_present: bool = True,
    email_input_present: bool = True,
) -> dict:
    return run_node_harness(
        FORGOT_PASSWORD_HARNESS,
        ROOT_DIR / "js" / "forgot-password.js",
        {
            "email": email,
            "errorMessage": error_message,
            "formPresent": form_present,
            "emailInputPresent": email_input_present,
            "locationHref": (
                "https://example.test/Web%20Ui/forgot-password.html?from=login"
            ),
        },
    )


@pytest.mark.skipif(NODE is None, reason="Node.js is required for JavaScript unit tests")
def test_forgot_password_submits_trimmed_email_with_page_relative_redirect():
    result = run_forgot_password("  user@example.test  ")

    assert result["prevented"] is True
    assert result["calls"] == [
        {
            "email": "user@example.test",
            "options": {
                "redirectTo": "https://example.test/Web%20Ui/reset_password.html"
            },
        }
    ]
    assert result["alerts"] == [
        "A password reset link has been sent to your email address."
    ]


@pytest.mark.skipif(NODE is None, reason="Node.js is required for JavaScript unit tests")
@pytest.mark.parametrize("email", ["", "  \n\t  "])
def test_forgot_password_rejects_blank_email_without_calling_supabase(email: str):
    result = run_forgot_password(email)

    assert result["prevented"] is True
    assert result["calls"] == []
    assert result["alerts"] == ["Please enter your email address."]


@pytest.mark.skipif(NODE is None, reason="Node.js is required for JavaScript unit tests")
def test_forgot_password_handles_missing_email_control_as_invalid_input():
    result = run_forgot_password(email_input_present=False)

    assert result["calls"] == []
    assert result["alerts"] == ["Please enter your email address."]


@pytest.mark.skipif(NODE is None, reason="Node.js is required for JavaScript unit tests")
def test_forgot_password_surfaces_supabase_error_without_success_message():
    result = run_forgot_password("failed@example.test", error_message="Rate limited")

    assert result["calls"][0]["email"] == "failed@example.test"
    assert result["alerts"] == ["Error sending reset link: Rate limited"]


@pytest.mark.skipif(NODE is None, reason="Node.js is required for JavaScript unit tests")
def test_forgot_password_is_safe_when_form_is_absent():
    result = run_forgot_password(form_present=False)

    assert result == {
        "calls": [],
        "alerts": [],
        "prevented": False,
        "listenerRegistered": False,
    }


ROUTER_HARNESS = r"""
    const fs = require('node:fs');
    const vm = require('node:vm');

    const sourcePath = process.argv[1];
    const appendedScripts = [];
    const removedScripts = [];
    const pushedStates = [];
    const dispatchedEvents = [];
    const currentShell = { innerHTML: '<main>old content</main>' };
    const newShell = { innerHTML: '<main>new content</main>' };
    const inlineSource = 'globalThis.inlineExecutions = '
        + '(globalThis.inlineExecutions || 0) + 1;';
    const inlineScript = {
        attributes: [],
        textContent: inlineSource,
        getAttribute() { return null; },
    };
    const parsedDocument = {
        title: 'Next page',
        querySelector(selector) {
            return selector === '.app-shell' ? newShell : null;
        },
        querySelectorAll(selector) {
            return selector === 'script' ? [inlineScript] : [];
        },
    };

    global.inlineExecutions = 0;
    global.fetch = async () => ({
        ok: true,
        async text() { return '<html>next page</html>'; },
    });
    global.DOMParser = class {
        parseFromString() { return parsedDocument; }
    };
    global.Event = class {
        constructor(type) { this.type = type; }
    };
    global.document = {
        title: 'Current page',
        body: {
            appendChild(script) {
                appendedScripts.push(script);
                if (script.textContent) vm.runInThisContext(script.textContent);
            },
            removeChild(script) { removedScripts.push(script); },
        },
        addEventListener() {},
        dispatchEvent(event) { dispatchedEvents.push(event.type); },
        querySelector(selector) {
            return selector === '.app-shell' ? currentShell : null;
        },
        querySelectorAll() { return []; },
        createElement() {
            return {
                textContent: '',
                setAttribute(name, value) { this[name] = value; },
            };
        },
    };
    global.window = {
        location: { pathname: '/Web Ui/current.html', href: '' },
        history: {
            pushState(state, title, url) {
                pushedStates.push({ state, title, url });
            },
        },
        addEventListener() {},
    };

    vm.runInThisContext(fs.readFileSync(sourcePath, 'utf8'), {
        filename: sourcePath,
    });

    (async () => {
        await window.AppRouter.loadPage('next.html');
        process.stdout.write(JSON.stringify({
            inlineExecutions: global.inlineExecutions,
            appendedScriptCount: appendedScripts.length,
            removedScriptCount: removedScripts.length,
            renderedHtml: currentShell.innerHTML,
            title: document.title,
            pushedStates,
            dispatchedEvents,
        }));
    })().catch((error) => {
        console.error(error);
        process.exitCode = 1;
    });
"""


@pytest.mark.skipif(NODE is None, reason="Node.js is required for JavaScript unit tests")
def test_router_executes_inline_script_through_a_transient_dom_node():
    router_path = ROOT_DIR / "js" / "router.js"
    result = run_node_harness(ROUTER_HARNESS, router_path)

    assert "new Function" not in router_path.read_text(encoding="utf-8")
    assert result["inlineExecutions"] == 1
    assert result["appendedScriptCount"] == 1
    assert result["removedScriptCount"] == 1
    assert result["renderedHtml"] == "<main>new content</main>"
    assert result["title"] == "Next page"
    assert result["pushedStates"] == [
        {
            "state": {"url": "next.html"},
            "title": "Next page",
            "url": "next.html",
        }
    ]
    assert result["dispatchedEvents"] == ["DOMContentLoaded"]
