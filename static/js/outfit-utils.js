// REDIRECT_DELAY must be less than TOAST_DURATION so the success toast
// is still visible when navigation fires.
const TOAST_DURATION = 4000;
const REDIRECT_DELAY = 1500;

let _originalSaveBtnText = null;

function setLoadingState(isLoading) {
    const saveBtn = document.getElementById('save');
    const nameInput = document.getElementById('nameInput');
    const arrows = document.querySelectorAll('.arrowBack, .arrowFoward');
    const navLinks = document.querySelectorAll('nav a, .completeArea a');

    if (_originalSaveBtnText === null) {
        _originalSaveBtnText = saveBtn.textContent;
    }

    if (isLoading) {
        saveBtn.disabled = true;
        saveBtn.setAttribute('aria-busy', 'true');
        saveBtn.innerHTML = '<span class="spinner"></span> Salvando...';

        arrows.forEach(arrow => {
            arrow.disabled = true;
            arrow.style.visibility = 'hidden';
            arrow.style.opacity = '0.3';
            arrow.style.pointerEvents = 'none';
        });

        nameInput.disabled = true;

        navLinks.forEach(link => {
            link.style.pointerEvents = 'none';
            link.setAttribute('aria-disabled', 'true');
            link.setAttribute('tabindex', '-1');
        });
    } else {
        saveBtn.disabled = false;
        saveBtn.setAttribute('aria-busy', 'false');
        saveBtn.textContent = _originalSaveBtnText;

        arrows.forEach(arrow => {
            arrow.disabled = false;
            arrow.style.visibility = '';
            arrow.style.opacity = '';
            arrow.style.pointerEvents = '';
        });

        nameInput.disabled = false;

        navLinks.forEach(link => {
            link.style.pointerEvents = '';
            link.removeAttribute('aria-disabled');
            link.removeAttribute('tabindex');
        });
    }
}

function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    // role=alert implies aria-live=assertive (interrupts screen reader) — use for errors.
    // role=status implies aria-live=polite (queued) — use for non-critical messages.
    // Never set aria-live explicitly alongside these roles; it overrides the implicit value.
    toast.setAttribute('role', type === 'error' ? 'alert' : 'status');

    document.body.appendChild(toast);

    // Double-rAF: first frame lets the browser paint the initial opacity:0 state,
    // second frame adds .show so the CSS transition fires reliably in Chromium.
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });
    });

    setTimeout(() => {
        toast.classList.remove('show');
        // Fallback timer removes the toast if transitionend never fires,
        // which happens under prefers-reduced-motion or when CSS fails to load.
        const fallback = setTimeout(() => toast.remove(), 500);
        toast.addEventListener('transitionend', () => {
            clearTimeout(fallback);
            toast.remove();
        }, { once: true });
    }, TOAST_DURATION);
}
