// State
let apiKeys = [];
let currentKeyIndex = 0;
let currentGeneratedHtml = ''; // Store generated HTML

// DOM Elements
const inputPasteCode = document.getElementById('inputPasteCode');
const previewBody = document.getElementById('preview-body');
const generateBtn = document.getElementById('generateBtn');
const checkHtmlBtn = document.getElementById('checkHtmlBtn');
const styleSelect = document.getElementById('styleSelect');
const toggleThemeBtn = document.getElementById('toggleThemeBtn');
const themeIconSun = document.getElementById('themeIconSun');
const themeIconMoon = document.getElementById('themeIconMoon');

// Load saved theme or default to dracula
const savedTheme = localStorage.getItem('editorTheme') || 'dracula';
updateThemeIcon(savedTheme);

// Initialize CodeMirror
const editor = CodeMirror.fromTextArea(inputPasteCode, {
    mode: "htmlmixed",
    theme: savedTheme,
    lineNumbers: true,
    lineWrapping: true,
    viewportMargin: Infinity
});

// Theme Toggle Logic
toggleThemeBtn.addEventListener('click', () => {
    const currentTheme = editor.getOption('theme');
    const newTheme = currentTheme === 'dracula' ? 'eclipse' : 'dracula';

    editor.setOption('theme', newTheme);
    localStorage.setItem('editorTheme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    if (theme === 'dracula') {
        themeIconSun.style.display = 'block';
        themeIconMoon.style.display = 'none';
    } else {
        themeIconSun.style.display = 'none';
        themeIconMoon.style.display = 'block';
    }
}

// Sync CodeMirror changes to textarea (optional, but good for form submission if needed)
editor.on('change', () => {
    editor.save();
});
const apiKeyInput = document.getElementById('apiKeyInput');
const copyHtmlBtn = document.getElementById('copyHtmlBtn');
const toggleApiKeyBtn = document.getElementById('toggleApiKey');
const apiKeyModal = document.getElementById('apiKeyModal');
const closeModalBtn = document.getElementById('closeModal');
const saveApiKeysBtn = document.getElementById('saveApiKeys');
const clearApiKeysBtn = document.getElementById('clearApiKeys');
const apiKeyCount = document.getElementById('apiKeyCount');

// Event Listener

// API Key Management
function loadApiKeys() {
    const savedKeys = localStorage.getItem('gemini_api_keys');
    if (savedKeys) {
        apiKeys = savedKeys.split('\n').filter(key => key.trim() !== '');
    }

    // Fallback/Default to User's Key if no keys found
    if (apiKeys.length === 0) {
        const defaultKey = "AIzaSyAuMHWCs216ym-Y6J1ihK4ZBwUfdJf7Q_o";
        apiKeys = [defaultKey];
        // Optional: Save it to localStorage so it persists
        localStorage.setItem('gemini_api_keys', defaultKey);
    }

    apiKeyInput.value = apiKeys.join('\n');
    updateApiKeyCount();
}

function saveApiKeys() {
    const keys = apiKeyInput.value.split('\n').filter(key => key.trim() !== '');
    apiKeys = keys;
    localStorage.setItem('gemini_api_keys', keys.join('\n'));
    updateApiKeyCount();
}

function clearApiKeys() {
    if (confirm('Hapus semua API keys?')) {
        apiKeys = [];
        apiKeyInput.value = '';
        localStorage.removeItem('gemini_api_keys');
        currentKeyIndex = 0;
        updateApiKeyCount();
    }
}

function updateApiKeyCount() {
    apiKeyCount.textContent = `${apiKeys.length} API Key${apiKeys.length !== 1 ? 's' : ''}`;
}

function getNextApiKey() {
    if (apiKeys.length === 0) return '';
    const key = apiKeys[currentKeyIndex];
    currentKeyIndex = (currentKeyIndex + 1) % apiKeys.length;
    return key;
}

// Modal Management
toggleApiKeyBtn.addEventListener('click', () => {
    apiKeyModal.style.display = 'block';
});

closeModalBtn.addEventListener('click', () => {
    apiKeyModal.style.display = 'none';
});

apiKeyModal.addEventListener('click', (e) => {
    if (e.target === apiKeyModal) {
        apiKeyModal.style.display = 'none';
    }
});

// Auto-save on input
apiKeyInput.addEventListener('input', () => {
    saveApiKeys();
});

saveApiKeysBtn.addEventListener('click', () => {
    saveApiKeys();
    apiKeyModal.style.display = 'none';
    alert(`✅ ${apiKeys.length} API key(s) berhasil disimpan!`);
});

clearApiKeysBtn.addEventListener('click', clearApiKeys);

// Hardcode theme to premium (no selection needed) - REMOVED
// let currentTheme = 'premium';

// UI Helper Functions
function showError(message) {
    alert(message); // Simple alert for now, can be improved later
}

function hideError() {
    // No-op for now as we use alert
}

function showLoading(isLoading) {
    if (isLoading) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span>⏳</span> Generating...';
    } else {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<span>⚡</span> Generate'; // Restore original text
    }
}

