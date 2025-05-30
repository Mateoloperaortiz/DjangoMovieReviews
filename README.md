# Movie Review Web Application

A comprehensive movie review web application built with Django, offering features such as movie listings, search, reviews, news, recommendations, and data visualization. This application has been developed progressively through multiple workshops, each adding new functionality.

## 📋 Project Overview

This application provides users with:

- Movie listing with details and search functionality
- Movie recommendations based on user preferences
- News section with latest movie-related articles
- Data visualization of movie statistics
- Scheduled tasks for updating movie information

## 🛠️ Technology Stack

- **Backend**: Django 5.0.1
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (default), expandable to other DB systems
- **Data Processing**: Pandas, Matplotlib
- **AI Integration**: OpenAI, Google Generative AI, Hugging Face
- **Task Scheduling**: Django-based task scheduler

## 🚀 Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Steps to Install

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/DjangoMovieReviews.git
   cd DjangoMovieReviews
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (for AI integration):
   Create an `openAI.env` file with your API keys.

5. Set up the database:

   ```bash
   python manage.py migrate
   ```

6. Load initial data (if available):

   ```bash
   python manage.py load_movies
   ```

7. Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

## 🏃‍♂️ Running the Application

1. Start the development server:

   ```bash
   python manage.py runserver
   ```

2. Access the application at `http://127.0.0.1:8000/`

