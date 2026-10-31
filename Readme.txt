Little Lemon API endpoints

GET, POST: /api/menu/
GET, PUT, PATCH, DELETE: /api/menu/{id}/
GET, POST: /api/bookings/
GET, PUT, PATCH, DELETE: /api/bookings/{id}/
POST: /api/registration/
POST: /api-token-auth/

Registration accepts username, email, and password and returns an authentication token.
Send authenticated API requests with the header: Authorization: Token <token>
Menu reads are public. Menu writes and all booking API requests require authentication.