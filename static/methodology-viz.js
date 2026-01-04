/**
 * Methodology Visualization Module
 * Handles interactivity for the TF-IDF methodology page
 */

// Global state
let currentStep = 0;

/**
 * Show step detail panel
 * @param {number} stepNumber - Step number (1-5)
 */
function showStepDetail(stepNumber) {
    // Hide all detail panels
    document.querySelectorAll('.step-detail-panel').forEach(panel => {
        panel.classList.remove('active');
    });

    // Remove active state from all step items
    document.querySelectorAll('.step-item').forEach(item => {
        item.classList.remove('active');
    });

    // Show selected detail panel
    const detailPanel = document.getElementById(`step-${stepNumber}-detail`);
    if (detailPanel) {
        detailPanel.classList.add('active');

        // Smooth scroll to detail panel
        setTimeout(() => {
            detailPanel.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'nearest'
            });
        }, 100);
    }

    // Highlight active step item
    const stepItem = document.querySelector(`.step-item[data-step="${stepNumber}"]`);
    if (stepItem) {
        stepItem.classList.add('active');
    }

    // Update current step
    currentStep = stepNumber;

    // Log for debugging
    console.log(`[Methodology] Showing step ${stepNumber}`);
}

/**
 * Navigate to next step
 */
function nextStep() {
    if (currentStep < 5) {
        showStepDetail(currentStep + 1);
    }
}

/**
 * Navigate to previous step
 */
function previousStep() {
    if (currentStep > 1) {
        showStepDetail(currentStep - 1);
    }
}

/**
 * Smooth scroll for internal anchor links
 */
function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);

            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Add keyboard navigation support
 */
function initializeKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
        // Only handle keyboard nav when not typing in an input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }

        switch(e.key) {
            case 'ArrowRight':
            case 'ArrowDown':
                e.preventDefault();
                nextStep();
                break;
            case 'ArrowLeft':
            case 'ArrowUp':
                e.preventDefault();
                previousStep();
                break;
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
                e.preventDefault();
                showStepDetail(parseInt(e.key));
                break;
        }
    });

    console.log('[Methodology] Keyboard navigation enabled (Arrow keys, 1-5)');
}

/**
 * Add animation on scroll for section cards
 */
function initializeScrollAnimations() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        },
        {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }
    );

    // Observe all section cards
    document.querySelectorAll('.section-card').forEach(card => {
        observer.observe(card);
    });
}

/**
 * Add hover effects for step items
 */
function enhanceStepInteractions() {
    document.querySelectorAll('.step-item').forEach((item, index) => {
        // Add tooltip on hover
        item.addEventListener('mouseenter', () => {
            const stepNumber = index + 1;
            const stepNames = [
                'Pengumpulan Dokumen',
                'Preprocessing Teks',
                'Perhitungan TF-IDF',
                'Cosine Similarity',
                'Ranking Hasil'
            ];

            // You can add a tooltip element here if needed
            console.log(`[Methodology] Hovering step ${stepNumber}: ${stepNames[index]}`);
        });

        // Add click feedback
        item.addEventListener('click', () => {
            // Add a subtle pulse animation
            item.style.animation = 'none';
            setTimeout(() => {
                item.style.animation = '';
            }, 10);
        });
    });
}

/**
 * Track user engagement with steps
 */
function trackStepEngagement() {
    const visitedSteps = new Set();

    // Track when a step is viewed
    const originalShowStepDetail = window.showStepDetail;
    window.showStepDetail = function(stepNumber) {
        visitedSteps.add(stepNumber);

        // Log progress
        if (visitedSteps.size === 5) {
            console.log('[Methodology] 🎉 All steps viewed! User has completed the tour.');
        }

        // Call original function
        originalShowStepDetail(stepNumber);
    };
}

/**
 * Initialize page on load
 */
function initializePage() {
    console.log('[Methodology] Initializing page...');

    // Show first step by default
    showStepDetail(1);

    // Initialize smooth scrolling
    initializeSmoothScroll();

    // Initialize keyboard navigation
    initializeKeyboardNavigation();

    // Initialize scroll animations
    initializeScrollAnimations();

    // Enhance step interactions
    enhanceStepInteractions();

    // Track engagement
    trackStepEngagement();

    // Add progress indicator (optional)
    updateProgressIndicator();

    console.log('[Methodology] ✓ Page initialized successfully');
}

/**
 * Update progress indicator based on current step
 */
function updateProgressIndicator() {
    // Calculate progress percentage
    const progress = (currentStep / 5) * 100;

    // You can add a progress bar element if needed
    console.log(`[Methodology] Progress: ${progress}%`);
}

/**
 * Add accessibility features
 */
