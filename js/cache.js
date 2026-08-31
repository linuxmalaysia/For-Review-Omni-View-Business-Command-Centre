/**
 * Session Cache Utility
 * Utility for storing and retrieving session-level cached data in sessionStorage.
 */
window.SessionCache = {
    /**
     * Get cached item from sessionStorage.
     * @param {string} key
     * @returns {any|null}
     */
    get(key) {
        try {
            const data = sessionStorage.getItem(`cache_${key}`);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.warn("SessionCache.get error:", e);
            return null;
        }
    },

    /**
     * Set cached item in sessionStorage.
     * @param {string} key
     * @param {any} value
     */
    set(key, value) {
        try {
            sessionStorage.setItem(`cache_${key}`, JSON.stringify(value));
        } catch (e) {
            console.warn("SessionCache.set error:", e);
        }
    },

    /**
     * Remove specific cached item from sessionStorage.
     * @param {string} key
     */
    remove(key) {
        try {
            sessionStorage.removeItem(`cache_${key}`);
        } catch (e) {
            console.warn("SessionCache.remove error:", e);
        }
    },

    /**
     * Clear all application session caches.
     */
    clearAll() {
        try {
            Object.keys(sessionStorage).forEach(key => {
                if (key.startsWith('cache_') || key.startsWith('page_html_')) {
                    sessionStorage.removeItem(key);
                }
            });
        } catch (e) {
            console.warn("SessionCache.clearAll error:", e);
        }
    }
};