3. Access the admin panel at `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

The project consists of several Django apps, each with a specific responsibility:

- **movie**: Core app handling movie listings, search, and statistics
- **news**: Manages movie-related news articles
- **recommendations**: Provides personalized movie recommendations
- **scheduler**: Handles scheduled tasks like updating movie data

## 🌟 Features

### Movie App

- Display of movie listings with details
- Search functionality by title
- Movie details page
- Data visualization (movies by year, genre)
- Database management through Django admin

### News App

- Display of movie-related news
- News listing using Bootstrap horizontal cards
- News detail pages

### Recommendations App

- AI-powered movie recommendations based on user preferences
- Form handling for user input
- Integration with AI services (OpenAI, Google Generative AI, Hugging Face)

### Scheduler App

- Automated tasks for data updates
- Custom management commands

## 📝 Workshop Reports

The following sections detail the development progress through a series of workshops.

# Movie Review Web Application - Workshop #1 Completion Report

This document serves as a summary of the accomplishments achieved during Workshop #1, focused on developing a movie review web application using Python and Django.  This workshop provided a hands-on introduction to full-stack web development principles and practical application of key technologies.

## Workshop Objectives and Achievements

Over the course of this workshop, I successfully implemented the foundational components of a functional web application. Key achievements include:

- **Django Project Initialization and Setup:**
  - Successfully initialized a Django project, establishing the base architecture for the application.
  - Explored the directory structure of a Django project, gaining familiarity with core files and directories such as `settings.py`, `urls.py`, and `manage.py`.
  - Demonstrated proficiency in launching the Django development server for local application testing and verification.
  - Created a Django application named `movie` to encapsulate movie-related functionalities, adhering to best practices for modular application design.

- **View and URL Configuration for Web Navigation:**
  - Developed Python-based views (`views.py`) to handle application logic and prepare data for presentation in web pages.
  - Configured URL patterns (`urls.py`) to map specific web routes to corresponding views, enabling navigation to key application pages such as the homepage and an "About" page.
  - Implemented data passing from views to templates, facilitating dynamic content rendering and user interaction.

- **Template Design and Bootstrap Integration for Enhanced User Interface:**
  - Utilized Django templates (`.html`) to decouple presentation logic from application code, promoting maintainability and clear separation of concerns.
  - Integrated the Bootstrap CSS framework to enhance the application's visual appeal and responsiveness, ensuring a consistent user experience across devices.
  - Implemented a functional Bootstrap Navbar for improved site navigation and user accessibility.
  - Enhanced the "About" page's presentation using Bootstrap components, specifically leveraging the Jumbotron component for a more engaging and informative layout.

- **Data Modeling and Database Management with Django ORM:**
  - Defined a `Movie` model (`models.py`) to represent movie data within the application, specifying relevant fields such as title, description, image, and URL, utilizing Django's ORM.
  - Leveraged Django migrations to translate the Python model definition into corresponding database schema modifications, streamlining database setup and evolution.
  - Explored the Django Admin interface, a built-in administration tool, to manage application data and content, including adding and administering movie records with associated images.

- **Implementation of Core Application Functionality: Movie Listing and Search:**
  - Implemented dynamic display of movie listings from the database on the homepage, creating a functional movie catalog.
  - Developed a search feature enabling users to filter movies by title, enhancing content discoverability and user engagement.
  - Created dedicated movie detail pages to present comprehensive information for each movie, improving content depth and user experience.

- **Version Control and Collaboration Workflow with Git and GitHub:**
  - Initialized a Git repository for the project, establishing version control for code tracking and collaborative development.
  - Created a remote repository on GitHub and pushed the local project, preparing for collaborative development and code sharing.
  - Practiced branching and merging workflows using Git, creating a `development` branch for feature development and subsequently merging it back into the `main` branch, demonstrating a fundamental collaborative development pattern.

# News and Movie Review Web Application - Workshop #2 Completion Report

This document summarizes the accomplishments and implementations achieved during Workshop #2, focused on enhancing a Movie Review Web Application using Django, Bootstrap, and database integration techniques.

## 🎯 Workshop Objectives

Workshop #2 built upon the foundation established in Workshop #1, expanding the application with:

- Improved frontend using Bootstrap components
- Enhanced database functionality with automatic population
- Implementation of data visualization features
- Addition of a news section
- Implementation of navigation between pages

## 💻 Technical Implementations

### Frontend Enhancement with Bootstrap

- **Bootstrap Integration**: Incorporated Bootstrap CSS and JS libraries into the application for responsive design and modern UI components.
- **Card Components**: Implemented Bootstrap cards to display movies in an aesthetically pleasing grid layout that automatically adjusts based on screen size.
- **Horizontal Cards**: Used Bootstrap's horizontal card layout to display news items in a clean, organized manner.
- **Navbar**: Created a responsive navigation bar with links to the main application sections (Home, News, Statistics).
- **Footer**: Added a professional footer with copyright information.

### Template Structure

- **Base Template**: Developed a base template with common elements (navigation bar, footer) to maintain consistency across all pages.
- **Template Extension**: Implemented template inheritance where specific page templates extend the base template, following DRY (Don't Repeat Yourself) principles.
- **Static Files Management**: Set up proper handling of static files (CSS, JS, images) to enhance the UI.

### Database Enhancements

- **Model Expansion**: Extended the `Movie` model with additional fields (genre, year) to provide more comprehensive movie information.
- **Automated Database Population**: Created a custom management command to automatically populate the database with movie data from a JSON file converted from a CSV dataset.
- **Data Migration**: Implemented database migrations to accommodate model changes while preserving existing data.

### Data Visualization

- **Statistics Page**: Created a dedicated page to visualize movie data through charts.
- **Year-based Analysis**: Implemented charts showing the distribution of movies by year.
- **Genre-based Analysis**: Created visualizations to display the number of movies per genre.
- **Matplotlib Integration**: Used Matplotlib to generate custom charts and embedded them in the templates as base64-encoded images.

### News Application

- **New Django App**: Created a separate Django app for news functionality.
- **News Model**: Designed a model to store news articles with headlines, content, and dates.
- **News Listing**: Implemented a page to display all news articles in reverse chronological order using Bootstrap horizontal cards.

### Navigation and Interactivity

- **Form Submissions**: Implemented form handling for search functionality and newsletter signup.
- **Cross-page Navigation**: Created a system to navigate between different pages of the application.
- **Back Navigation**: Added "back" links to improve user experience when moving between pages.
- **URL Patterns**: Defined named URL patterns for cleaner and more maintainable navigation.

## 📱 Responsive Design

- **Grid System**: Utilized Bootstrap's responsive grid system to ensure the application displays correctly on various screen sizes.
- **Mobile-friendly Layout**: Implemented responsive design principles, allowing the movie cards to stack vertically on smaller screens.
- **Responsive Navbar**: Configured the navigation bar to collapse into a hamburger menu on mobile devices.

## 🔍 Search Functionality

- **Movie Search**: Enhanced the search functionality to filter movies by title.
- **Search Results Display**: Improved the presentation of search results with clear indication of the search term.

## 📧 User Engagement Features

- **Newsletter Signup**: Implemented a form for users to subscribe to a newsletter.
- **Confirmation Page**: Created a confirmation page that displays after successful subscription.

## 🛠️ Development Tools and Dependencies

- **Requirements File**: Created a `requirements.txt` file listing all necessary Python packages for the project.
- **Version Control**: Maintained the project using Git with proper documentation.
- **Environment Configuration**: Set up proper Django settings for both development and future production environments.

## 🔄 Data Flow Implementation

- **CSV to JSON Conversion**: Developed a script to convert CSV movie data to JSON format for easier database integration.
- **GET Parameters**: Implemented parameter passing between views using GET method.
- **Context Variables**: Used Django's context system to pass data from views to templates.

## 🎨 Visual Improvements

- **Consistent Color Scheme**: Applied a consistent color palette throughout the application.
- **Typography**: Used Bootstrap's typography classes for readable and aesthetically pleasing text.
- **Visual Hierarchy**: Implemented proper spacing and sizing to create a clear visual hierarchy.

# Movie Review Web Application - Workshop #3 Completion Report

This document details the enhancements and new features implemented during Workshop #3, focusing on advanced features and integrations to elevate the movie review application.

## 🎯 Workshop #3 Objectives

Workshop #3 built upon previous foundations by implementing:

- AI-powered recommendation system
- Task scheduling for automated updates
- Enhanced user interaction features
- Advanced data integration techniques

## 💻 New Technical Implementations

### AI-Powered Recommendation System

- **Multiple AI Models Integration**: Implemented a recommendation system using OpenAI, Google's Generative AI, and Hugging Face.
- **User Preference Analysis**: Created a form to collect user movie preferences for personalized recommendations.
- **Cross-Model Result Comparison**: Developed functionality to compare and display recommendation results from different AI models.
- **Content-Based Filtering**: Implemented algorithms that analyze movie descriptions and genres to identify similar content.

### Task Scheduling System

- **Custom Scheduler App**: Created a dedicated Django app to manage scheduled tasks.
- **Automated Data Updates**: Implemented periodic tasks to update movie data and descriptions.
- **Management Commands**: Developed custom management commands for task execution.
- **Scalable Task Framework**: Designed a flexible system that can be extended for various scheduled operations.

### Enhanced User Experience

- **Improved UI/UX**: Refined the application interface with additional Bootstrap components and custom styling.
- **Interactive Elements**: Added dynamic content loading and user interaction features.
- **Responsive Design Enhancements**: Further improved mobile and tablet display optimization.
- **Form Validation**: Implemented client and server-side validation for user inputs.

### Advanced Data Integration

- **CSV Processing**: Enhanced data import functionality with improved CSV processing.
- **AI-Generated Content**: Implemented system to update movie descriptions using AI services.
- **Metadata Enhancement**: Added capability to enrich movie data with additional metadata.

## 🔄 Database and Model Improvements

- **Model Relationships**: Established relationships between movies, recommendations, and user preferences.
- **Data Integrity**: Implemented constraints to ensure data consistency across the application.
- **Query Optimization**: Improved database queries for better performance with larger datasets.

## 🛡️ Security and Error Handling

- **Form Security**: Enhanced form processing with CSRF protection and input sanitization.
- **Graceful Error Handling**: Implemented try-except blocks for robust error management.
- **User Input Validation**: Added comprehensive validation for all user inputs.

## 📊 Additional Data Visualization

- **Interactive Charts**: Enhanced data visualization with more interactive elements.
- **Recommendation Analysis**: Added visualizations to compare recommendation effectiveness.
- **Trend Analysis**: Implemented visualizations for movie trends based on release years and genres.

## 🔌 API Integration

- **External API Connections**: Set up framework for connecting to external movie data APIs.
- **AI Service API Handling**: Implemented robust error handling for AI service API calls.
- **Rate Limiting**: Added mechanisms to respect API rate limits and optimize usage.

## 📝 Documentation and Code Quality

- **Inline Documentation**: Added comprehensive docstrings and comments throughout the codebase.
- **README Enhancement**: Updated project documentation with complete setup and usage instructions.
- **Code Refactoring**: Improved code organization and reduced redundancy.
