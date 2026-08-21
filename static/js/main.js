// static/js/main.js

// Initialize GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(10, 92, 54, 0.95)';
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
    } else {
        navbar.style.background = 'rgba(34, 94, 46, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Toast notification function
function showToast(message, type = 'success') {
    const colors = {
        success: '#225E2E',
        error: '#dc3545',
        info: '#0A5C36'
    };

    const toast = document.createElement('div');
    toast.className = 'toast align-items-center show';
    toast.style.background = colors[type];
    toast.style.color = '#FEF1B4';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    const container = document.querySelector('.toast-container') || document.createElement('div');
    if (!document.querySelector('.toast-container')) {
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Quantity control function (global)
window.updateQuantity = function(change, element) {
    const card = element.closest('.product-card');
    const input = card.querySelector('.quantity-input');
    const display = card.querySelector('.quantity-display');
    if (!input) return;

    let newValue = parseInt(input.value) + change;
    if (newValue < 1) newValue = 1;
    input.value = newValue;
    if (display) display.textContent = newValue;
};

// Cart count update
window.updateCartCount = function() {
    fetch('/menu/cart-count/')
        .then(response => response.json())
        .then(data => {
            const countElement = document.getElementById('cart-count');
            if (countElement) countElement.textContent = data.count;
        })
        .catch(error => console.error('Error updating cart count:', error));
};

// Add to cart function
window.addToCart = function(button) {
    const card = button.closest('.product-card');
    if (!card) return;

    const name = card.querySelector('h4')?.textContent || 'Unknown';
    const activePrice = card.querySelector('.price-variant.active');
    const price = activePrice ? activePrice.dataset.price : '';
    const type = activePrice ? activePrice.dataset.type : '';
    const quantity = card.querySelector('.quantity-input')?.value || 1;

    const formData = new URLSearchParams();
    formData.append('product_name', name);
    formData.append('price', price);
    formData.append('quantity', quantity);
    formData.append('price_type', type);
    formData.append('image_url', card.dataset.product ? JSON.parse(card.dataset.product).image : '');

    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Adding...';
    button.disabled = true;

    fetch('/menu/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showToast('Added to cart successfully!', 'success');
            updateCartCount();
        } else {
            showToast(data.message || 'Error adding to cart', 'error');
        }
        button.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
        button.disabled = false;
    })
    .catch(error => {
        showToast('Network error. Please try again.', 'error');
        button.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
        button.disabled = false;
    });
};

// Lazy loading images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    images.forEach(img => imageObserver.observe(img));
});

// Cart count on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
});