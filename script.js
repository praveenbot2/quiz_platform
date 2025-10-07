// Real-time Portfolio JavaScript

// Navigation
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initVisitorCounter();
    initTypingEffect();
    initScrollAnimations();
    initStatsCounter();
    initSkillBars();
    initProjects();
    initContactForm();
    initRealTimeUpdates();
});

// Navigation highlighting
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section, .hero');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= sectionTop - 100) {
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

    // Smooth scroll for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Visitor Counter (Real-time simulation)
function initVisitorCounter() {
    const counterElement = document.getElementById('visitor-count');
    
    // Get or initialize visitor count from localStorage
    let visitorCount = localStorage.getItem('visitorCount');
    if (!visitorCount) {
        visitorCount = Math.floor(Math.random() * 1000) + 500;
        localStorage.setItem('visitorCount', visitorCount);
    }
    
    // Increment count
    visitorCount = parseInt(visitorCount) + 1;
    localStorage.setItem('visitorCount', visitorCount);
    
    // Animate counter
    animateCounter(counterElement, 0, visitorCount, 2000);
    
    // Simulate real-time updates
    setInterval(() => {
        const currentCount = parseInt(counterElement.textContent.replace(/,/g, ''));
        const newCount = currentCount + Math.floor(Math.random() * 3);
        animateCounter(counterElement, currentCount, newCount, 500);
        localStorage.setItem('visitorCount', newCount);
    }, 10000); // Update every 10 seconds
}

// Animate counter
function animateCounter(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

// Typing effect
function initTypingEffect() {
    const texts = [
        'Hello, I\'m a Developer',
        'Hello, I\'m a Designer',
        'Hello, I\'m a Problem Solver',
        'Hello, I\'m a Creator'
    ];
    
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingElement = document.querySelector('.typing-text');
    const typingSpeed = 100;
    const deletingSpeed = 50;
    const pauseDuration = 2000;
    
    function type() {
        const currentText = texts[textIndex];
        
        if (isDeleting) {
            typingElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
        }
        
        let timeout = isDeleting ? deletingSpeed : typingSpeed;
        
        if (!isDeleting && charIndex === currentText.length) {
            timeout = pauseDuration;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            textIndex = (textIndex + 1) % texts.length;
        }
        
        setTimeout(type, timeout);
    }
    
    type();
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.skill-card, .project-card, .stat-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });
}

// Stats counter animation
function initStatsCounter() {
    const statNumbers = document.querySelectorAll('.stat-number');
    let animated = false;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                animated = true;
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.getAttribute('data-target'));
                    animateCounter(stat, 0, target, 2000);
                });
            }
        });
    }, { threshold: 0.5 });
    
    const statsSection = document.querySelector('.stats');
    if (statsSection) {
        observer.observe(statsSection);
    }
}

// Skill bars animation
function initSkillBars() {
    const skillBars = document.querySelectorAll('.skill-progress');
    let animated = false;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !animated) {
                animated = true;
                skillBars.forEach(bar => {
                    const progress = bar.getAttribute('data-progress');
                    setTimeout(() => {
                        bar.style.width = progress + '%';
                    }, 200);
                });
            }
        });
    }, { threshold: 0.3 });
    
    const skillsSection = document.getElementById('skills');
    if (skillsSection) {
        observer.observe(skillsSection);
    }
}

