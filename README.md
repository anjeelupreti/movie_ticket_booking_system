# 🎟️ Movie Ticket Booking System (Python CLI)

A fully functional **command-line based Movie Ticket Booking System** built entirely with **Python**, using the **standard library only**. This project supports both `User` and `Admin` roles, persistent data storage using JSON files, and a clean, interactive CLI experience.

---

## 📌 Project Overview

This application simulates a real-world movie ticket booking system where:

- 👤 **Users** can:
  - Register and login
  - Browse available movies
  - View showtimes
  - Book seats
  - Cancel their bookings (*entire booking — seat-wise cancellation is not yet implemented*)

- 🛠️ **Admins** can:
  - Login with default credentials
  - Add or remove movies
  - Add showtimes for movies
  - View movie listings

All actions are executed within a single file: `main.py`.

---

## 📦 Setup & Installation

### 1. Clone the Repository

- git clone https://github.com/anjeelupreti/movie_ticket_booking_system.git
- cd movie-ticket-booking
- python main.py


---

## 🔐 Default Admin Access

The system comes with a pre-registered admin:

- Username: admin
- Password: admin


This credential is stored in `data/users.json`, which is the only JSON file present initially. All other files (`movies.json`, `showtimes.json`) are created when new data is added by the admin or users.

---

## 🧑‍💼 Roles and Features

### 👤 User Role

- ✅ Register a new account  
- ✅ Login to access user menu  
- ✅ View available movies  
- ✅ Check showtimes for each movie  
- ✅ Book seats for a selected showtime  
- ✅ Cancel a booking 


### 🛠 Admin Role

- ✅ Login using default credentials  
- ✅ Add movies to the system  
- ✅ Remove movies from the list  
- ✅ Add showtimes for any movie  
- ✅ View list of all movies  

---

## 🗃️ Project Structure
### movie_ticket_booking_system

#### data
- **users.json**  
  *Admin + user login info (preloaded with admin)*

- **movies.json**  
  *Created when admin adds movies*

- **showtimes.json**  
  *Created when admin adds showtimes*

#### main.py  
*All logic and interaction live in one file*

#### README.md  
*You're reading it!*

> 🔸 `users.json` is the only file created beforehand  
> 🔸 All other data files are auto-generated when needed

---

## 🖥️ Requirements

- Python **3.7+**  
- No external libraries required  


---

## 📚 Used Python Standard Libraries

- `json` — for persistent data  
- `os` — for cross-platform terminal clearing  
- `getpass` — to securely input passwords  
- `time` — for short interactive delays  
- `sys` — to exit and detect environment  

---

## 🧠 System Design Decisions

### Single File Structure

All code is written in `main.py` for simplicity.

### JSON for Persistence

- `users.json` stores user/admin data and bookings.  
- `movies.json` stores movie entries.  
- `showtimes.json` stores showtimes and seat maps.  

Files (except `users.json`) are created dynamically.

### Minimalist CLI UX

Simple menus and clear prompts ensure usability without needing GUI.

### No Third-Party Libraries

100% pure Python. Easy to run anywhere without installation overhead.

---

## 🤖 Use of AI Tools & Attribution

AI assistance (ChatGPT) was used:

- For refactoring, naming, and designing menus.  
- To improve validations, UX flow, and error handling.  

But all logic, testing, structural decisions, and incremental improvements were made manually — as part of a user-centered iterative design mindset.

---

## 📝 Author Notes

This system was designed with real-world user experience in mind. From input validation to responsive prompts, every part was imagined as if a user was navigating it live. Admin workflows are streamlined for quick movie/showtime updates, while user flows simulate actual ticket systems — all within a terminal interface.

