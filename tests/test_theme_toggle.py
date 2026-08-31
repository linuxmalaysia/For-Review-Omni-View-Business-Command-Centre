import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]
THEME_SCRIPT = ROOT_DIR / "assets" / "js" / "theme-toggle.js"
NODE = shutil.which("node")

NODE_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const options = JSON.parse(process.argv[1]);
const source = fs.readFileSync(process.argv[2], 'utf8');
const documentListeners = {};
const mediaListeners = {};
const stored = new Map();
if (options.savedTheme !== null) stored.set('lab-theme', options.savedTheme);

function makeButton(theme) {
  const classes = new Set(theme === 'dark' ? ['active'] : []);
  const listeners = {};
  return {
    dataset: {themeVal: theme},
    classList: {
      add(value) { classes.add(value); },
      remove(value) { classes.delete(value); },
      contains(value) { return classes.has(value); }
    },
    addEventListener(type, callback) { listeners[type] = callback; },
    click() { listeners.click(); }
  };
}

const buttons = ['light', 'dark', 'auto'].map(makeButton);
const html = {
  theme: null,
  setAttribute(name, value) {
    if (name === 'data-theme') this.theme = value;
  }
};
const mediaQuery = {
  matches: options.prefersDark,
  addEventListener(type, callback) { mediaListeners[type] = callback; }
};

global.document = {
  documentElement: html,
  querySelectorAll(selector) {
    if (selector !== '.theme-btn') throw new Error(`unexpected selector: ${selector}`);
    return buttons;
  },
  addEventListener(type, callback) { documentListeners[type] = callback; }
};
global.window = {
  matchMedia(query) {
    if (query !== '(prefers-color-scheme: dark)') throw new Error(`unexpected query: ${query}`);
    return mediaQuery;
  }
};
global.localStorage = {
  getItem(key) { return stored.has(key) ? stored.get(key) : null; },
  setItem(key, value) { stored.set(key, value); }
};

vm.runInThisContext(source, {filename: process.argv[2]});
documentListeners.DOMContentLoaded();

for (const action of options.actions) {
  if (action.type === 'click') {
    buttons.find(button => button.dataset.themeVal === action.theme).click();
  } else if (action.type === 'system-change') {
    mediaQuery.matches = action.matches;
    mediaListeners.change({matches: action.matches});
  }
}

process.stdout.write(JSON.stringify({
  renderedTheme: html.theme,
  savedTheme: stored.get('lab-theme'),
  activeThemes: buttons
    .filter(button => button.classList.contains('active'))
    .map(button => button.dataset.themeVal)
}));
"""


def run_theme_toggle(*, saved_theme=None, prefers_dark=False, actions=()):
    if NODE is None:
        pytest.skip("Node.js is required to execute the theme controller")

    options = {
        "savedTheme": saved_theme,
        "prefersDark": prefers_dark,
        "actions": list(actions),
    }
    result = subprocess.run(
        [NODE, "-e", NODE_HARNESS, json.dumps(options), str(THEME_SCRIPT)],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return json.loads(result.stdout)


def test_defaults_to_dark_and_persists_the_default():
    state = run_theme_toggle()

    assert state == {
        "renderedTheme": "dark",
        "savedTheme": "dark",
        "activeThemes": ["dark"],
    }


@pytest.mark.parametrize(
    ("prefers_dark", "expected_rendered"),
    [(False, "light"), (True, "dark")],
)
def test_auto_theme_uses_system_preference_and_marks_auto_active(prefers_dark, expected_rendered):
    state = run_theme_toggle(saved_theme="auto", prefers_dark=prefers_dark)

    assert state["renderedTheme"] == expected_rendered
    assert state["savedTheme"] == "auto"
    assert state["activeThemes"] == ["auto"]


def test_clicking_a_theme_updates_dom_storage_and_active_button():
    state = run_theme_toggle(
        saved_theme="dark",
        actions=[{"type": "click", "theme": "light"}],
    )

    assert state == {
        "renderedTheme": "light",
        "savedTheme": "light",
        "activeThemes": ["light"],
    }

def test_system_change_updates_auto_theme_without_overwriting_preference():
    state = run_theme_toggle(
        saved_theme="auto",
        prefers_dark=False,
        actions=[{"type": "system-change", "matches": True}],
    )

    assert state == {
        "renderedTheme": "dark",
        "savedTheme": "auto",
        "activeThemes": ["auto"],
    }


def test_system_change_is_ignored_for_an_explicit_theme():
    state = run_theme_toggle(
        saved_theme="light",
        prefers_dark=False,
        actions=[{"type": "system-change", "matches": True}],
    )

    assert state == {
        "renderedTheme": "light",
        "savedTheme": "light",
        "activeThemes": ["light"],
    }