// Initialize projects
function initProjects() {
    const projects = [
        {
            title: 'E-Commerce Platform',
            description: 'A full-stack e-commerce solution with real-time inventory management',
            icon: '🛒',
            tags: ['React', 'Node.js', 'MongoDB'],
            github: '#',
            demo: '#'
        },
        {
            title: 'Task Management App',
            description: 'Collaborative task manager with real-time updates and notifications',
            icon: '✓',
            tags: ['Vue.js', 'Firebase', 'Tailwind'],
            github: '#',
            demo: '#'
        },
        {
            title: 'Weather Dashboard',
            description: 'Real-time weather data visualization with interactive maps',
            icon: '🌤️',
            tags: ['JavaScript', 'API', 'Charts.js'],
            github: '#',
            demo: '#'
        },
        {
            title: 'Social Media App',
            description: 'Modern social networking platform with messaging features',
            icon: '💬',
            tags: ['React Native', 'GraphQL', 'PostgreSQL'],
            github: '#',
            demo: '#'
        },
        {
            title: 'Portfolio Generator',
            description: 'Tool to create beautiful portfolios from templates',
            icon: '🎨',
            tags: ['Python', 'Flask', 'Jinja2'],
            github: '#',
            demo: '#'
        },
        {
            title: 'Analytics Dashboard',
            description: 'Real-time analytics dashboard with data visualization',
            icon: '📊',
            tags: ['React', 'D3.js', 'WebSocket'],
            github: '#',
            demo: '#'
        }
    ];
    
    const container = document.getElementById('projects-container');
    
    projects.forEach((project, index) => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        projectCard.style.animationDelay = `${index * 0.1}s`;
        
        projectCard.innerHTML = `
            <div class="project-image">
                <span>${project.icon}</span>
            </div>
            <div class="project-content">
                <h3>${project.title}</h3>
                <p>${project.description}</p>
                <div class="project-tags">
                    ${project.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
                <div class="project-links">
                    <a href="${project.github}" class="project-link"><i class="fab fa-github"></i> Code</a>
                    <a href="${project.demo}" class="project-link"><i class="fas fa-external-link-alt"></i> Demo</a>
                </div>
            </div>
        `;
        
        container.appendChild(projectCard);
    });
}

// Contact form
function initContactForm() {
    const form = document.getElementById('contact-form');
    const statusElement = document.getElementById('form-status');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        // Show loading state
        statusElement.textContent = 'Sending message...';
        statusElement.className = 'form-status';
        statusElement.style.display = 'block';
        
        // Simulate sending (in real app, this would make an API call)
        setTimeout(() => {
            statusElement.textContent = 'Message sent successfully! I\'ll get back to you soon.';
            statusElement.className = 'form-status success';
            form.reset();
            
            // Hide message after 5 seconds
            setTimeout(() => {
                statusElement.style.display = 'none';
            }, 5000);
        }, 1500);
    });
}

// Real-time updates
function initRealTimeUpdates() {
    const statusElement = document.getElementById('online-status');
    const updateElement = document.getElementById('last-update');
    
    // Update last modified time
    function updateTime() {
        const now = new Date();
        const timeAgo = getTimeAgo(now);
        updateElement.textContent = `Last updated: ${timeAgo}`;
    }
    
    updateTime();
    setInterval(updateTime, 30000); // Update every 30 seconds
    
    // Simulate online/offline status
    window.addEventListener('online', () => {
        statusElement.textContent = 'Online';
        statusElement.style.color = 'var(--accent-color)';
    });
    
    window.addEventListener('offline', () => {
        statusElement.textContent = 'Offline';
        statusElement.style.color = '#ef4444';
    });
    
    // Check connection periodically
    setInterval(() => {
        if (navigator.onLine) {
            statusElement.textContent = 'Online';
            statusElement.style.color = 'var(--accent-color)';
        } else {
            statusElement.textContent = 'Offline';
            statusElement.style.color = '#ef4444';
        }
    }, 5000);
}

// Helper function to get time ago
function getTimeAgo(date) {
    const now = new Date();
    const secondsAgo = Math.floor((now - date) / 1000);
    
    if (secondsAgo < 60) {
        return 'Just now';
    } else if (secondsAgo < 3600) {
        const minutes = Math.floor(secondsAgo / 60);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else if (secondsAgo < 86400) {
        const hours = Math.floor(secondsAgo / 3600);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
        const days = Math.floor(secondsAgo / 86400);
        return `${days} day${days > 1 ? 's' : ''} ago`;
    }
}

// Add real-time activity indicators
function addActivityIndicator() {
    const activities = [
        'Code committed',
        'Project updated',
        'Skill improved',
        'Achievement unlocked'
    ];
    
    setInterval(() => {
        const activity = activities[Math.floor(Math.random() * activities.length)];
        showNotification(activity);
    }, 60000); // Show activity every minute
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--card-bg);
        color: var(--text-primary);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px var(--shadow);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize activity indicators
addActivityIndicator();

// Console message
console.log('%c🚀 Portfolio Loaded!', 'color: #6366f1; font-size: 20px; font-weight: bold;');
console.log('%cReal-time features enabled ✓', 'color: #10b981; font-size: 14px;');
