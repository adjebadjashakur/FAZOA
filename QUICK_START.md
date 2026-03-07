# Quick Start Guide - Fazao Gestion

Get your Fazao Gestion SSR application running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- PostgreSQL database
- pip package manager

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
cat > .env << EOF
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
```

### 3. Database Setup

Configure your database in `config/settings.py` or use the default SQLite for development:

```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to create your first admin user
```

### 4. Start Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

---

## First Login

1. Navigate to http://localhost:8000
2. You'll be redirected to login page
3. Enter superuser credentials you created
4. You'll see the admin dashboard

---

## Default User Roles

When creating users, assign one of these roles:

- **ADMIN** - Full system access, user management
- **SECRETARY** - Client and order management
- **STOCK_MANAGER** - Inventory operations
- **PRODUCTION_MANAGER** - Production tracking

---

## Main Navigation

After login, use the sidebar to navigate:

### Admin Access
- **Tableau de Bord** - Dashboard with key metrics
- **Clients** - Manage customers
- **Commandes** - Manage orders
- **Stock** - Manage inventory
- **Production** - Track production
- **Ressources** - Manage equipment/personnel
- **Rapports** - Generate reports
- **Utilisateurs** - User management (admin only)
- **Admin** - Django admin panel

### Staff Access
View is limited based on role:
- Secretaries see: Clients, Commandes
- Stock Managers see: Stock
- Production Managers see: Production

---

## Creating Test Data

### Via Admin Interface

1. Go to http://localhost:8000/admin
2. Login with superuser account
3. Click on each model to add test data:
   - Clients (customers)
   - Commandes (orders)
   - Stock (inventory items)
   - Productions
   - Ressources
   - Reports

### Via Application UI

1. Navigate to each section from the sidebar
2. Click **+ Nouveau...** button to create new items
3. Fill in the form
4. Click **Enregistrer** to save

---

## Common Tasks

### Add a New Client

1. Click **Clients** in sidebar
2. Click **+ Nouveau Client** button
3. Fill in client information
4. Click **Enregistrer**

### Create an Order

1. Click **Commandes** in sidebar
2. Click **+ Nouvelle Commande** button
3. Select client
4. Enter order details
5. Click **Enregistrer**

### Check Low Stock

1. Click **Stock** in sidebar
2. Filter by **Low Stock** or check minimum quantities
3. Edit quantities as needed

### Generate Report

1. Click **Rapports** in sidebar
2. Click **+ Nouveau Rapport** button
3. Select report type
4. Choose date range
5. Click **Enregistrer**

---

## Useful Django Commands

```bash
# Create new superuser
python manage.py createsuperuser

# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (WARNING: loses all data)
python manage.py migrate zero
python manage.py migrate

# Open Django shell
python manage.py shell

# Create cache tables (if using cache)
python manage.py createcachetable

# Collect static files for production
python manage.py collectstatic
```

---

## Troubleshooting

### Migration Errors

```bash
# If migrations fail, reset and re-run
python manage.py migrate zero
python manage.py migrate
```

### Permission Denied (403)

Your user role doesn't have access to that section. Log in as admin to manage user roles.

### Database Connection Error

Check that PostgreSQL is running and connection details in `settings.py` are correct.

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

---

## Production Deployment

Before deploying to production:

1. **Set DEBUG to False**
   ```python
   DEBUG = False
   ```

2. **Update ALLOWED_HOSTS**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

3. **Generate new SECRET_KEY**
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

4. **Use environment variables** for sensitive data

5. **Set up proper logging**

6. **Use production database** (PostgreSQL recommended)

7. **Serve static files** via web server or CDN

8. **Enable HTTPS** with SSL/TLS

9. **Set up backups** for database

10. **Configure email** for notifications

---

## File Structure Overview

```
fazaogestion/
├── config/          # Django configuration
├── apps/            # Application modules
│   ├── users/       # Authentication
│   ├── clients/     # Client management
│   ├── commandes/   # Order management
│   ├── stock/       # Inventory
│   ├── production/  # Production tracking
│   ├── ressources/  # Resource management
│   ├── reporting/   # Reports
│   └── dashboard/   # Dashboard
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── manage.py        # Django management script
└── requirements.txt # Python dependencies
```

---

## Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Font Awesome Icons](https://fontawesome.com/icons)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Support

For issues, errors, or questions:

1. Check the README.md for detailed documentation
2. Review the TRANSFORMATION_REPORT.md for architecture details
3. Check Django logs for error messages
4. Use Python debugger with `breakpoint()`

---

## Next Steps

1. ✅ Get the app running (you're here!)
2. Create test users with different roles
3. Add sample client and order data
4. Test different user roles and permissions
5. Customize templates to match your branding
6. Set up production database and deployment

---

**Welcome to Fazao Gestion! 🚀**

Your enterprise management system is now ready to use. Happy managing!
