# Afra's Tabs - Django Guitar Tablature Website

A Django-based website for managing and displaying guitar tablatures, converted from static HTML templates.

## Features

- Artist, Album, and Song management
- Guitar tablature file management
- Search and filtering functionality
- Admin interface for content management
- Responsive design with TailwindCSS
- Dark theme optimized for music content

## Setup Instructions

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   
   ```

3. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the Site**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
├── tabs/                   # Main Django app
│   ├── models.py          # Data models (Artist, Album, Song, etc.)
│   ├── views.py           # View functions
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin interface configuration
├── templates/             # Django templates
│   ├── base.html          # Base template with common layout
│   └── tabs/              # App-specific templates
├── static/                # Static files (CSS, JS, images)
├── settings.py            # Django settings
├── urls.py                # Main URL configuration
└── manage.py              # Django management script
```

## Models

- **Artist**: Musicians/bands with tablatures
- **Album**: Music albums containing songs
- **Song**: Individual songs with tablature files
- **Tabber**: People who create the tablatures
- **SongChangeLog**: Track changes to song tablatures

## Key Features

- **Search**: Search across songs, artists, and albums
- **Filtering**: Filter by tuning, difficulty, and other criteria
- **Admin Interface**: Full CRUD operations for all models
- **File Management**: Automatic URL generation for tablature files
- **Responsive Design**: Works on desktop and mobile devices

## Usage

1. Use the admin interface to add artists, albums, and songs
2. Upload tablature files to your file storage (Backblaze B2 configured)
3. Users can browse, search, and filter tablatures
4. Individual pages for artists, albums, and songs with detailed information

## Configuration

- Update `settings.py` for production deployment
- Configure database settings as needed
- Update file storage URLs in models if using different storage provider