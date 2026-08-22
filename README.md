# ☕ Kiarash Cafe — Coffee Shop Web Application

<div align="center">


[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge\&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge\&logo=python)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge\&logo=mongodb)](https://www.mongodb.com/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge\&logo=microsoft-sql-server)](https://www.microsoft.com/en-us/sql-server/)
[![GSAP](https://img.shields.io/badge/GSAP-88CE02?style=for-the-badge\&logo=greensock)](https://greensock.com/gsap/)

</div>

---

## 📖 About The Project

**Kiarash Cafe** is a full-featured web application for a modern coffee shop.

Customers can browse the menu, view detailed products with multiple pricing options, register and log in, manage their shopping cart, and place and track orders.

### 🎯 Key Features

| Feature                    | Description                                                           |
| -------------------------- | --------------------------------------------------------------------- |
| 🍽️ **Dynamic Menu**       | Browse categories with beautiful product cards                        |
| 💰 **Multi-Price Support** | Products with variants such as single/double shot and different sizes |
| 🛒 **Shopping Cart**       | Add, remove, and update product quantities                            |
| 👤 **User Accounts**       | Register, login, and manage user profiles                             |
| 📋 **Order History**       | View previous orders and their current status                         |
| 🎨 **Art Gallery**         | Visual showcase of the cafe's products and atmosphere                 |
| 📱 **Responsive Design**   | Fully responsive interface for desktop, tablet, and mobile            |

---

## 🎨 Color Palette

| Color           | Hex Code  | Usage                            |
| --------------- | --------- | -------------------------------- |
| 🌿 Forest Green | `#0A5C36` | Primary color, headers, buttons  |
| 🍃 Sage Green   | `#225E2E` | Secondary color and hover states |
| 🧈 Cream        | `#FEF1B4` | Backgrounds and highlights       |
| ✨ Gold          | `#C8973B` | Accents and badges               |
| 🤎 Espresso     | `#2B1B12` | Text and dark elements           |

---

## 🏗️ Project Structure

```text
kiarash-coffe/
├── apps/
│   ├── core/                  # Home, About, Contact, Art
│   ├── accounts/              # Register, Login, Profile
│   ├── menu/                  # Menu listing & product details
│   └── orders/                # Cart, Checkout, Order History
│
├── templates/                 # HTML templates
├── static/                    # CSS, JavaScript, Images, Videos
├── kiarash_cafe/              # Django project settings
│
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management script
└── README.md                  # Project documentation
```

---

## 🛠️ Technologies Used

### Backend

* **Django 6.1** — Python web framework
* **MongoDB** — Menu and product data
* **SQL Server** — User and order data
* **PyMongo** — MongoDB connection
* **PyODBC** — SQL Server connection

### Frontend

* **Bootstrap 5** — Responsive layout
* **GSAP** — Professional animations
* **Font Awesome** — Icons
* **Custom CSS** — Coffee-shop themed design

### Development

* **Python 3.14+**
* **Visual Studio Code**
* **Git & GitHub**

---

## 📸 Demo

<div align="center">

<img src="demo/demo.gif" alt="Kiarash Cafe Demo" width="100%">

</div>

## 🚀 Installation & Setup

### Prerequisites

Before running the project, make sure you have the following installed:

* Python 3.14+
* MongoDB running on `localhost:27017`
* SQL Server running on `localhost\sqlserver2025`
* Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/Kiarash-sabbaghii-giit/kiarash_coffee.git
cd ...
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


> ⚠️ **Important:** Never commit your `.env` file or secret keys to GitHub.

---

### 4. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the instructions in the terminal to create your admin account.

---

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

---

### 7. Run the Development Server

```bash
python manage.py runserver
```

---

### 8. Access the Application

* 🌐 **Website:** http://127.0.0.1:8000/
* 🔐 **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 📊 Database Schema

### 🍃 MongoDB Collections

MongoDB is used for storing menu and product information.

| Collection           | Description                  |
| -------------------- | ---------------------------- |
| `hot_drinks`         | Hot beverages with variants  |
| `cold_drinks`        | Cold beverages with variants |
| `Seasonal_Promotion` | Seasonal specials            |
| `matcha`             | Matcha products              |
| `healthy_menu`       | Healthy menu options         |
| `Brewed_coffee`      | Brewed coffee products       |
| `tea`                | Tea and herbal drinks        |
| `elcless`            | Silent menu                  |
| `cakes`              | Cakes and desserts           |
| `testbar`            | Toast bar products           |
| `crosan_sandwich`    | Croissant sandwiches         |
| `popsickle`          | Popsicles                    |

---

### 🗄️ SQL Server Tables

SQL Server is used for user accounts, shopping carts, and order management.

| Table        | Description                                             |
| ------------ | ------------------------------------------------------- |
| `Users`      | User accounts including name, email, phone, and address |
| `Orders`     | Order records including user, total price, and status   |
| `OrderItems` | Individual items belonging to orders                    |
| `CartItems`  | Temporary shopping cart items                           |

---

## 📦 Internal API Endpoints

| Endpoint             | Method | Description                      |
| -------------------- | ------ | -------------------------------- |
| `/menu/add-to-cart/` | `POST` | Add an item to the shopping cart |
| `/menu/cart-count/`  | `GET`  | Get the current cart item count  |
| `/orders/cart/`      | `GET`  | View the shopping cart           |
| `/orders/checkout/`  | `POST` | Place an order                   |
| `/orders/history/`   | `GET`  | View order history               |

---

## 🎯 Future Improvements

* [ ] Payment gateway integration
* [ ] Email notifications for order status
* [ ] Admin dashboard for order management
* [ ] User review and rating system
* [ ] Loyalty program with points
* [ ] Mobile application using React Native
* [ ] Real-time order tracking
* [ ] Multi-language support (Persian / English)
* [ ] Online table reservation
* [ ] Advanced product search and filtering

---

## 🤝 Contributing

Contributions are welcome and appreciated!

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes

```bash
git commit -m "Add some AmazingFeature"
```

4. Push the branch

```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request

---

## 📄 License

This project is distributed under the **MIT License**.

See the `LICENSE` file for more information.

---


<div align="center">

### Made with ❤️ and ☕ by Kiarash Cafe Team

</div>
