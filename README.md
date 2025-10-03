# Quiz Platform with Portfolio

A Django-based quiz platform with AI-powered question generation and a modern portfolio showcase.

## Features

### Quiz Platform
- User registration and authentication
- Quiz creation and management
- AI-powered question generation using OpenAI API
- Real-time quiz functionality with WebSocket support (Django Channels)

### Portfolio Page
- Modern, responsive design
- Real-time status updates
- Smooth scroll navigation
- Animated skill progress bars
- Project showcase
- Contact information

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. (Optional) Set OpenAI API key as environment variable:
```bash
export OPENAI_API_KEY=your_api_key_here
```

4. Run the development server:
```bash
python manage.py runserver
```

5. Access the application:
- Portfolio (Home): http://localhost:8000/
- Alternative Portfolio URL: http://localhost:8000/quiz/portfolio/
- Admin: http://localhost:8000/admin/
- Quiz Registration: http://localhost:8000/quiz/register/
- Create Quiz: http://localhost:8000/quiz/create-quiz/
- Generate Questions: http://localhost:8000/quiz/generate-questions/

## Technology Stack

### Backend
- Python 3.12
- Django 5.1+
- Django REST Framework
- Django Channels (WebSocket support)
- Django Allauth (Authentication)
- OpenAI API

### Frontend
- HTML5
- CSS3 (Modern animations and gradients)
- JavaScript (ES6+)
- Responsive design

## Project Structure

```
quiz_platform/
├── quiz/                          # Main quiz app
│   ├── static/                    # Static files
│   │   ├── css/
│   │   │   └── portfolio.css      # Portfolio styles
│   │   └── js/
│   │       └── portfolio.js       # Portfolio interactions
│   ├── templates/                 # HTML templates
│   │   └── quiz/
│   │       └── portfolio.html     # Portfolio page
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── urls.py                    # URL routing
│   ├── consumers.py               # WebSocket consumers
│   └── routing.py                 # WebSocket routing
├── quiz_platform/                 # Project settings
│   ├── settings.py                # Django settings
│   ├── urls.py                    # Main URL configuration
│   └── asgi.py                    # ASGI configuration
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Features Details

### Real-time Portfolio Features
- **Dynamic Status Updates**: Status indicator cycles through different messages every 5 seconds
- **Smooth Navigation**: Click navigation links for smooth scroll to sections
- **Active Link Highlighting**: Navigation links highlight based on scroll position
- **Animated Skill Bars**: Progress bars animate when scrolled into view
- **Project Cards**: Hover effects and fade-in animations
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Quiz Features
- Create and manage quizzes with categories
- AI-powered question generation
- Multiple-choice questions
- User authentication and registration

## Development

The portfolio page is fully functional and includes:
- Praveen's developer information
- Featured projects including this quiz platform
- Technical skills with visual progress indicators
- Contact information
- Modern UI with gradients and animations

## License

This project is for educational and portfolio purposes.

## Author

Praveen - Software Developer
- GitHub: @praveenbot2
- Specializing in Node.js, Python/Django, and real-time web applications
