document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.theme-btn');
  const html = document.documentElement;

  function setTheme(theme) {
    if (theme === 'auto') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      html.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
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

  const savedTheme = localStorage.getItem('lab-theme') || 'dark';
  setTheme(savedTheme);

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      setTheme(btn.dataset.themeVal);
    });
  });
});
