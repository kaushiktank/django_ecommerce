## Django eCommerce site

I have used the Django for the bcakend and HTML template for the frontend part. The site contain the below functionality

### Admin Functionality
- Add products from the admin panel.
    - Add product details like name, descripton, images, price, available inventory, etc... from the Django's Admin panel.
- Manage purchases
- Manage users

### User functionality
- Search products
- Filter products
    - Filter by category
    - Filter by ratting
    - Filter by company
- Add Products to the cart, and purchases it.
- Able to Add and manage addresses for the delivery.

### System emails
Users will receive multiple system emails as per the user's operations
- Welcome email
- Product purchase email

I have integrated the celery for sending all the system memails. For the middleman I have used the rabbit-mq server as a message broker.