// Generate Function with Retry Logic
async function generateRedesign() {
    const htmlInput = inputPasteCode.value;
    const originalBtnText = generateBtn.innerHTML; // Store original text

    if (!htmlInput.trim()) {
        alert('Silakan tempel kode HTML terlebih dahulu!');
        return;
    }

    console.log('=== GENERATE START ===');
    console.log('API Keys available:', apiKeys.length);

    // Show loading state
    showLoading(true);

    // Progress Bar HTML
    previewBody.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 40px; text-align: center;">
            <div style="width: 100%; max-width: 300px; background: #e2e8f0; border-radius: 10px; height: 10px; overflow: hidden; margin-bottom: 15px;">
                <div id="progressBarPreview" style="width: 0%; height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.3s ease;"></div>
            </div>
            <p id="progressTextPreview" style="color: #4a5568; font-weight: 600; font-size: 16px; margin-bottom: 5px;">0%</p>
            <p style="color: #718096; font-size: 14px;">Sedang menganalisis & redesign dengan AI...</p>
        </div>
    `;

    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        if (progress < 90) {
            // Random increment between 1 and 5
            const increment = Math.floor(Math.random() * 5) + 1;
            progress = Math.min(progress + increment, 90);

            const progressBar = document.getElementById('progressBarPreview');
            const progressText = document.getElementById('progressTextPreview');

            if (progressBar && progressText) {
                progressBar.style.width = `${progress}%`;
                progressText.textContent = `${progress}%`;
            }
        }
    }, 200);

    let retryCount = 0;
    const maxRetries = apiKeys.length > 0 ? apiKeys.length : 1;

    async function tryGenerate(key) {
        console.log('=== TRYING GENERATE ===');
        console.log('API Key:', key ? 'YES (length: ' + key.length + ')' : 'NO');

        try {
            const apiKey = key;
            const style = styleSelect.value;
            const customPrompt = document.getElementById('customStylePrompt').value;
            const rewriteCopywriting = document.getElementById('rewriteCopywriting').checked;

            const referenceUrl = document.getElementById('referenceUrl').value;

            if (!apiKey) {
                showError('API Key belum diisi! Klik icon gear di pojok kanan atas.');
                return false;
            }

            if (style === 'custom' && !customPrompt.trim() && !referenceUrl) {
                showError('Silakan isi deskripsi style custom Anda atau masukkan link referensi!');
                return false;
            }

            showLoading(true);
            hideError();

            const requestBody = {
                html: htmlInput,
                api_key: apiKey,
                style: style,
                custom_prompt: customPrompt,
                rewrite_copywriting: rewriteCopywriting,
                reference_url: referenceUrl
            };

            console.log('Request body prepared. Sending fetch request...');

            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            console.log('Fetch response received. Status:', response.status);

            const result = await response.json();

            if (response.ok) {
                // Complete progress bar
                clearInterval(progressInterval);
                const progressBar = document.getElementById('progressBarPreview');
                const progressText = document.getElementById('progressTextPreview');
                if (progressBar && progressText) {
                    progressBar.style.width = '100%';
                    progressText.textContent = '100%';
                    progressText.style.color = '#38ef7d';
                }

                await new Promise(resolve => setTimeout(resolve, 500));
                console.log('✓ Generation successful');

                currentGeneratedHtml = result.html;
                if (copyHtmlBtn) copyHtmlBtn.classList.remove('hidden');

                // Save to history
                saveToHistory(result.html, style, customPrompt);

                // CRITICAL FIX: Restore iframe element (it was destroyed by progress HTML)
                previewBody.innerHTML = `
                    <iframe id="previewFrame" class="bg-white shadow-xl rounded-[35px] border-[8px] border-gray-800"
                        style="width: 375px; height: 95%;" sandbox="allow-scripts allow-same-origin"></iframe>
                `;

                // Wait for iframe to be ready
                await new Promise(resolve => setTimeout(resolve, 100));

                // Update preview using document.write (Robust method)
                const iframe = document.getElementById('previewFrame');
                if (iframe) {
                    const doc = iframe.contentDocument || iframe.contentWindow.document;
                    doc.open();
                    doc.write(result.html);
                    doc.close();
                    injectPreviewScript(doc);
                } else {
                    console.error('❌ Iframe not found after restoration!');
                }

                generateBtn.disabled = false;
                generateBtn.innerHTML = originalBtnText;

                return true;
            } else {
                showError(result.error || 'Terjadi kesalahan saat generate landing page.');
                return false;
            }

        } catch (error) {
            clearInterval(progressInterval);
            console.error('✗ FETCH ERROR:', error);
            showError('Error: ' + error.message + '\n\nCek console browser untuk detail.');
            return false;
        } finally {
            showLoading(false);
        }
    }

    // Try with each API key in rotation
    while (retryCount < maxRetries) {
        const apiKey = getNextApiKey();
        const success = await tryGenerate(apiKey);
        if (success) return;

        retryCount++;
        if (retryCount < maxRetries) {
            console.log(`Retrying with next API key (${retryCount}/${maxRetries})...`);
        }
    }

    // Restore button on error
    generateBtn.disabled = false;
    generateBtn.innerHTML = originalBtnText;

    alert('Terjadi kesalahan saat generate. Silakan coba lagi atau periksa API keys Anda.');
}

// Event Listeners
generateBtn.addEventListener('click', generateRedesign);

checkHtmlBtn.addEventListener('click', () => {
    const htmlInput = inputPasteCode.value;
    if (!htmlInput.trim()) {
        alert('Silakan tempel kode HTML terlebih dahulu!');
        return;
    }

    // Update preview
    const iframe = document.createElement('iframe');
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';

    previewBody.innerHTML = '';
    previewBody.appendChild(iframe);

    iframe.contentDocument.open();
    iframe.contentDocument.write(htmlInput);
    iframe.contentDocument.close();

    injectPreviewScript(iframe.contentDocument);
});

// --- Click-to-Locate Logic ---
function injectPreviewScript(doc) {
    if (!doc || !doc.body) {
        console.warn('Cannot inject preview script: doc.body is null');
        return;
    }

    const script = doc.createElement('script');
    script.textContent = `
        document.body.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            let text = e.target.innerText || e.target.textContent;
            if (text) {
                text = text.trim();
                if (text.length > 50) text = text.substring(0, 50); // Limit length
                if (text) {
                    window.parent.handlePreviewClick(text);
                }
            }
        }, true);
        
        // Add cursor pointer to all elements to indicate clickable
        const style = document.createElement('style');
        style.textContent = '* { cursor: pointer !important; }';
        if (document.head) {
            document.head.appendChild(style);
        } else if (document.body) {
            document.body.appendChild(style);
        }
    `;
    doc.body.appendChild(script);
}

window.handlePreviewClick = function (text) {
    if (!text) return;

    // Show search bar if hidden
    if (searchBar.style.display === 'none') {
        searchBar.style.display = 'flex';
    }

    searchInput.value = text;
    performSearch(); // This function already uses editor.getSearchCursor and scrollToMatch (which uses editor.scrollIntoView)
}

// Copy HTML Button Logic
// copyHtmlBtn is already declared at the top
if (copyHtmlBtn) {
    copyHtmlBtn.addEventListener('click', () => {
        if (currentGeneratedHtml) {
            navigator.clipboard.writeText(currentGeneratedHtml).then(() => {
                const originalText = copyHtmlBtn.innerHTML;
                copyHtmlBtn.innerHTML = '<i class="fas fa-check mr-2"></i> Copied!';
                copyHtmlBtn.classList.remove('bg-green-500', 'hover:bg-green-600');
                copyHtmlBtn.classList.add('bg-gray-500', 'hover:bg-gray-600');

                setTimeout(() => {
                    copyHtmlBtn.innerHTML = originalText;
                    copyHtmlBtn.classList.add('bg-green-500', 'hover:bg-green-600');
                    copyHtmlBtn.classList.remove('bg-gray-500', 'hover:bg-gray-600');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
                alert('Gagal menyalin kode. Silakan coba manual.');
            });
        }
    });
}


// Toggle Custom Style Input
styleSelect.addEventListener('change', () => {
    const customContainer = document.getElementById('customStyleContainer');
    if (styleSelect.value === 'custom') {
        customContainer.classList.remove('hidden');
    } else {
        customContainer.classList.add('hidden');
    }
});

// Auto-switch to Reference Style when URL is entered
const referenceUrlInput = document.getElementById('referenceUrl');
referenceUrlInput.addEventListener('input', () => {
    if (referenceUrlInput.value.trim() !== '') {
        styleSelect.value = 'reference_style';
        // Trigger change event to handle custom container visibility
        styleSelect.dispatchEvent(new Event('change'));
    }
});

// ===== HISTORY SYSTEM =====
const HISTORY_KEY = 'lp_history';
const MAX_HISTORY = 5;

// Toggle History Panel
const toggleHistoryBtn = document.getElementById('toggleHistoryBtn');
const historyPanel = document.getElementById('historyPanel');
const closeHistoryBtn = document.getElementById('closeHistoryBtn');

toggleHistoryBtn.addEventListener('click', () => {
    historyPanel.style.right = '0';
    loadHistory();
});

closeHistoryBtn.addEventListener('click', () => {
    historyPanel.style.right = '-400px';
});

// Save to History
function saveToHistory(html, style, customPrompt) {
    const history = getHistory();
    const newItem = {
        id: Date.now(),
        html: html,
        style: style,
        customPrompt: customPrompt || null,
        timestamp: Date.now()
    };

    history.unshift(newItem); // Add to beginning

    // Keep only last 5
    if (history.length > MAX_HISTORY) {
        history.pop();
    }

    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    console.log('✓ Saved to history:', newItem.id);
}

// Get History
function getHistory() {
    const stored = localStorage.getItem(HISTORY_KEY);
    return stored ? JSON.parse(stored) : [];
}

// Load and Display History
function loadHistory() {
    const history = getHistory();
    const historyList = document.getElementById('historyList');

    if (history.length === 0) {
        historyList.innerHTML = `
            <div style="text-align: center; padding: 40px 20px; color: #718096;">
                <svg xmlns="http://www.w3.org/2000/svg" style="width: 48px; height: 48px; margin: 0 auto 15px; opacity: 0.5;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p style="margin: 0; font-size: 14px;">No history yet</p>
                <p style="margin: 5px 0 0; font-size: 12px; opacity: 0.7;">Generate a design to start</p>
            </div>
        `;
        return;
    }

    historyList.innerHTML = history.map(item => {
        const date = new Date(item.timestamp);
        const timeStr = date.toLocaleString('id-ID', {
            day: '2-digit',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit'
        });

        const styleLabel = item.style === 'custom'
            ? `Custom: ${(item.customPrompt || '').substring(0, 30)}...`
            : item.style.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());

        const preview = item.html.substring(0, 100).replace(/</g, '&lt;').replace(/>/g, '&gt;');

        return `
            <div style="background: #2d3748; border-radius: 8px; padding: 12px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                    <div>
                        <div style="font-size: 11px; color: #a0aec0; margin-bottom: 4px;">${timeStr}</div>
                        <div style="font-size: 13px; color: #ffffff; font-weight: 600;">${styleLabel}</div>
                    </div>
                    <button onclick="restoreHistory(${item.id})" style="background: #4299e1; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 11px; cursor: pointer; font-weight: 600;">
                        Restore
                    </button>
                </div>
                <div style="font-size: 11px; color: #718096; font-family: 'Fira Code', monospace; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    ${preview}...
                </div>
            </div>
        `;
    }).join('');
}

// Restore History Item
window.restoreHistory = function (id) {
    const history = getHistory();
    const item = history.find(h => h.id === id);

    if (!item) {
        alert('History item not found!');
        return;
    }

    // Update preview
    currentGeneratedHtml = item.html;
    const iframe = document.getElementById('previewFrame');
    if (iframe) {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        doc.open();
        doc.write(item.html);
        doc.close();
        injectPreviewScript(doc);
    }

    // Show copy button
    if (copyHtmlBtn) copyHtmlBtn.classList.remove('hidden');

    // Close history panel
    historyPanel.style.right = '-400px';

    console.log('✓ Restored history item:', id);
};

// Clear All History
document.getElementById('clearHistoryBtn').addEventListener('click', () => {
    if (confirm('Are you sure you want to clear all history?')) {
        localStorage.removeItem(HISTORY_KEY);
        loadHistory();
        console.log('✓ History cleared');
    }
});

// Hook into existing generate function to save history
// We'll modify the tryGenerate function to call saveToHistory after success

// Toggle Card Function
window.toggleCard = function (header) {
    const card = header.parentElement;
    const icon = header.querySelector('.chevron-icon');

    card.classList.toggle('collapsed');

    // Rotate icon logic is handled by CSS based on .collapsed class
    // But if we want to be explicit or if CSS rotation isn't enough:
    if (card.classList.contains('collapsed')) {
        icon.classList.add('-rotate-90');
    } else {
        icon.classList.remove('-rotate-90');
    }
};

// Initialize
loadApiKeys();
