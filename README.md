
# Online Auction System 

This project implements an online auction platform using Django, allowing users to bid on items in real-time. It features user registration, item listing, bidding, and auction management functionalities. Admins can manage auctions and monitor bids, while users can place bids, view auction history, and receive notifications about auction status. The system is built with a user-friendly interface and leverages modern web technologies for a seamless auction experience.

## Features

- User Registration and Authentication: Secure registration and login for buyers, sellers, and administrators.
- Auction Management: Sellers can list products with detailed descriptions, images, starting prices, and end dates. Buyers can place bids and track auction progress.
- Administrator Dashboard: Admins can manage user registrations, monitor auctions, and approve or reject user-submitted auctions.
- Responsive Design: Built with HTML, CSS, and Bootstrap to ensure a seamless user experience across devices.
- Real-Time Updates: Users can see real-time updates on auction status and bids.

## Requirements

- Python 3.x
- A text editor or IDE (e.g., VS Code, PyCharm, Sublime Text)
- Python framework (Django)
- SQLite (database)

## Installation

Clone the repository

```bash
  git clone https://github.com/omchavan01/Online-Auction-System-using-Django.git
```

Go to the project directory

```bash
  cd Online-Auction-System-using-Django
```

Create a local environment and activate it

```bash
  python -m venv env_name

  env_name/Scripts/activate
```

Install the django framework using pip

```bash
  pip install django
```

Apply migrations

```bash
  python manage.py makemigrations
  python manage.py migrate
```

Create a Superuser account to access admin interface

```bash
  python manage.py createsuperuser
```

Run the development server

```bash
  python manage.py runserver
```

Access the application by opening your browser and navigating to:

```bash
  http://127.0.0.1:8000/
```
## Authors

- [Om Chavan](https://github.com/omchavan01/)
- [Anurag Kumar](https://github.com/Anurag-747/)
- [Atharva Mishra](https://github.com/atharvamishra07/)

