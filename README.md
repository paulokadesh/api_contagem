# Inventory Management API

This is a Python-based REST API for inventory management, built with Flask and MySQL.

## Project Structure

```
.
├── app/
│   ├── config/
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── user.py
│   │   └── inventory.py
│   └── routes/
│       ├── auth.py
│       └── inventory.py
├── .env
├── main.py
├── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file with the following variables:
```
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
APP_PORT=8082
```

5. Run the application:
```bash
python main.py
```

## API Endpoints

### Authentication
- POST `/login` - User authentication

### Inventory Management
- POST `/verificar_codigo` - Verify and register product code
- POST `/buscar_estoque` - Get product stock information
- POST `/conferencias` - Get conference counts

## Features
- User authentication
- Product verification
- Stock management
- Conference tracking
- MySQL database integration
- CORS support 