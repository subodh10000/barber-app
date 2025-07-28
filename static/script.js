document.addEventListener('DOMContentLoaded', () => {

    // Feature 1: Pre-loader
    const preloader = document.querySelector('.preloader');
    window.addEventListener('load', () => {
        setTimeout(() => {
            preloader.classList.add('hidden');
        }, 200);
    });
    
    // Feature 2: Interactive Cursor
    const cursor = document.querySelector('.custom-cursor');
    const hoverElements = document.querySelectorAll('a, button, input, select, i');

    window.addEventListener('mousemove', e => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    hoverElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('grow'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('grow'));
    });

    // Feature 3: Advanced GSAP Animations
    const headline = new SplitType('.hero-headline', { types: 'chars' });
    gsap.from(headline.chars, {
        y: 100,
        opacity: 0,
        stagger: 0.05,
        ease: 'power4.out',
        duration: 1.5,
        delay: 1 // Delay to start after preloader fades
    });
    
    // Initialize AOS (Animate on Scroll)
    AOS.init({
        duration: 1000,
        once: true,
    });

    // Sticky Header & Active Link Highlighting
    const header = document.querySelector('.main-header');
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.background = 'rgba(18, 18, 18, 0.95)';
        } else {
            header.style.background = 'rgba(18, 18, 18, 0.8)';
        }

        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - header.offsetHeight) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === current) {
                link.classList.add('active');
            }
        });
    });
    
    // Form Submission
    const bookingForm = document.getElementById('booking-form');
    const formMessage = document.getElementById('form-message');

    bookingForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const service = document.getElementById('service').value;
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;

        if (!name || !email || !service || !date || !time) {
            showMessage('All fields are required.', 'error');
            return;
        }

        const formData = { name, email, service, date, time };

        fetch('/book-appointment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            showMessage(data.message, 'success');
            bookingForm.reset();
        })
        .catch((error) => {
            console.error('Error:', error);
            showMessage('An error occurred. Please try again.', 'error');
        });
    });
    
    function showMessage(message, type) {
        formMessage.textContent = message;
        formMessage.className = `form-message ${type}`;
        formMessage.style.display = 'block';
        
        setTimeout(() => {
            formMessage.style.display = 'none';
        }, 5000);
    }
});