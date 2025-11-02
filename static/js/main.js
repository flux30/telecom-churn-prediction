// ===================================
// MAIN JAVASCRIPT
// ===================================

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Telecom Churn Prediction App Loaded');
    
    // Initialize features
    initScrollReveal();
    initSmoothScroll();
    initFormValidation();
    
    // Add ripple effect to buttons
    addRippleEffect();
});

// ===================================
// SCROLL REVEAL
// ===================================
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.card, .feature-card, .metric-card, .stat-card');
    
    const revealOnScroll = () => {
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('reveal', 'active');
            }
        });
    };
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Initial check
}

// ===================================
// SMOOTH SCROLL
// ===================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ===================================
// FORM VALIDATION
// ===================================
function initFormValidation() {
    const form = document.getElementById('predictForm');
    
    if (form) {
        form.addEventListener('submit', handlePredictionSubmit);
    }
}

async function handlePredictionSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Disable button and show loading state
    submitButton.disabled = true;
    submitButton.textContent = 'Predicting...';
    
    // Prepare data
    const data = {
        age: formData.get('age'),
        monthly_spend: formData.get('monthly_spend'),
        tenure: formData.get('tenure'),
        recharge_type: formData.get('recharge_type'),
        data_usage: formData.get('data_usage'),
        complaints: formData.get('complaints'),
        model_type: formData.get('model_type')
    };
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayPredictionResult(result);
        } else {
            showError(result.error || 'Prediction failed');
        }
    } catch (error) {
        showError('Network error. Please try again.');
        console.error('Error:', error);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Predict Churn';
    }
}

// ===================================
// DISPLAY PREDICTION RESULT
// ===================================
function displayPredictionResult(result) {
    const resultContainer = document.getElementById('resultContainer');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');
    const modelUsed = document.getElementById('modelUsed');
    const prediction = document.getElementById('prediction');
    const probability = document.getElementById('probability');
    const confidence = document.getElementById('confidence');
    const recommendation = document.getElementById('recommendation');
    
    // Show result container
    resultContainer.style.display = 'block';
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Update status
    const isChurn = result.prediction === 'Churn';
    statusIcon.textContent = isChurn ? '⚠️' : '✅';
    statusText.textContent = result.prediction;
    statusText.style.color = isChurn ? '#F44336' : '#4CAF50';
    
    // Update details
    modelUsed.textContent = result.model_used === 'decision_tree' ? 'Decision Tree' : 'K-Nearest Neighbors';
    prediction.textContent = result.prediction;
    prediction.style.color = isChurn ? '#F44336' : '#4CAF50';
    
    if (result.probability !== null) {
        const probPercentage = (result.probability * 100).toFixed(2);
        probability.textContent = `${probPercentage}% chance of churn`;
    } else {
        probability.textContent = 'N/A';
    }
    
    confidence.textContent = result.confidence;
    
    // Update recommendation
    if (isChurn) {
        recommendation.innerHTML = `
            <h4 style="color: #F44336;">⚠️ High Churn Risk</h4>
            <p>This customer shows signs of potential churn. Recommended actions:</p>
            <ul>
                <li>Reach out proactively with retention offers</li>
                <li>Address any outstanding complaints immediately</li>
                <li>Offer personalized plans or upgrades</li>
                <li>Provide loyalty rewards or discounts</li>
            </ul>
        `;
    } else {
        recommendation.innerHTML = `
            <h4 style="color: #4CAF50;">✅ Low Churn Risk</h4>
            <p>This customer is likely to stay. Recommended actions:</p>
            <ul>
                <li>Continue providing excellent service</li>
                <li>Consider upselling premium features</li>
                <li>Encourage referrals and testimonials</li>
                <li>Maintain regular engagement</li>
            </ul>
        `;
    }
    
    // Animate result container
    resultContainer.classList.add('fade-in');
}

// ===================================
// ERROR HANDLING
// ===================================
function showError(message) {
    alert('Error: ' + message);
}

// ===================================
// RIPPLE EFFECT
// ===================================
function addRippleEffect() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.classList.add('ripple');
    });
}

// ===================================
// UTILITY FUNCTIONS
// ===================================

// Format currency
function formatCurrency(amount) {
    return '₹' + amount.toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Format percentage
function formatPercentage(value) {
    return (value * 100).toFixed(2) + '%';
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

console.log('✅ Main.js loaded successfully');
