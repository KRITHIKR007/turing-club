// Initialize all components
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeAnimations();
    initializeForms();
    initializeScrollBehavior();
    initializeCookieConsent();
});

// Remove duplicate initialization code from index.html and move here
function initializeAnimations() {
    gsap.registerPlugin(ScrollTrigger);

    // Hero animation
    gsap.from('.hero-content', {
        opacity: 0,
        y: 100,
        duration: 1,
        scrollTrigger: {
            trigger: '.hero-content',
            start: 'top 80%',
        }
    });

    // Initialize AOS
    AOS.init({
        duration: 800,
        once: true,
        offset: 100
    });
}

function initializeScrollBehavior() {
    // Back to top button
    const backToTopButton = document.getElementById('backToTop');
    
    window.addEventListener('scroll', () => {
        backToTopButton.style.opacity = window.scrollY > 500 ? '1' : '0';
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

function initializeCookieConsent() {
    const cookieConsent = document.getElementById('cookieConsent');
    const acceptCookies = document.getElementById('acceptCookies');
    const rejectCookies = document.getElementById('rejectCookies');

    if (!localStorage.getItem('cookieConsent')) {
        setTimeout(() => {
            cookieConsent.style.transform = 'translateY(0)';
        }, 1000);
    }

    [acceptCookies, rejectCookies].forEach(button => {
        button.addEventListener('click', () => {
            localStorage.setItem('cookieConsent', button.id === 'acceptCookies' ? 'accepted' : 'rejected');
            cookieConsent.style.transform = 'translateY(100%)';
        });
    });
}

function initializeForms() {
    // Join Form Handler
    const joinForm = document.querySelector('#join-form form');
    if (joinForm) {
        joinForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const button = joinForm.querySelector('button[type="submit"]');
            const originalText = button.innerHTML;
            
            try {
                button.innerHTML = `
                    <svg class="animate-spin h-5 w-5 mr-3 inline" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                `;

                const formData = new FormData(joinForm);
                const response = await fetch('/backend/forms/submit_form.php', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                
                if (data.success) {
                    button.innerHTML = `
                        <svg class="h-5 w-5 mr-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                        Application Submitted!
                    `;
                    joinForm.reset();
                } else {
                    throw new Error(data.error || 'Submission failed');
                }
            } catch (error) {
                button.innerHTML = `
                    <svg class="h-5 w-5 mr-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                    Error. Try Again
                `;
            }

            setTimeout(() => {
                button.innerHTML = originalText;
            }, 3000);
        });
    }

    // Newsletter Form Handler
    const newsletterForm = document.querySelector('footer form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const button = newsletterForm.querySelector('button');
            const input = newsletterForm.querySelector('input');
            const originalIcon = button.innerHTML;

            try {
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                
                const response = await fetch('/backend/forms/newsletter.php', {
                    method: 'POST',
                    body: JSON.stringify({ email: input.value }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();
                
                if (data.success) {
                    button.innerHTML = '<i class="fas fa-check"></i>';
                    input.value = '';
                } else {
                    throw new Error(data.error || 'Subscription failed');
                }
            } catch (error) {
                button.innerHTML = '<i class="fas fa-exclamation"></i>';
            }

            setTimeout(() => {
                button.innerHTML = originalIcon;
            }, 3000);
        });
    }
}