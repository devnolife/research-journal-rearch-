// CBF Calculation Functions
// Fitur untuk menampilkan detail perhitungan TF-IDF dan Cosine Similarity

let selectedPapersForCBF = [];
let currentQueryForCBF = '';

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    console.log('[CBF] Initializing CBF calculation module...');

    // Listen for checkbox changes
    document.addEventListener('change', function (e) {
        if (e.target.classList.contains('paper-checkbox')) {
            setTimeout(updateFromCheckboxes, 100);
        }
    });

    console.log('[CBF] Module initialized');
});

// Update from checked checkboxes - this reads data from the DOM
function updateFromCheckboxes() {
    const checkboxes = document.querySelectorAll('.paper-checkbox:checked');
    selectedPapersForCBF = [];

    checkboxes.forEach((cb, idx) => {
        // Try to get paper data from various sources
        const card = cb.closest('.paper-card');
        if (card) {
            const title = card.querySelector('.paper-title')?.textContent || '';
            const authors = card.querySelector('.paper-authors')?.textContent || '';
            const abstract = card.querySelector('.paper-abstract')?.textContent || '';
            const relevanceSpan = card.querySelector('.relevance-score span');
            const relevance = relevanceSpan ? parseFloat(relevanceSpan.textContent) : 0;

            selectedPapersForCBF.push({
                title: title,
                authors: authors,
                abstract: abstract,
                relevance_score: relevance,
                index: idx
            });
        }
    });

    updateCBFPanelVisibility(selectedPapersForCBF);
}

// Update CBF panel visibility when papers are selected
function updateCBFPanelVisibility(papers, query) {
    selectedPapersForCBF = papers || [];
    currentQueryForCBF = query || '';

    const countBadge = document.getElementById('selectedCountBadge');
    const showCbfBtn = document.getElementById('showCbfBtn');

    if (!countBadge || !showCbfBtn) {
        console.log('[CBF] Panel elements not found');
        return;
    }

    if (selectedPapersForCBF.length > 0) {
        countBadge.innerHTML = `<i class="fas fa-check-circle"></i> ${selectedPapersForCBF.length} jurnal dipilih`;
        countBadge.classList.add('visible');
        showCbfBtn.classList.add('visible');
        console.log(`[CBF] ${selectedPapersForCBF.length} papers selected`);
    } else {
        countBadge.classList.remove('visible');
        showCbfBtn.classList.remove('visible');
        const cbfPanel = document.getElementById('cbfCalculationPanel');
        if (cbfPanel) cbfPanel.classList.remove('active');
    }
}

// Show CBF calculation panel
async function showCBFCalculation() {
    if (selectedPapersForCBF.length === 0) {
        alert('Pilih minimal 1 jurnal untuk melihat perhitungan');
        return;
    }

    const panel = document.getElementById('cbfCalculationPanel');
    const panelContent = document.getElementById('cbfPanelContent');

    if (!panel || !panelContent) {
        console.error('[CBF] Panel elements not found');
        return;
    }

    panelContent.innerHTML = `
        <div style="text-align: center; padding: 30px;">
            <i class="fas fa-spinner fa-spin fa-2x"></i>
            <p style="margin-top: 10px;">Menghitung TF-IDF dan Cosine Similarity...</p>
        </div>
    `;
    panel.classList.add('active');

    try {
        const response = await fetch('/api/cbf-details', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                papers: selectedPapersForCBF,
                query: currentQueryForCBF
            })
        });

        const data = await response.json();

        if (data.success) {
            displayCBFCalculation(data.details);
        } else {
            panelContent.innerHTML = '<p style="color: #ff6b6b;">Gagal menghitung. Silakan coba lagi.</p>';
        }
    } catch (error) {
        console.error('CBF calculation error:', error);
        panelContent.innerHTML = '<p style="color: #ff6b6b;">Terjadi kesalahan saat menghitung.</p>';
    }
}

