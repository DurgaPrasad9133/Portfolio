# Bus Tickets Booking API Documentation

## Authentication
- JWT-based authentication
- Register: `POST /tickets/register/`
- Login: `POST /tickets/auth/login/` (returns access/refresh tokens)
- Refresh: `POST /tickets/auth/refresh/`

## Endpoints

### User Registration
- `POST /tickets/register/`
- Body: `{ username, password, phone_number, age, address, gender, role, email }`
- Response: Success or error message

### Login
- `POST /tickets/auth/login/`
- Body: `{ username, password }`
- Response: `{ access, refresh }` tokens

### Bus Search
- `GET /tickets/buses/search/?starts_from=...&going_to=...&running_day=...`
- Response: List of buses matching criteria

### Seat Availability
- `GET /tickets/buses/seat-availability/?bus_id=...&trip_date=...`
- Response: `{ available_lower_seats, available_upper_seats }`

### Bookings
- `POST /tickets/bookings/`
- Body: `{ booked_by, booked_Bus, status, seat_no, seat_position, trip_date }`
- Response: Success or error (e.g., seat already booked)
- Requires authentication
- `GET /tickets/bookings/` to list bookings

### List Passengers
- `GET /tickets/passengers/`
- Response: List of passengers

### List Buses
- `GET /tickets/buses/`
- Response: List of buses

## Notes
- All endpoints return JSON responses.
- Use the `Authorization: Bearer <access_token>` header for protected endpoints.
- CORS is enabled for all origins (for development).
