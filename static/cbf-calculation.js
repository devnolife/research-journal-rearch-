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
  // Use all papers from search results if no papers selected
  let papersToAnalyze = selectedPapersForCBF;

  // If no papers selected, try to get from the global app
  if (papersToAnalyze.length === 0 && window.app && window.app.papers) {
    papersToAnalyze = window.app.papers.slice(0, 10);
    currentQueryForCBF = document.getElementById('searchInput')?.value || '';
  }

  if (papersToAnalyze.length === 0) {
    alert('Tidak ada jurnal untuk dianalisis. Silakan lakukan pencarian terlebih dahulu.');
    return;
  }

  const panel = document.getElementById('cbfCalculationPanel');
  const panelContent = document.getElementById('cbfPanelContent');

  if (!panel || !panelContent) {
    console.error('[CBF] Panel elements not found');
    return;
  }

  panelContent.innerHTML = `
        <div style="text-align: center; padding: 40px;">
            <i class="fas fa-spinner fa-spin fa-3x" style="color: #ffd43b;"></i>
            <p style="margin-top: 15px; font-size: 16px;">Menghitung TF-IDF dan Cosine Similarity...</p>
            <p style="margin-top: 5px; font-size: 12px; color: #a5d8ff;">Menganalisis ${papersToAnalyze.length} dokumen</p>
        </div>
    `;
  panel.classList.add('active');

  // Scroll to panel
  panel.scrollIntoView({ behavior: 'smooth', block: 'start' });

  try {
    const response = await fetch('/api/cbf-details', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        papers: papersToAnalyze,
        query: currentQueryForCBF || document.getElementById('searchInput')?.value || ''
      })
    });

    const data = await response.json();

    if (data.success) {
      displayCBFCalculation(data.details);
    } else {
      panelContent.innerHTML = `
                <div style="text-align: center; padding: 30px;">
                    <i class="fas fa-exclamation-triangle" style="color: #ff6b6b; font-size: 40px;"></i>
                    <p style="margin-top: 15px; color: #ff6b6b;">Gagal menghitung. Silakan coba lagi.</p>
                </div>
            `;
    }
  } catch (error) {
    console.error('CBF calculation error:', error);
    panelContent.innerHTML = `
            <div style="text-align: center; padding: 30px;">
                <i class="fas fa-exclamation-triangle" style="color: #ff6b6b; font-size: 40px;"></i>
                <p style="margin-top: 15px; color: #ff6b6b;">Terjadi kesalahan saat menghitung.</p>
                <p style="font-size: 12px; color: #a5d8ff;">${error.message}</p>
            </div>
        `;
  }
}