// Display CBF calculation results
function displayCBFCalculation(details) {
    const panelContent = document.getElementById('cbfPanelContent');
    if (!panelContent) return;

    // Build preprocessing section
    const preprocessHtml = details.preprocessing_info.steps.map(s =>
        `<div style="padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">${s}</div>`
    ).join('');

    // Build TF-IDF terms section
    const tfidfHtml = details.papers_analysis.map(paper => `
        <div class="paper-terms-card">
            <h5><i class="fas fa-file-alt"></i> D${paper.index}: ${paper.title.substring(0, 40)}...</h5>
            <div style="font-size: 11px; color: #a5d8ff; margin-bottom: 8px;">Skor: ${paper.relevance_score}%</div>
            ${paper.top_tfidf_terms.map(t => `
                <div class="term-item">
                    <span>${t.term}</span>
                    <span class="term-weight">${t.weight}</span>
                </div>
            `).join('')}
        </div>
    `).join('');

    // Build similarity matrix section
    let matrixHtml = '';
    if (details.similarity_matrix && details.similarity_matrix.length > 0) {
        matrixHtml = `
            <table class="similarity-matrix-table">
                <thead>
                    <tr>
                        <th>Dokumen</th>
                        <th>Paling Mirip Dengan</th>
                    </tr>
                </thead>
                <tbody>
                    ${details.similarity_matrix.map(row => `
                        <tr>
                            <td><strong>D${row.paper_index}</strong>: ${row.paper_title}</td>
                            <td>
                                ${row.similarities.map(s =>
            `<span class="similarity-badge-small">D${s.to_paper}: ${s.score}%</span>`
        ).join('')}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    panelContent.innerHTML = `
        <!-- Preprocessing Section -->
        <div class="cbf-section">
            <h4><i class="fas fa-broom"></i> Tahap Preprocessing Teks</h4>
            ${preprocessHtml}
        </div>
        
        <!-- TF-IDF Formula Section -->
        <div class="cbf-section">
            <h4><i class="fas fa-calculator"></i> Pembobotan TF-IDF</h4>
            <div class="formula-box">${details.tfidf_info.formula}</div>
            <div class="formula-desc">
                <strong>TF:</strong> ${details.tfidf_info.tf_formula}<br>
                <strong>IDF:</strong> ${details.tfidf_info.idf_formula}
            </div>
            <div class="formula-desc" style="margin-top: 10px;">${details.tfidf_info.description}</div>
        </div>
        
        <!-- Top TF-IDF Terms per Paper -->
        <div class="cbf-section">
            <h4><i class="fas fa-tags"></i> Top TF-IDF Terms per Dokumen</h4>
            <div class="tfidf-terms-grid">${tfidfHtml}</div>
        </div>
        
        <!-- Cosine Similarity Section -->
        <div class="cbf-section">
            <h4><i class="fas fa-project-diagram"></i> Cosine Similarity</h4>
            <div class="formula-box">${details.cosine_info.formula}</div>
            <div class="formula-desc">${details.cosine_info.description}</div>
            ${details.similarity_matrix && details.similarity_matrix.length > 0 ? `
                <div style="margin-top: 15px;">
                    <h5 style="color: #ffd43b; margin-bottom: 10px;"><i class="fas fa-table"></i> Matriks Kemiripan Antar Dokumen</h5>
                    ${matrixHtml}
                </div>
            ` : ''}
        </div>
        
        <!-- Statistics -->
        <div class="cbf-stats-row">
            <div class="cbf-stat-item">
                <div class="cbf-stat-value">${details.total_papers}</div>
                <div class="cbf-stat-label">Dokumen Dianalisis</div>
            </div>
            <div class="cbf-stat-item">
                <div class="cbf-stat-value">${details.statistics?.total_unique_terms || 0}</div>
                <div class="cbf-stat-label">Total Terms Unik</div>
            </div>
            <div class="cbf-stat-item">
                <div class="cbf-stat-value">${details.statistics?.average_relevance || 0}%</div>
                <div class="cbf-stat-label">Rata-rata Relevansi</div>
            </div>
            <div class="cbf-stat-item">
                <div class="cbf-stat-value">${details.statistics?.max_relevance || 0}%</div>
                <div class="cbf-stat-label">Relevansi Tertinggi</div>
            </div>
        </div>
    `;
}

// Close CBF panel
function closeCBFPanel() {
    const panel = document.getElementById('cbfCalculationPanel');
    if (panel) panel.classList.remove('active');
}

console.log('[CBF] CBF calculation script loaded');
