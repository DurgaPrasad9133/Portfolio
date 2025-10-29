# Frontend API Guide for Bus Tickets Booking

## Base URL
All API calls must start with `/tickets/` (e.g., `http://localhost:8000/tickets/`).

## Endpoints

### User Registration
- `POST /tickets/register/`
- Body: `{ username, password, phone_number, age, address, gender, role, email }`

### Login (JWT)
- `POST /tickets/auth/login/`
- Body: `{ username, password }`
- Response: `{ access, refresh }` tokens

### Refresh Token
- `POST /tickets/auth/refresh/`
- Body: `{ refresh }`

### List Passengers
- `GET /tickets/passengers/`

### List Buses
- `GET /tickets/buses/`

### Bus Search
- `GET /tickets/buses/search/?starts_from=...&going_to=...&running_day=...`

### Seat Availability
- `GET /tickets/buses/seat-availability/?bus_id=...&trip_date=...`

### Bookings
- `GET /tickets/bookings/` (list)
- `POST /tickets/bookings/` (create)
- Body: `{ booked_by, booked_Bus, status, seat_no, seat_position, trip_date }`
- Requires `Authorization: Bearer <access_token>` header

## Example Frontend Code (JavaScript/Fetch)

```js
// Register user
fetch('http://localhost:8000/tickets/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password, ... })
})

// Login
fetch('http://localhost:8000/tickets/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
})

// Get buses
fetch('http://localhost:8000/tickets/buses/')

// Search buses
fetch('http://localhost:8000/tickets/buses/search/?starts_from=CityA&going_to=CityB&running_day=MONDAY')

// Check seat availability
fetch('http://localhost:8000/tickets/buses/seat-availability/?bus_id=1&trip_date=2025-09-30T10:00:00Z')

// Create booking (with JWT)
fetch('http://localhost:8000/tickets/bookings/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <access_token>'
  },
  body: JSON.stringify({ booked_by, booked_Bus, ... })
})
```

## Notes
- Always use trailing slashes (`/`) in URLs.
- Always use the `/tickets/` prefix.
- Use correct HTTP methods (GET, POST).
- For protected endpoints, include the JWT token in the `Authorization` header.

