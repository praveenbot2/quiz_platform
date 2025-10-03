// Real-time Portfolio Features

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Animate skill bars on scroll
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const skillBars = entry.target.querySelectorAll('.skill-progress');
                skillBars.forEach(bar => {
                    const width = bar.style.width;
                    bar.style.width = '0%';
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 100);
                });
            }
        });
    }, observerOptions);

    const skillsSection = document.querySelector('.skills');
    if (skillsSection) {
        observer.observe(skillsSection);
    }

    // Real-time status updates (simulated)
    const statusText = document.getElementById('status-text');
    const statuses = [
        'Available for projects',
        'Currently coding',
        'Open to opportunities',
        'Building something amazing'
    ];
    
    let currentStatusIndex = 0;
    setInterval(() => {
        currentStatusIndex = (currentStatusIndex + 1) % statuses.length;
        if (statusText) {
            statusText.style.opacity = '0';
            setTimeout(() => {
                statusText.textContent = statuses[currentStatusIndex];
                statusText.style.opacity = '1';
            }, 300);
        }
    }, 5000);

    // Add transition to status text
    if (statusText) {
        statusText.style.transition = 'opacity 0.3s ease';
    }

    // WebSocket connection for real-time updates (optional)
    // Uncomment if you want real WebSocket functionality
    /*
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/portfolio/`;
    
    const socket = new WebSocket(wsUrl);
    
    socket.onopen = function(e) {
        console.log('WebSocket connection established');
        socket.send(JSON.stringify({
            'type': 'portfolio_view',
            'message': 'User viewing portfolio'
        }));
    };
    
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log('Received:', data);
        
        // Handle real-time updates
        if (data.type === 'status_update' && statusText) {
            statusText.textContent = data.message;
        }
    };
    
    socket.onerror = function(error) {
        console.log('WebSocket error:', error);
    };
    
    socket.onclose = function(event) {
        console.log('WebSocket connection closed');
    };
    */

    // Add fade-in animation to project cards
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
    });

    // Highlight active navigation link on scroll
    const sections = document.querySelectorAll('section[id]');
    
    function highlightNavigation() {
        const scrollY = window.pageYOffset;
        
        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            const sectionId = section.getAttribute('id');
            
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                document.querySelectorAll('.nav-links a').forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', highlightNavigation);

    // Add parallax effect to hero section
    window.addEventListener('scroll', function() {
        const hero = document.querySelector('.hero');
        if (hero) {
            const scrolled = window.pageYOffset;
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });

    // Console message for developers
    console.log('%c👋 Hi there!', 'color: #6366f1; font-size: 20px; font-weight: bold;');
    console.log('%cThanks for checking out the source code!', 'color: #8b5cf6; font-size: 14px;');
    console.log('%cThis portfolio is built with Django and features real-time capabilities.', 'color: #6b7280; font-size: 12px;');
});
