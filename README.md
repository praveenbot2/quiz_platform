# Real-Time Portfolio

A modern, responsive portfolio website with real-time features and dynamic content updates.

## Features

### 🚀 Real-Time Features
- **Live Visitor Counter**: Tracks and displays visitor count in real-time
- **Online Status Indicator**: Shows current online/offline status
- **Last Update Timestamp**: Displays when the portfolio was last updated
- **Activity Notifications**: Periodic updates showing recent activities
- **Dynamic Content Loading**: Projects and content load dynamically

### 🎨 Design Features
- Modern, dark-themed UI with gradient accents
- Fully responsive design (mobile, tablet, desktop)
- Smooth scroll animations
- Interactive hover effects
- Animated skill bars and statistics counters
- Typing effect on hero section

### 📦 Sections
1. **Home/Hero**: Introduction with animated typing text
2. **About**: Personal information with animated statistics
3. **Skills**: Technical skills with progress bars
4. **Projects**: Portfolio of featured projects
5. **Contact**: Contact form and information

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid, Flexbox, and animations
- **JavaScript (ES6+)**: Interactive features and real-time updates
- **Font Awesome**: Icons
- **LocalStorage**: Persistent visitor count

## Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A local web server (optional, for development)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/praveenbot2/quiz_platform.git
cd quiz_platform
```

2. Open the portfolio:
   - **Option 1**: Simply open `index.html` in your web browser
   - **Option 2**: Use a local server:
     ```bash
     # Using Python
     python -m http.server 8000
     
     # Using Node.js
     npx http-server
     
     # Then open http://localhost:8000
     ```

## File Structure

```
quiz_platform/
├── index.html       # Main HTML file
├── styles.css       # CSS styles
├── script.js        # JavaScript functionality
└── README.md        # Documentation
```

## Real-Time Features Explained

### Visitor Counter
- Tracks unique visits using localStorage
- Updates count on page load
- Simulates real-time updates every 10 seconds
- Displays formatted count with animations

### Status Indicator
- Shows online/offline status with a pulsing dot
- Monitors browser connectivity
- Updates automatically when connection changes

### Last Update Timer
- Displays time since last update
- Updates every 30 seconds
- Shows human-readable time format (e.g., "Just now", "5 minutes ago")

### Activity Notifications
- Shows periodic activity updates
- Slides in from bottom-right corner
- Auto-dismisses after 3 seconds
- Simulates real-time portfolio activity

## Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --dark-bg: #0f172a;
    --accent-color: #10b981;
}
```

### Content
- **Personal Info**: Update text in `index.html` sections
- **Skills**: Modify skill cards in HTML and adjust percentages
- **Projects**: Edit the projects array in `script.js`
- **Contact Info**: Update contact details in the Contact section

### Real-Time Settings
Adjust update intervals in `script.js`:
```javascript
// Visitor counter update (default: 10 seconds)
setInterval(() => { ... }, 10000);

// Status check (default: 5 seconds)
setInterval(() => { ... }, 5000);

// Activity notifications (default: 60 seconds)
setInterval(() => { ... }, 60000);
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Opera (latest)

## Performance

- Lightweight: No external dependencies except Font Awesome CDN
- Fast load times with optimized CSS and JavaScript
- Smooth animations using CSS transforms
- Efficient DOM manipulation

## Future Enhancements

- [ ] Backend integration for real visitor tracking
- [ ] WebSocket support for live updates
- [ ] Blog section with real-time comments
- [ ] Dark/Light theme toggle
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with GitHub API for live commit data
- [ ] Real-time chat feature

## License

This project is open source and available under the MIT License.

## Author

**Your Name**
- Email: contact@portfolio.com
- GitHub: [@praveenbot2](https://github.com/praveenbot2)

## Acknowledgments

- Font Awesome for icons
- CSS gradient inspirations from various design resources
- Animation techniques from modern web development practices

---

**Note**: This portfolio features simulated real-time updates. For production use with actual real-time data, consider integrating:
- WebSocket server (Socket.io, ws)
- Backend API (Node.js, Python, etc.)
- Database (MongoDB, PostgreSQL, Firebase)
- Analytics service (Google Analytics, custom solution)
