import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")

THEME_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const sourcePath = process.argv[1];
const scenario = JSON.parse(process.argv[2]);
let onReady;
let onPreferenceChange;
let selectedTheme;

class ClassList {
  constructor(active) {
    this.values = new Set(active ? ['active'] : []);
  }
  add(value) { this.values.add(value); }
  remove(value) { this.values.delete(value); }
  contains(value) { return this.values.has(value); }
}

const buttons = ['light', 'dark', 'auto'].map(theme => ({
  dataset: { themeVal: theme },
  classList: new ClassList(theme === 'dark'),
  addEventListener(event, callback) {
    if (event === 'click') this.onClick = callback;
  }
}));
const storage = new Map(Object.entries(scenario.storage || {}));
const context = {
  document: {
    documentElement: {
      setAttribute(name, value) {
        if (name === 'data-theme') selectedTheme = value;
      }
    },
    addEventListener(event, callback) {
      if (event === 'DOMContentLoaded') onReady = callback;
    },
    querySelectorAll(selector) {
      if (selector !== '.theme-btn') throw new Error(`Unexpected selector: ${selector}`);
      return buttons;
    }
  },
  window: {
    matchMedia(query) {
      if (query !== '(prefers-color-scheme: dark)') throw new Error(`Unexpected query: ${query}`);
      return {
        matches: scenario.prefersDark,
        addEventListener(event, callback) {
          if (event === 'change') onPreferenceChange = callback;
        }
      };
    }
  },
  localStorage: {
    getItem(key) { return storage.has(key) ? storage.get(key) : null; },
    setItem(key, value) { storage.set(key, value); }
  }
};

vm.runInNewContext(fs.readFileSync(sourcePath, 'utf8'), context);
onReady();
if (scenario.click) {
  buttons.find(button => button.dataset.themeVal === scenario.click).onClick();
}
if (typeof scenario.preferenceChange === 'boolean') {
  onPreferenceChange({ matches: scenario.preferenceChange });
}

process.stdout.write(JSON.stringify({
  selectedTheme,
  storedTheme: storage.get('lab-theme'),
  activeTheme: buttons.find(button => button.classList.contains('active')).dataset.themeVal
}));
"""


def run_theme_scenario(scenario: dict) -> dict:
    completed = subprocess.run(
        [
            NODE,
            "-e",
            THEME_HARNESS,
            str(ROOT_DIR / "assets" / "js" / "theme-toggle.js"),
            json.dumps(scenario),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return json.loads(completed.stdout)


pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is required to execute theme-toggle.js")


def test_theme_defaults_to_dark_and_persists_the_default():
    result = run_theme_scenario({"prefersDark": False})

    assert result == {
        "selectedTheme": "dark",
        "storedTheme": "dark",
        "activeTheme": "dark",
    }


@pytest.mark.parametrize(
    ("prefers_dark", "expected_theme"),
    [(True, "dark"), (False, "light")],
)
def test_saved_auto_theme_follows_current_system_preference(prefers_dark, expected_theme):
    result = run_theme_scenario(
        {"prefersDark": prefers_dark, "storage": {"lab-theme": "auto"}}
    )

    assert result["selectedTheme"] == expected_theme
    assert result["storedTheme"] == "auto"
    assert result["activeTheme"] == "auto"


def test_clicking_a_theme_updates_dom_selection_and_storage():
    result = run_theme_scenario({"prefersDark": True, "click": "light"})

    assert result == {
        "selectedTheme": "light",
        "storedTheme": "light",
        "activeTheme": "light",
    }


def test_system_preference_change_updates_an_auto_theme():
    result = run_theme_scenario(
        {
            "prefersDark": False,
            "storage": {"lab-theme": "auto"},
            "preferenceChange": True,
        }
    )

    assert result["selectedTheme"] == "dark"
    assert result["storedTheme"] == "auto"
    assert result["activeTheme"] == "auto"


def test_system_preference_change_does_not_override_an_explicit_theme():
    result = run_theme_scenario(
        {
            "prefersDark": False,
            "storage": {"lab-theme": "light"},
            "preferenceChange": True,
        }
    )

    assert result["selectedTheme"] == "light"
    assert result["storedTheme"] == "light"
    assert result["activeTheme"] == "light"
