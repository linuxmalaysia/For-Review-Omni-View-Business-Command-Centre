/**
 * Client-Side Router for Omni-View Command Centre
 * Handles dynamic navigation without full reloads, caches HTML/data in sessionStorage,
 * and re-initializes page scripts dynamically.
 */
(function () {
    // Intercept click on links
    document.addEventListener('click', function (event) {
        const anchor = event.target.closest('a');
        if (!anchor) return;

        // Bypass router interception for modifier keys or download links
        if (event.ctrlKey || event.metaKey || event.shiftKey || anchor.hasAttribute('download')) {
            return;
        }

        const href = anchor.getAttribute('href');
        if (!href || href === '#' || href.startsWith('javascript:') || href.startsWith('http://') || href.startsWith('https://') || anchor.getAttribute('target') === '_blank') {
            return;
        }

        // Avoid intercepting if link has onclick handler like logout
        if (anchor.hasAttribute('onclick') && anchor.getAttribute('onclick').includes('logout')) {
            return;
        }

        event.preventDefault();
        navigateTo(href);
    });

    // Handle browser back/forward buttons
    window.addEventListener('popstate', function (event) {
        if (event.state && event.state.url) {
            loadPage(event.state.url, false);
        } else {
            const currentPath = window.location.pathname.split('/').pop() || 'index.html';
            loadPage(currentPath, false);
        }
    });

    /**
     * Navigate to a target URL seamlessly.
     * @param {string} url
     */
    function navigateTo(url) {
        if (window.location.pathname.endsWith(url)) return;
        loadPage(url, true);
    }

    /**
     * Load page via AJAX/Fetch, cache in sessionStorage, and replace container.
     * @param {string} url
     * @param {boolean} pushState
     */
    async function loadPage(url, pushState = true) {
        const targetUrl = url;
        const cacheKey = `page_html_${targetUrl}`;

        try {
            let htmlContent = window.SessionCache ? window.SessionCache.get(cacheKey) : null;

            if (!htmlContent) {
                const response = await fetch(targetUrl);
                if (!response.ok) {
                    window.location.href = targetUrl; // Fallback to traditional navigation
                    return;
                }
                htmlContent = await response.text();
                if (window.SessionCache) {
                    window.SessionCache.set(cacheKey, htmlContent);
                }
            }

            const parser = new DOMParser();
            const doc = parser.parseFromString(htmlContent, 'text/html');

            const newMain = doc.querySelector('.app-shell') || doc.querySelector('body');
            const currentMain = document.querySelector('.app-shell') || document.querySelector('body');

            if (newMain && currentMain) {
                // Update page title
                if (doc.title) {
                    document.title = doc.title;
                }

                // Replace shell content
                currentMain.innerHTML = newMain.innerHTML;

                if (pushState) {
                    window.history.pushState({ url: targetUrl }, doc.title, targetUrl);
                }

                // Execute new page scripts if not already present
                await loadNewScripts(doc);

                // Re-execute page lifecycle triggers
                reinitializeScripts();
            } else {
                window.location.href = targetUrl;
            }
        } catch (err) {
            console.error('Routing failed, falling back to page reload:', err);
            window.location.href = targetUrl;
        }
    }

    /**
     * Load new external scripts present in the target HTML document that are not yet loaded.
     * @param {Document} newDoc
     */
    async function loadNewScripts(newDoc) {
        const existingScriptSrcs = new Set(
            Array.from(document.querySelectorAll('script[src]')).map(s => s.getAttribute('src'))
        );

        const scripts = Array.from(newDoc.querySelectorAll('script'));

        for (const oldScript of scripts) {
            const src = oldScript.getAttribute('src');

            // Skip script if already loaded in the document
            if (src && existingScriptSrcs.has(src)) {
                continue;
            }

            const newScript = document.createElement('script');

            Array.from(oldScript.attributes).forEach(attr => {
                newScript.setAttribute(attr.name, attr.value);
            });

            if (src) {
                existingScriptSrcs.add(src);
                await new Promise((resolve) => {
                    newScript.onload = resolve;
                    newScript.onerror = () => {
                        console.warn(`Failed to load script: ${src}`);
                        resolve();
                    };
                    document.body.appendChild(newScript);
                });
            }
        }
    }

    /**
     * Re-execute page lifecycle triggers after navigation.
     */
    function reinitializeScripts() {
        const domContentLoadedEvent = new Event('DOMContentLoaded', {
            bubbles: true,
            cancelable: true
        });
        document.dispatchEvent(domContentLoadedEvent);
    }

    window.AppRouter = {
        navigateTo: navigateTo,
        loadPage: loadPage
    };
})();
