# Fazao Gestion - Django Full SSR Application

A complete Django Server-Side Rendering (SSR) enterprise management system for production, stock, clients, and resource management.

## Overview

This project has been transformed from an API-based architecture to a **100% Server-Side Rendering application** using Django's class-based views and HTML templates. All features are rendered on the server using Tailwind CSS for styling.

## Features

### Removed Components
- ❌ Django REST Framework (DRF)
- ❌ JWT Authentication
- ❌ CORS headers
- ❌ API endpoints
- ❌ Serializers
- ❌ React/Vue/AJAX

### Core Features
- ✅ Role-based authentication and authorization
- ✅ User management (ADMIN, SECRETARY, STOCK_MANAGER, PRODUCTION_MANAGER)
- ✅ Client management
- ✅ Order/Commande management
- ✅ Stock tracking with low-stock alerts
- ✅ Production tracking
- ✅ Resource management
- ✅ Reporting system
- ✅ Dashboard with role-specific views
- ✅ Server-side pagination
- ✅ Search functionality
- ✅ Responsive Tailwind CSS UI

## Project Structure

```
fazaogestion/
├── manage.py
├── requirements.txt
├── .env
├── config/
│   ├── settings.py          # Enhanced with SSR config
│   ├── urls.py              # Central URL routing
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/               # Authentication & User Management
│   │   ├── models.py        # CustomUser with roles
│   │   ├── views.py         # Login, Logout, User CRUD
│   │   ├── forms.py         # Authentication forms
│   │   ├── mixins.py        # Role-based access control
│   │   └── urls.py
│   ├── dashboard/           # Main dashboard
│   │   ├── views.py
│   │   └── urls.py
│   ├── clients/             # Client management
│   ├── commandes/           # Order management
│   ├── stock/               # Inventory management
│   ├── production/          # Production tracking
│   ├── ressources/          # Resource management
│   └── reporting/           # Reports
├── templates/
│   ├── base.html            # Base template with sidebar
│   ├── 403.html             # Permission denied
│   ├── 404.html             # Not found
│   ├── users/               # User templates
│   ├── clients/             # Client templates
│   ├── commandes/           # Order templates
│   ├── stock/               # Stock templates
│   ├── production/          # Production templates
│   ├── ressources/          # Resource templates
│   ├── reporting/           # Report templates
│   └── dashboard/           # Dashboard templates
└── static/                  # CSS, JS, images
```

## Database Models

### Users (CustomUser)
- Extends Django's AbstractUser
- Roles: ADMIN, SECRETARY, STOCK_MANAGER, PRODUCTION_MANAGER
- Fields: phone, avatar

### Client
- Name, email, phone, address
- Status: ACTIVE, INACTIVE, SUSPENDED
- Registration tracking

### Commande (Order)
- Links to Client
- Order number, description, quantity
- Status tracking (PENDING → DELIVERED)
- Expected and actual delivery dates

### Stock
- SKU, name, category
- Quantity and minimum thresholds
- Supplier and location tracking
- Low stock alerts

### Production
- Links to Commande
- Status tracking
- Production metrics (quantity produced, defects)
- Team assignment

### Ressource
- Types: EQUIPMENT, PERSONNEL, FACILITY, SOFTWARE
- Status tracking
- Maintenance scheduling
- Cost tracking

### Report
- Types: SALES, PRODUCTION, STOCK, FINANCIAL, OPERATIONS
- Date range tracking
- Generated data storage

## Authentication & Authorization

### Role-Based Access Control
- **ADMIN**: Full system access
- **SECRETARY**: Client and order management
- **STOCK_MANAGER**: Stock and inventory operations
- **PRODUCTION_MANAGER**: Production tracking and management
- All authenticated users have access to dashboard and resources

### Mixins
- `RoleRequiredMixin`: Base mixin for role checking
- `AdminRequiredMixin`: Admin only
- `AdminOrSecretaryMixin`: Admin or Secretary
- `AdminOrStockMixin`: Admin or Stock Manager
- `AdminOrProductionMixin`: Admin or Production Manager
- `AllStaffMixin`: All authenticated users

## URL Routing

### Main Routes
- `/` - Login page (or redirect to dashboard if authenticated)
- `/dashboard/` - Dashboard (requires authentication)
- `/utilisateurs/` - User management (admin only)
- `/clients/` - Client management
- `/commandes/` - Order management
- `/stock/` - Inventory management
- `/production/` - Production tracking
- `/ressources/` - Resource management
- `/reporting/` - Reports
- `/logout/` - Logout

### CRUD Pattern
For each entity:
- `/{entity}/` - List view
- `/{entity}/ajouter/` - Create view
- `/{entity}/<id>/` - Detail view
- `/{entity}/<id>/modifier/` - Update view
- `/{entity}/<id>/supprimer/` - Delete confirmation

## Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL (configured in settings.py)
- pip

### Installation Steps

1. **Clone and navigate to project**
   ```bash
   cd fazaogestion
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

Access the application at `http://localhost:8000`

## Environment Variables

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=fazao_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Templates & Styling

All templates use:
- **Tailwind CSS** (via CDN)
- **Font Awesome** icons
- **Responsive design** with mobile-first approach
- **Dark sidebar** navigation
- **Color-coded status badges**

## Forms

All forms include:
- CSRF protection
- Client-side validation via HTML5
- Responsive input styling
- Error message display
- Submit and cancel buttons

## Security Features

- ✅ CSRF token on all forms
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection (Django template escaping)
- ✅ Authentication required for all views
- ✅ Role-based access control
- ✅ Password hashing (Django default)
- ✅ HTTP-only sessions

## Admin Interface

The Django admin panel is fully functional at `/admin/`:
- User management
- Client management
- Order management
- Stock management
- Production tracking
- Resource management
- Reports

## Key Improvements from API Version

1. **Server-Side Rendering**: All HTML generated on server, no API calls needed
2. **Simplified Architecture**: No serializers, no API endpoints
3. **Better SEO**: Full HTML pages indexable by search engines
4. **Reduced Complexity**: Fewer moving parts, easier to maintain
5. **Enhanced Security**: No API token exposure
6. **Faster Initial Load**: No client-side processing needed
7. **Better UX**: Instant page loads, no loading spinners

## Development Notes

- Forms automatically apply Tailwind CSS classes via widget attributes
- All views use generic class-based views for consistency
- Templates inherit from `base.html` for consistent layout
- Messages framework used for user feedback
- Pagination configured at 15-20 items per page
- Search implemented via ORM filters, not full-text search

## Migration Guide

If upgrading from API version:
1. Backup your database
2. Run migrations: `python manage.py migrate`
3. No model changes needed - migrations handle schema updates
4. Test all routes in the new UI
5. Configure email for password reset (optional)

## Performance Optimization

- Database query optimization via select_related/prefetch_related
- Template caching enabled in production
- Static files served efficiently
- Pagination prevents loading large datasets
- Indexed database fields on commonly searched columns

## Contributing

- Follow PEP 8 style guide
- Use meaningful commit messages
- Test all CRUD operations
- Update templates consistently
- Document any new features

## Support

For issues or questions, contact the development team or check the project documentation.

## License

[Your License Here]
# FAZOA
