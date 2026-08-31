document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.theme-btn');
  const html = document.documentElement;
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

  /**
   * Applies a theme preference, updates the active theme control, and persists the selection.
   * @param {string} theme - The theme preference to apply: `light`, `dark`, or `auto`.
   */
  function setTheme(theme) {
    if (theme === 'auto') {
      html.setAttribute('data-theme', mediaQuery.matches ? 'dark' : 'light');
    } else {
      html.setAttribute('data-theme', theme);
    }

    buttons.forEach(btn => {
      if (btn.dataset.themeVal === theme) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    localStorage.setItem('lab-theme', theme);
  }

  // Register listener for system color scheme preference changes
  mediaQuery.addEventListener('change', (e) => {
    if (localStorage.getItem('lab-theme') === 'auto') {
      html.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    }
  });

  const savedTheme = localStorage.getItem('lab-theme') || 'dark';
  setTheme(savedTheme);

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      setTheme(btn.dataset.themeVal);
    });
  });
});
