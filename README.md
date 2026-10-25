# Container Slot Booking System

A small Flask app for booking hourly truck slots at a container yard, with user accounts and an admin view of all bookings.

**Status:** early learning prototype · runs locally · **not production-ready** (see [Limitations](#limitations-and-next-steps)) · no QR verification or gate control

## Overview

Transport operators register, log in and book an hourly slot for a truck. Each hour accepts at most 3 trucks, so a full slot is refused and the user is asked to pick another time. An admin can see every booking in one table.

**Problem it addresses:** keeping one shared record of how many trucks are expected at the yard each hour, so a slot cannot be overbooked.

**Intended users:** transport operators (book a slot) and yard admins (see the day's bookings).

## What is implemented

- Registration and login with Flask sessions. The booking page requires a login.
- A booking form: driver name, truck number, container size (20 ft or 40 ft), date and time. The time is rounded down to the hour.
- A capacity rule of 3 trucks per date and hourly slot, with a "Slot Full" response when it is reached.
- A confirmation page after a successful booking.
- An admin page, shown only to the user named `admin`, listing all bookings.

It does **not** include QR passes, gate verification, hardware control, billing or notifications. Related: [YardFlow](https://github.com/kavyaraval543-gif/yardflow) is a separate case study on yard entry and gate verification.

## Tech stack

Python, Flask, SQLite, and Tailwind CSS (loaded from the Tailwind CDN).

## Run it locally

```bash
pip install -r requirements.txt
python database.py      # creates bookings.db with the users and bookings tables
python app.py           # http://127.0.0.1:5000
```

1. Open `/register` and create an account.
2. To see the admin page, register a user named `admin`, then open `/admin`.

There is no `.env` file and no configuration. The database file is created next to the app.

## Limitations and next steps

These are known gaps, and the app should not be deployed or used with real data until they are fixed.

- **Passwords are stored in plain text** and compared directly. They should be hashed (for example with Werkzeug's `generate_password_hash`).
- **The session secret key is hard-coded** in `app.py`. It should come from an environment variable.
- **Anyone can register as `admin`** and see all bookings. There is no separate admin role.
- The app runs with `debug=True`, which must be off in any shared environment.
- The slot-capacity check and the insert are not atomic, so two simultaneous requests could overbook a slot.
- No tests, no input validation beyond the browser form, and no way to cancel or edit a booking.
- Next: fix the security items above, add cancellation and a seeded admin role, and add tests for the capacity rule.