// Display CBF calculation results
function displayCBFCalculation(details) {
  const panelContent = document.getElementById('cbfPanelContent');
  if (!panelContent) return;

  // Build preprocessing section with example
  const preprocessHtml = details.preprocessing_info.steps.map(s =>
    `<div style="padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <i class="fas fa-check" style="color: #4ade80; margin-right: 8px;"></i>${s}
        </div>`
  ).join('');

  // Build example preprocessing
  const exampleHtml = details.preprocessing_info.example ? `
        <div style="margin-top: 15px; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px;">
            <div style="color: #ffd43b; font-size: 12px; margin-bottom: 10px;"><i class="fas fa-lightbulb"></i> Contoh Preprocessing:</div>
            <div style="font-size: 11px; margin-bottom: 5px;">
                <span style="color: #ff6b6b;">Original:</span> "${details.preprocessing_info.example.original}"
            </div>
            <div style="font-size: 11px;">
                <span style="color: #4ade80;">Final:</span> "${details.preprocessing_info.example.final}"
            </div>
        </div>
    ` : '';

  // Build TF-IDF detail section with formula examples
  let tfidfDetailHtml = '';
  if (details.tfidf_details && details.tfidf_details.length > 0) {
    tfidfDetailHtml = `
            <div style="margin-top: 15px;">
                <h5 style="color: #ffd43b; margin-bottom: 10px;"><i class="fas fa-table"></i> Detail Perhitungan TF-IDF per Term</h5>
                <div style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                        <thead>
                            <tr style="background: rgba(0,0,0,0.3);">
                                <th style="padding: 8px; text-align: left; color: #a5d8ff;">Term</th>
                                <th style="padding: 8px; text-align: center; color: #a5d8ff;">DF</th>
                                <th style="padding: 8px; text-align: left; color: #a5d8ff;">IDF Calculation</th>
                                <th style="padding: 8px; text-align: center; color: #a5d8ff;">Avg TF-IDF</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${details.tfidf_details.slice(0, 10).map(term => `
                                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                                    <td style="padding: 8px;"><strong style="color: #4ade80;">${term.term}</strong></td>
                                    <td style="padding: 8px; text-align: center;">${term.df}/${term.n_docs}</td>
                                    <td style="padding: 8px; font-family: monospace; color: #fbbf24;">${term.idf_formula}</td>
                                    <td style="padding: 8px; text-align: center; color: #4ade80; font-weight: bold;">${term.avg_tfidf}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
  }

  // Build Cosine Similarity detail section with step-by-step calculation
  let cosineDetailHtml = '';
  if (details.cosine_details && details.cosine_details.length > 0) {
    cosineDetailHtml = `
            <div style="margin-top: 15px;">
                <h5 style="color: #ffd43b; margin-bottom: 10px;"><i class="fas fa-calculator"></i> Perhitungan Cosine Similarity per Dokumen</h5>
                <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <div style="font-size: 11px; color: #a5d8ff; margin-bottom: 5px;">Query: "${details.query}"</div>
                    <div style="font-size: 11px; color: #4ade80;">Preprocessed: "${details.query_preprocessed || ''}"</div>
                </div>
                <div style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
                        <thead>
                            <tr style="background: rgba(0,0,0,0.3);">
                                <th style="padding: 8px; text-align: center; color: #a5d8ff;">Doc</th>
                                <th style="padding: 8px; text-align: left; color: #a5d8ff;">Title</th>
                                <th style="padding: 8px; text-align: left; color: #a5d8ff;">Calculation</th>
                                <th style="padding: 8px; text-align: center; color: #a5d8ff;">Similarity</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${details.cosine_details.map(doc => {
      const simColor = doc.similarity_percent >= 50 ? '#4ade80' : (doc.similarity_percent >= 25 ? '#fbbf24' : '#ff6b6b');
      return `
                                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                                        <td style="padding: 8px; text-align: center;"><strong>${doc.doc_id}</strong></td>
                                        <td style="padding: 8px; max-width: 150px; overflow: hidden; text-overflow: ellipsis;">${doc.title}...</td>
                                        <td style="padding: 8px; font-family: monospace; font-size: 10px; color: #a5d8ff;">${doc.formula}</td>
                                        <td style="padding: 8px; text-align: center;">
                                            <span style="background: ${simColor}20; color: ${simColor}; padding: 3px 10px; border-radius: 20px; font-weight: bold;">
                                                ${doc.similarity_percent}%
                                            </span>
                                        </td>
                                    </tr>
                                `;
    }).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
  }

  // Build TF-IDF terms section
  const tfidfHtml = details.papers_analysis.map(paper => `
        <div class="paper-terms-card">
            <h5><i class="fas fa-file-alt"></i> D${paper.index}: ${paper.title.substring(0, 40)}...</h5>
            <div style="font-size: 11px; color: #a5d8ff; margin-bottom: 8px;">Skor Relevansi: ${paper.relevance_score}%</div>
            ${paper.top_tfidf_terms.map(t => `
                <div class="term-item">
                    <span>${t.term}</span>
                    <span class="term-weight">${t.weight}</span>
                </div>
            `).join('')}
        </div>
    `).join('');

  // Build similarity interpretation
  const interpretHtml = details.cosine_info.interpretation ? `
        <div style="margin-top: 15px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
            <div style="background: rgba(74, 222, 128, 0.2); padding: 10px; border-radius: 8px; text-align: center;">
                <div style="color: #4ade80; font-weight: bold;">≥ 70%</div>
                <div style="font-size: 10px; color: #a5d8ff;">Sangat Relevan</div>
            </div>
            <div style="background: rgba(251, 191, 36, 0.2); padding: 10px; border-radius: 8px; text-align: center;">
                <div style="color: #fbbf24; font-weight: bold;">40-70%</div>
                <div style="font-size: 10px; color: #a5d8ff;">Cukup Relevan</div>
            </div>
            <div style="background: rgba(255, 107, 107, 0.2); padding: 10px; border-radius: 8px; text-align: center;">
                <div style="color: #ff6b6b; font-weight: bold;">< 40%</div>
                <div style="font-size: 10px; color: #a5d8ff;">Kurang Relevan</div>
            </div>
        </div>
    ` : '';

  panelContent.innerHTML = `
        <!-- Preprocessing Section -->
        <div class="cbf-section">
            <h4><i class="fas fa-broom"></i> Tahap 1: Preprocessing Teks</h4>
            ${preprocessHtml}
            ${exampleHtml}
        </div>
        
        <!-- TF-IDF Formula Section -->
        <div class="cbf-section">
            <h4><i class="fas fa-calculator"></i> Tahap 2: Pembobotan TF-IDF</h4>
            <div class="formula-box">${details.tfidf_info.formula}</div>
            <div class="formula-desc">
                <strong>Term Frequency (TF):</strong> ${details.tfidf_info.tf_formula}<br>
                <strong>Inverse Document Frequency (IDF):</strong> ${details.tfidf_info.idf_formula}<br>
                <span style="color: #a5d8ff; font-size: 11px;">${details.tfidf_info.idf_explanation || ''}</span>
            </div>
            <div class="formula-desc" style="margin-top: 10px; font-style: italic;">${details.tfidf_info.description}</div>
            ${tfidfDetailHtml}
        </div>
        
        <!-- Top TF-IDF Terms per Paper -->
        <div class="cbf-section">
            <h4><i class="fas fa-tags"></i> Top TF-IDF Terms per Dokumen</h4>
            <div class="tfidf-terms-grid">${tfidfHtml}</div>
        </div>
        
        <!-- Cosine Similarity Section -->
        <div class="cbf-section">
            <h4><i class="fas fa-project-diagram"></i> Tahap 3: Cosine Similarity</h4>
            <div class="formula-box">${details.cosine_info.formula}</div>
            <div class="formula-desc">
                <strong>Dot Product:</strong> ${details.cosine_info.dot_product_desc || 'A · B = Σ(Ai × Bi)'}<br>
                <strong>Magnitude:</strong> ${details.cosine_info.magnitude_desc || '||A|| = √(Σ Ai²)'}<br>
                <span style="color: #a5d8ff;">${details.cosine_info.range || 'Nilai: 0 hingga 1'}</span>
            </div>
            ${interpretHtml}
            ${cosineDetailHtml}
        </div>
        
        <!-- Statistics -->
        <div class="cbf-section">
            <h4><i class="fas fa-chart-bar"></i> Statistik Hasil</h4>
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
        </div>
    `;
}

// Close CBF panel
function closeCBFPanel() {
  const panel = document.getElementById('cbfCalculationPanel');
  if (panel) panel.classList.remove('active');
}

console.log('[CBF] CBF calculation script loaded');
