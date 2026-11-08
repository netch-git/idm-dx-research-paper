/**
 * ============================================================================
 * MAIN APPLICATION LOGIC — IDM STATISTICAL STUDY GUIDE
 * Navigation, Smooth Scrolling, Q&A Accordion, KaTeX + Fallback Renderer
 * ============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initAccordion();
  initMobileToggle();
  setupKaTeXWithFallback();
});

function initNavigation() {
  const navLinks = document.querySelectorAll('.nav-item a');
  const sections = document.querySelectorAll('.chapter-section');

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('href').substring(1);
      const targetElem = document.getElementById(targetId);
      if (targetElem) {
        targetElem.scrollIntoView({ behavior: 'smooth' });
        const sidebar = document.getElementById('sidebar');
        if (sidebar) sidebar.classList.remove('mobile-open');
      }
    });
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(l => {
          if (l.getAttribute('href') === '#' + id) {
            l.classList.add('active');
          } else {
            l.classList.remove('active');
          }
        });
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });

  sections.forEach(sec => observer.observe(sec));
}

function initAccordion() {
  const qaTriggers = document.querySelectorAll('.qa-trigger');
  qaTriggers.forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.parentElement;
      parent.classList.toggle('open');
      const icon = btn.querySelector('.qa-icon');
      if (icon) {
        icon.textContent = parent.classList.contains('open') ? '▲' : '▼';
      }
    });
  });
}

function initMobileToggle() {
  const toggleBtn = document.getElementById('mobile-toggle');
  const sidebar = document.getElementById('sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
    });
  }
}

/**
 * Robust KaTeX Auto-rendering with offline fallback
 */
function setupKaTeXWithFallback() {
  let rendered = false;

  function tryKaTeX() {
    if (window.renderMathInElement) {
      renderMathInElement(document.body, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\[', right: '\\]', display: true },
          { left: '\\(', right: '\\)', display: false }
        ],
        throwOnError: false,
        errorColor: '#D32F2F'
      });
      rendered = true;
      return true;
    }
    return false;
  }

  // Attempt immediately
  if (tryKaTeX()) return;

  // Retry on window load
  window.addEventListener('load', () => {
    if (!rendered) tryKaTeX();
  });

  // If after 1.5 seconds KaTeX is still unavailable (offline / blocked), apply clean Unicode fallback
  setTimeout(() => {
    if (!rendered && !window.renderMathInElement) {
      applyOfflineMathFallback();
    }
  }, 1500);
}

/**
 * Offline fallback: Converts raw LaTeX in formula cards into clean, legible HTML
 */
function applyOfflineMathFallback() {
  const formulaCards = document.querySelectorAll('.formula-card');
  formulaCards.forEach(card => {
    let t = card.innerHTML;
    // Strip $$ delimiters
    t = t.replace(/\$\$(.*?)\$\$/gs, '$1');
    
    // Replace standard LaTeX symbols
    t = t.replace(/\\alpha_\{?\\text\{family\}\}?/g, 'α<sub>family</sub>');
    t = t.replace(/\\alpha/g, 'α');
    t = t.replace(/\\beta_0/g, 'β₀');
    t = t.replace(/\\beta_1/g, 'β₁');
    t = t.replace(/\\beta/g, 'β');
    t = t.replace(/\\eta\^2/g, 'η²');
    t = t.replace(/\\eta/g, 'η');
    t = t.replace(/\\approx/g, '≈');
    t = t.replace(/\\bar\{X\}/g, 'X̄');
    t = t.replace(/\\bar\{Z\}/g, 'Z̄');
    t = t.replace(/\\times/g, '×');
    t = t.replace(/\\ge|\\geq/g, '≥');
    t = t.replace(/\\le|\\leq/g, '≤');
    t = t.replace(/\\Longleftrightarrow/g, '⟺');
    t = t.replace(/\\quad/g, '　');
    t = t.replace(/\\%/g, '%');
    
    // Format simple fractions: \frac{A}{B} -> (A) ÷ (B)
    t = t.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '<span class="offline-frac"><span class="frac-top">$1</span><span class="frac-div">÷</span><span class="frac-bottom">$2</span></span>');
    // Format complex fractions with text
    t = t.replace(/\\text\{([^}]+)\}/g, '$1');
    t = t.replace(/\\left\(/g, '(').replace(/\\right\)/g, ')');
    
    card.innerHTML = t;
  });
}
