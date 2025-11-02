// ===================================
// GSAP ANIMATIONS - PRODUCTION READY
// No Content Disappears - Guaranteed
// ===================================

/**
 * Initialize GSAP animations only if library is available
 * Focuses on hover effects and smooth transitions
 * NO animations that hide or fade out content
 */

(function() {
    'use strict';

    // Check if GSAP is available
    const hasGSAP = typeof gsap !== 'undefined';
    
    if (!hasGSAP) {
        console.log('✅ GSAP not loaded - using CSS transitions');
        return;
    }

    // Register GSAP plugins if available
    if (typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
    }

    // ===================================
    // INITIALIZATION
    // ===================================
    
    document.addEventListener('DOMContentLoaded', function() {
        console.log('✅ Animations initialized');
        initHoverEffects();
        initButtonAnimations();
        initNavAnimations();
    });

    // ===================================
    // CARD HOVER EFFECTS
    // ===================================
    function initHoverEffects() {
        const cards = document.querySelectorAll(
            '.feature-card, ' +
            '.metric-card, ' +
            '.stat-card, ' +
            '.glass-card, ' +
            '.insight-card, ' +
            '.characteristic-card, ' +
            '.matrix-container, ' +
            '.chart-container, ' +
            '.metric-info-card'
        );

        if (cards.length === 0) {
            console.log('No cards found for hover animations');
            return;
        }

        cards.forEach((card) => {
            // Mouse enter
            card.addEventListener('mouseenter', function() {
                gsap.killTweensOf(this);
                gsap.to(this, {
                    y: -4,
                    duration: 0.3,
                    ease: 'power2.out',
                    overwrite: 'auto'
                });
            });

            // Mouse leave
            card.addEventListener('mouseleave', function() {
                gsap.killTweensOf(this);
                gsap.to(this, {
                    y: 0,
                    duration: 0.3,
                    ease: 'power2.out',
                    overwrite: 'auto'
                });
            });
        });

        console.log(`✅ Hover effects added to ${cards.length} cards`);
    }

    // ===================================
    // BUTTON ANIMATIONS
    // ===================================
    function initButtonAnimations() {
        const buttons = document.querySelectorAll('.btn');

        if (buttons.length === 0) {
            console.log('No buttons found for animations');
            return;
        }

        buttons.forEach((button) => {
            // Mouse enter
            button.addEventListener('mouseenter', function() {
                gsap.killTweensOf(this);
                gsap.to(this, {
                    scale: 1.02,
                    duration: 0.2,
                    ease: 'power2.out',
                    overwrite: 'auto'
                });
            });

            // Mouse leave
            button.addEventListener('mouseleave', function() {
                gsap.killTweensOf(this);
                gsap.to(this, {
                    scale: 1,
                    duration: 0.2,
                    ease: 'power2.out',
                    overwrite: 'auto'
                });
            });

            // Click effect
            button.addEventListener('mousedown', function() {
                gsap.killTweensOf(this);
                gsap.to(this, {
                    scale: 0.98,
                    duration: 0.1,
                    overwrite: 'auto'
                });
            });

            button.addEventListener('mouseup', function() {
                gsap.killTweensOf(this);
                gsap.to(this, {
                    scale: 1.02,
                    duration: 0.1,
                    overwrite: 'auto'
                });
            });
        });

        console.log(`✅ Button animations added to ${buttons.length} buttons`);
    }

    // ===================================
    // NAVIGATION ANIMATIONS
    // ===================================
    function initNavAnimations() {
        const navLinks = document.querySelectorAll('.nav-link');

        if (navLinks.length === 0) {
            console.log('No nav links found for animations');
            return;
        }

        navLinks.forEach((link) => {
            // Mouse enter
            link.addEventListener('mouseenter', function() {
                if (!this.classList.contains('active')) {
                    gsap.killTweensOf(this);
                    gsap.to(this, {
                        scale: 1.03,
                        duration: 0.2,
                        ease: 'power2.out',
                        overwrite: 'auto'
                    });
                }
            });

            // Mouse leave
            link.addEventListener('mouseleave', function() {
                if (!this.classList.contains('active')) {
                    gsap.killTweensOf(this);
                    gsap.to(this, {
                        scale: 1,
                        duration: 0.2,
                        ease: 'power2.out',
                        overwrite: 'auto'
                    });
                }
            });
        });

        console.log(`✅ Navigation animations added to ${navLinks.length} links`);
    }

    // ===================================
    // UTILITY FUNCTIONS
    // ===================================

    /**
     * Animate value counter
     * @param {HTMLElement} element - Target element
     * @param {number} target - Target value
     * @param {number} duration - Animation duration
     */
    window.animateCounter = function(element, target, duration = 1.5) {
        if (!hasGSAP || !element) return;

        let current = parseInt(element.textContent) || 0;
        
        gsap.to({ value: current }, {
            value: target,
            duration: duration,
            ease: 'power2.out',
            onUpdate: function() {
                element.textContent = Math.ceil(this.targets()[0].value);
            }
        });
    };

    /**
     * Scroll to element smoothly
     * @param {string|HTMLElement} target - Target selector or element
     */
    window.smoothScroll = function(target) {
        if (!hasGSAP) return;

        const element = typeof target === 'string' 
            ? document.querySelector(target) 
            : target;

        if (!element) return;

        gsap.to(window, {
            scrollTo: element,
            duration: 0.8,
            ease: 'power2.inOut'
        });
    };

    /**
     * Animate element fade in
     * @param {HTMLElement} element - Target element
     * @param {number} duration - Animation duration
     */
    window.fadeInElement = function(element, duration = 0.6) {
        if (!hasGSAP || !element) return;

        gsap.from(element, {
            opacity: 0,
            y: 20,
            duration: duration,
            ease: 'power2.out'
        });
    };

    /**
     * Stagger animate elements
     * @param {string|HTMLElement[]} elements - Elements selector or array
     * @param {number} stagger - Stagger amount
     * @param {number} duration - Animation duration
     */
    window.staggerAnimateIn = function(elements, stagger = 0.1, duration = 0.6) {
        if (!hasGSAP) return;

        const els = typeof elements === 'string'
            ? document.querySelectorAll(elements)
            : elements;

        if (els.length === 0) return;

        gsap.from(els, {
            opacity: 0,
            y: 30,
            duration: duration,
            stagger: stagger,
            ease: 'power2.out'
        });
    };

    // ===================================
    // PAGE LOAD ANIMATION (OPTIONAL)
    // ===================================
    
    window.addEventListener('load', function() {
        // Animate hero section if exists
        const heroTitle = document.querySelector('.hero-title');
        const heroSubtitle = document.querySelector('.hero-subtitle');
        const heroDescription = document.querySelector('.hero-description');
        const ctaButtons = document.querySelector('.cta-buttons');

        if (heroTitle) {
            gsap.from(heroTitle, {
                opacity: 0,
                y: 30,
                duration: 0.6,
                ease: 'power2.out'
            });
        }

        if (heroSubtitle) {
            gsap.from(heroSubtitle, {
                opacity: 0,
                y: 20,
                duration: 0.6,
                delay: 0.1,
                ease: 'power2.out'
            });
        }

        if (heroDescription) {
            gsap.from(heroDescription, {
                opacity: 0,
                y: 20,
                duration: 0.6,
                delay: 0.2,
                ease: 'power2.out'
            });
        }

        if (ctaButtons) {
            gsap.from(ctaButtons, {
                opacity: 0,
                y: 20,
                duration: 0.6,
                delay: 0.3,
                ease: 'power2.out'
            });
        }

        // Stagger feature cards
        const featureCards = document.querySelectorAll('.features-grid .feature-card');
        if (featureCards.length > 0) {
            gsap.from(featureCards, {
                opacity: 0,
                y: 40,
                duration: 0.5,
                stagger: 0.1,
                delay: 0.4,
                ease: 'power2.out'
            });
        }

        // Stagger metric cards
        const metricCards = document.querySelectorAll('.metrics-grid .metric-card');
        if (metricCards.length > 0) {
            gsap.from(metricCards, {
                opacity: 0,
                scale: 0.95,
                duration: 0.5,
                stagger: 0.1,
                delay: 0.5,
                ease: 'back.out(1.5)'
            });
        }

        console.log('✅ Page load animations complete');
    });

    // ===================================
    // GLOBAL ERROR HANDLING
    // ===================================
    window.addEventListener('error', function(event) {
        // Don't break animations on errors
        if (event.message && event.message.includes('GSAP')) {
            console.warn('GSAP Error (non-critical):', event.message);
            return;
        }
    });

    console.log('✅ GSAP Animations Module Loaded Successfully');

})();
