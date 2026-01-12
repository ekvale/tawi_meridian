/**
 * Tawi Meridian - Main JavaScript
 * 
 * This file contains JavaScript functionality for the site.
 * Most interactions are handled by HTMX, but some vanilla JS is used
 * for UI enhancements and accessibility.
 */

(function() {
    'use strict';

    // Mobile menu toggle
    function initMobileMenu() {
        const menuButton = document.getElementById('mobile-menu-button');
        const menu = document.getElementById('mobile-menu');
        
        if (menuButton && menu) {
            menuButton.addEventListener('click', function() {
                menu.classList.toggle('hidden');
                const isOpen = !menu.classList.contains('hidden');
                menuButton.setAttribute('aria-expanded', isOpen);
            });
        }
    }

    // Lazy loading images
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.classList.remove('lazy-load');
                            img.classList.add('loaded');
                            observer.unobserve(img);
                        }
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    // Animated counters for metrics
    function initCounters() {
        const counters = document.querySelectorAll('[data-count]');
        
        const animateCounter = (counter) => {
            const target = parseInt(counter.getAttribute('data-count'));
            const duration = 2000; // 2 seconds
            const increment = target / (duration / 16); // 60fps
            let current = 0;
            
            const update = () => {
                current += increment;
                if (current < target) {
                    const displayValue = Math.floor(current);
                    const suffix = counter.textContent.match(/[+%]/)?.[0] || '';
                    counter.textContent = displayValue + suffix;
                    requestAnimationFrame(update);
                } else {
                    const suffix = counter.textContent.match(/[+%]/)?.[0] || '';
                    counter.textContent = target + suffix;
                }
            };
            
            update();
        };

        if ('IntersectionObserver' in window) {
            const counterObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        counterObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            counters.forEach(counter => {
                counterObserver.observe(counter);
            });
        } else {
            // Fallback for browsers without IntersectionObserver
            counters.forEach(counter => {
                animateCounter(counter);
            });
        }
    }

    // Form validation enhancements
    function initFormValidation() {
        const forms = document.querySelectorAll('form[data-validate]');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    // Smooth scroll for anchor links
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href !== '#' && href.length > 1) {
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }

    // Alert dismissal
    function initAlertDismiss() {
        document.querySelectorAll('.alert-dismissible .close').forEach(button => {
            button.addEventListener('click', function() {
                const alert = this.closest('.alert');
                if (alert) {
                    alert.style.transition = 'opacity 0.3s';
                    alert.style.opacity = '0';
                    setTimeout(() => {
                        alert.remove();
                    }, 300);
                }
            });
        });
    }

    // Initialize everything when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initMobileMenu();
            initLazyLoading();
            initCounters();
            initFormValidation();
            initSmoothScroll();
            initAlertDismiss();
        });
    } else {
        initMobileMenu();
        initLazyLoading();
        initCounters();
        initFormValidation();
        initSmoothScroll();
        initAlertDismiss();
    }

    // Expose utility functions globally if needed
    window.TawiMeridian = {
        initMobileMenu,
        initLazyLoading,
        initCounters,
        initFormValidation,
        initSmoothScroll,
        initAlertDismiss
    };
})();