function enhanceAccessibility() {
    // Add ARIA labels to step items
    document.querySelectorAll('.step-item').forEach((item, index) => {
        const stepNumber = index + 1;
        item.setAttribute('role', 'button');
        item.setAttribute('aria-label', `Step ${stepNumber}: Click to view details`);
        item.setAttribute('tabindex', '0');

        // Allow Enter key to activate step
        item.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                showStepDetail(stepNumber);
            }
        });
    });

    // Add ARIA live region for step changes
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.style.position = 'absolute';
    liveRegion.style.left = '-10000px';
    liveRegion.style.width = '1px';
    liveRegion.style.height = '1px';
    liveRegion.style.overflow = 'hidden';
    document.body.appendChild(liveRegion);

    // Update live region when step changes
    const originalShowStepDetail = window.showStepDetail;
    window.showStepDetail = function(stepNumber) {
        const stepNames = [
            'Pengumpulan Dokumen',
            'Preprocessing Teks',
            'Perhitungan TF-IDF',
            'Cosine Similarity',
            'Ranking Hasil'
        ];
        liveRegion.textContent = `Now showing: Step ${stepNumber} - ${stepNames[stepNumber - 1]}`;
        originalShowStepDetail(stepNumber);
    };

    console.log('[Methodology] ✓ Accessibility features enabled');
}

/**
 * Add print-friendly styling
 */
function enablePrintMode() {
    window.addEventListener('beforeprint', () => {
        console.log('[Methodology] Preparing for print...');

        // Show all step details for printing
        document.querySelectorAll('.step-detail-panel').forEach(panel => {
            panel.style.display = 'block';
        });
    });

    window.addEventListener('afterprint', () => {
        console.log('[Methodology] Print completed');

        // Restore original state
        document.querySelectorAll('.step-detail-panel').forEach(panel => {
            panel.style.display = '';
        });

        // Re-show current step
        showStepDetail(currentStep);
    });
}

/**
 * Handle page visibility changes
 */
function handleVisibilityChange() {
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            console.log('[Methodology] Page hidden');
        } else {
            console.log('[Methodology] Page visible again');
        }
    });
}

/**
 * Add responsive behavior for mobile
 */
function handleResponsiveFeatures() {
    // Check if mobile
    const isMobile = window.innerWidth <= 768;

    if (isMobile) {
        console.log('[Methodology] Mobile mode detected');

        // Adjust scroll behavior for mobile
        document.querySelectorAll('.step-item').forEach(item => {
            item.addEventListener('click', () => {
                // Add slight delay for mobile tap
                setTimeout(() => {
                    window.scrollBy({
                        top: 100,
                        behavior: 'smooth'
                    });
                }, 300);
            });
        });
    }

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const newIsMobile = window.innerWidth <= 768;
            if (newIsMobile !== isMobile) {
                console.log('[Methodology] Screen size changed, updating layout');
            }
        }, 250);
    });
}

/**
 * Add share functionality (optional)
 */
function addShareFeature() {
    // Check if Web Share API is available
    if (navigator.share) {
        console.log('[Methodology] Web Share API available');

        // You can add a share button here if needed
        // Example:
        // const shareButton = document.getElementById('shareButton');
        // shareButton.addEventListener('click', async () => {
        //     try {
        //         await navigator.share({
        //             title: 'Metodologi TF-IDF',
        //             text: 'Pelajari bagaimana TF-IDF dan Content-Based Filtering bekerja!',
        //             url: window.location.href
        //         });
        //     } catch (err) {
        //         console.log('Share failed:', err);
        //     }
        // });
    }
}

/**
 * Error handling
 */
function setupErrorHandling() {
    window.addEventListener('error', (e) => {
        console.error('[Methodology] Error occurred:', e.message);
    });

    window.addEventListener('unhandledrejection', (e) => {
        console.error('[Methodology] Unhandled promise rejection:', e.reason);
    });
}

/**
 * Performance monitoring (optional)
 */
function monitorPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log('[Methodology] Page load time:', Math.round(perfData.loadEventEnd - perfData.fetchStart), 'ms');
            }
        });
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Main initialization when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('[Methodology] DOM Content Loaded');

    // Core initialization
    initializePage();

    // Enhanced features
    enhanceAccessibility();
    enablePrintMode();
    handleVisibilityChange();
    handleResponsiveFeatures();
    addShareFeature();

    // Monitoring
    setupErrorHandling();
    monitorPerformance();

    console.log('[Methodology] 🚀 All features initialized');
});

/**
 * Fallback for older browsers
 */
if (document.readyState === 'loading') {
    // DOM is still loading
    console.log('[Methodology] Waiting for DOM...');
} else {
    // DOM already loaded
    console.log('[Methodology] DOM already loaded, initializing immediately');
    setTimeout(() => {
        if (typeof showStepDetail === 'function') {
            showStepDetail(1);
        }
    }, 100);
}

// Export functions for potential use in console or other scripts
window.methodologyViz = {
    showStepDetail,
    nextStep,
    previousStep,
    currentStep: () => currentStep
};

console.log('[Methodology] Script loaded successfully');
