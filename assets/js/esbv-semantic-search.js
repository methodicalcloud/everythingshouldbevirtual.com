/**
 * ESBV Semantic Search Widget
 *
 * Drop-in JavaScript widget for semantic search powered by Methodical Cloud AI/ML.
 * Usage: <div id="esbv-semantic-search"></div>
 */

(function() {
    'use strict';

    // Configuration
    const API_URL = 'http://localhost:8000/products/esbv/search'; // Will update to production URL after deployment

    // Initialize widget
    function init() {
        const container = document.getElementById('esbv-semantic-search');
        if (!container) {
            console.warn('ESBV Semantic Search: Container not found (#esbv-semantic-search)');
            return;
        }

        render(container);
        attachEventListeners(container);
    }

    // Render search UI
    function render(container) {
        container.innerHTML = `
            <div class="esbv-search-widget">
                <div class="search-box">
                    <input
                        type="text"
                        id="esbv-search-input"
                        class="search-input"
                        placeholder="Ask anything... (e.g., 'How do I set up Docker networking?')"
                        autocomplete="off"
                    />
                    <button id="esbv-search-button" class="search-button">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
                        </svg>
                        Search
                    </button>
                </div>
                <div id="esbv-search-results" class="search-results"></div>
            </div>
        `;

        // Add styles
        addStyles();
    }

    // Add CSS styles
    function addStyles() {
        if (document.getElementById('esbv-search-styles')) return;

        const styles = document.createElement('style');
        styles.id = 'esbv-search-styles';
        styles.textContent = `
            .esbv-search-widget {
                margin: 20px 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            }

            .search-box {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }

            .search-input {
                flex: 1;
                padding: 12px 16px;
                font-size: 16px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                outline: none;
                transition: border-color 0.3s;
            }

            .search-input:focus {
                border-color: #667eea;
            }

            .search-button {
                padding: 12px 24px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: background 0.3s;
            }

            .search-button:hover {
                background: #5568d3;
            }

            .search-button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }

            .search-results {
                display: none;
            }

            .search-results.visible {
                display: block;
            }

            .search-result {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 15px;
                transition: box-shadow 0.3s;
            }

            .search-result:hover {
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }

            .result-title {
                font-size: 1.3em;
                font-weight: 600;
                margin-bottom: 8px;
            }

            .result-title a {
                color: #667eea;
                text-decoration: none;
            }

            .result-title a:hover {
                text-decoration: underline;
            }

            .result-meta {
                font-size: 0.9em;
                color: #666;
                margin-bottom: 10px;
            }

            .result-score {
                display: inline-block;
                background: #e8f4f8;
                color: #0077b6;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.85em;
                font-weight: 600;
                margin-left: 10px;
            }

            .result-excerpt {
                color: #333;
                line-height: 1.6;
            }

            .result-tags {
                margin-top: 10px;
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
            }

            .result-tag {
                background: #f0f0f0;
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 0.8em;
                color: #555;
            }

            .search-loading {
                text-align: center;
                padding: 40px;
                color: #666;
            }

            .search-error {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                border-radius: 4px;
                color: #856404;
            }

            .no-results {
                text-align: center;
                padding: 40px;
                color: #666;
            }
        `;
        document.head.appendChild(styles);
    }

    // Attach event listeners
    function attachEventListeners(container) {
        const input = container.querySelector('#esbv-search-input');
        const button = container.querySelector('#esbv-search-button');

        button.addEventListener('click', () => performSearch(container));

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch(container);
            }
        });
    }

    // Perform semantic search
    async function performSearch(container) {
        const input = container.querySelector('#esbv-search-input');
        const resultsContainer = container.querySelector('#esbv-search-results');
        const button = container.querySelector('#esbv-search-button');

        const query = input.value.trim();

        if (!query) {
            resultsContainer.classList.remove('visible');
            return;
        }

        // Show loading state
        button.disabled = true;
        resultsContainer.classList.add('visible');
        resultsContainer.innerHTML = '<div class="search-loading">🔍 Searching 327 posts...</div>';

        try {
            // Note: This requires posts data. In production, posts would be cached or retrieved from API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    posts: [], // TODO: Load posts from Jekyll site or API
                    top_k: 5,
                    min_similarity: 0.3
                })
            });

            if (!response.ok) {
                throw new Error(`Search failed: ${response.statusText}`);
            }

            const data = await response.json();
            renderResults(resultsContainer, data);

        } catch (error) {
            console.error('Search error:', error);
            resultsContainer.innerHTML = `
                <div class="search-error">
                    <strong>Search Error</strong><br>
                    ${error.message}<br>
                    <small>Make sure the AI/ML service is running on ${API_URL}</small>
                </div>
            `;
        } finally {
            button.disabled = false;
        }
    }

    // Render search results
    function renderResults(container, data) {
        if (!data.results || data.results.length === 0) {
            container.innerHTML = '<div class="no-results">No results found. Try a different search term.</div>';
            return;
        }

        const resultsHTML = data.results.map(result => `
            <div class="search-result">
                <div class="result-title">
                    <a href="/${result.post.slug}/">${result.post.title}</a>
                    <span class="result-score">${(result.similarity_score * 100).toFixed(0)}% match</span>
                </div>
                <div class="result-meta">
                    ${new Date(result.post.date).toLocaleDateString()} · ${result.post.word_count || 0} words
                    ${result.match_explanation ? `· ${result.match_explanation}` : ''}
                </div>
                <div class="result-excerpt">${result.excerpt}</div>
                ${result.post.tags && result.post.tags.length > 0 ? `
                    <div class="result-tags">
                        ${result.post.tags.map(tag => `<span class="result-tag">${tag}</span>`).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');

        container.innerHTML = `
            <div style="margin-bottom: 15px; color: #666;">
                Found ${data.results.length} relevant posts in ${data.search_time_ms.toFixed(0)}ms
            </div>
            ${resultsHTML}
        `;
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
