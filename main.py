import os
import json
import hashlib
from datetime import datetime
import math

# Global variables
history_stack = [] 
current_user = None
screen_router = {}

# ------------------ Data Helpers ------------------


def load_data(file_path):
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([], file) 
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def update_users_data(updated_user):
    file_path = 'data/users.json'
    users = load_data(file_path)
    for idx, user in enumerate(users):
        if user['username'] == updated_user['username']:
            
            users[idx] = updated_user
            break
    save_data(file_path, users)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------ Navigation Logic ------------------


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def go_to(screen_name):
    history_stack.append(screen_name)
    screen_router[screen_name]()

def back():
    if history_stack:
        history_stack.pop()
    if history_stack:
        screen_router[history_stack[-1]]()
    else:
        main_menu()



# ------------------ Auth Logic ------------------

def register():
    print("\n📋 User Registration")
    print("-" * 30)
    file_path = 'data/users.json'

    try:
        users = load_data(file_path)
    except FileNotFoundError:
        users = []

    username = input("👤 Enter a username: ").strip()
    if any(user["username"] == username for user in users):
        print("❌ Username already exists. Please try a different one.\n")
        return

    password = input("🔒 Enter a password: ").strip()
    confirm = input("🔁 Confirm password: ").strip()

    if password != confirm:
        print("❌ Passwords do not match. Please try again.\n")
        return

    role = "user"
    hashed_pw = hash_password(password)
    next_id = max((user["id"] for user in users), default=0) + 1

    new_user = {
        "id": next_id,
        "username": username,
        "password": hashed_pw,
        "role": role,
        "bookings": []
    }

    users.append(new_user)
    save_data(file_path, users)
    print(f"\n✅ User '{username}' registered successfully with ID {next_id} as '{role}'.\n")

def login():
    print("\n🔐 User Login")
    print("-" * 30)
    file_path = 'data/users.json'

    try:
        users = load_data(file_path)
    except FileNotFoundError:
        print("❌ No users registered yet. Please register first.\n")
        return None

    username = input("👤 Enter your username: ").strip()
    password = input("🔒 Enter your password: ").strip()
    hashed_pw = hash_password(password)

    for user in users:
        if user["username"].lower() == username.lower() and user["password"] == hashed_pw:
            print(f"\n✅ Welcome back, {username}! You are logged in as '{user['role']}'.\n")
            return user

    print("❌ Invalid username or password.\n")
    return None

def logout():
    global current_user
    history_stack.clear()
    current_user = None
    print("\n🚪 You have been logged out.\n")
    main_menu()
# ------------------ Menus ------------------

def main_menu():
    clear_screen()
    global current_user
    history_stack.clear()
    current_user = None

    while True:
        print("\n🎬 Welcome to Movie Ticket Booking System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                current_user = user
                if user['role'] == 'admin':
                    go_to("admin_menu")
                else:
                    go_to("user_menu")
                break
        elif choice == '3':
            print("👋 Thank you for visiting. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select from (1, 2, or 3).")

def admin_menu():
    clear_screen()
    while True:
        print("\n🛠️ Admin Dashboard")
        print("1. Add Movie")
        print("2. Edit Movie")
        print("3. List Movies")
        print("4. Remove Movie")
        print("5. Add Showtime")
        print("6. Edit Showtime")
        print("7. List Showtimes")
        print("8. Remove Showtime")
        print("9. Logout")



        choice = input("Enter your choice (1-11): ").strip()

        if choice == '1':
            go_to("add_movie")
        elif choice == '2':
            go_to("edit_movie")
        elif choice == '3':
            go_to("view_movies")
        elif choice == '4':
            go_to("remove_movie")
        elif choice == '5':
            go_to("add_showtime")
        elif choice == '6':
            go_to("edit_showtime")
        elif choice == '7':
            go_to("view_showtimes") 
        elif choice == '8':
            go_to("remove_showtime")
        elif choice == '9':
            logout()
            break

        
        else:
            print("❌ Invalid input. Try again.")

def user_menu():
    while True:
        clear_screen()
        print("\n🎟️ User Menu")
        print("1. Browse Movies")
        print("2. View Showtimes")
        print("3. Book Seats")
        print("4. Cancel Booking")
        print("5. Logout")


        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            go_to("view_movies")
        elif choice == '2':
            go_to("view_showtimes")
        elif choice == '3':
            go_to("book_seats")
        elif choice == '4':
            go_to("cancel_booking")
        elif choice == '5':
            logout()
            break

        else:
            print("❌ Invalid input. Try again.")

# ------------------ Admin Features ------------------

def add_movie():
    clear_screen()
    """
    Admin function to add a new movie with release date and availability status.
    """
    print("\n🎬 Add New Movie")
    print("-" * 30)

    movies_file = 'data/movies.json'

    try:
        movies = load_data(movies_file)
    except FileNotFoundError:
        movies = []

    title = input("Enter movie title: ").strip()
    genre = input("Enter movie genre: ").strip()

    try:
        duration = int(input("Enter duration (in minutes): ").strip())
        if duration <= 0:
            print("❌ Duration must be a positive integer.\n")
            return
    except ValueError:
        print("❌ Invalid duration. Please enter a number.\n")
        return

    release_date_str = input("Enter release date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(release_date_str, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.\n")
        return

    available_input = input("Is the movie currently available? (yes/no): ").strip().lower()
    if available_input not in ['yes', 'no']:
        print("❌ Invalid input for availability. Please enter 'yes' or 'no'.\n")
        return
    available = available_input == 'yes'

    if any(movie['title'].lower() == title.lower() for movie in movies):
        print("❌ Movie with this title already exists.\n")
        return

    next_id = max((movie['id'] for movie in movies), default=0) + 1

    new_movie = {
        "id": next_id,
        "title": title,
        "genre": genre,
        "duration": duration,
        "release_date": release_date_str,
        "available": available
    }

    movies.append(new_movie)
    save_data(movies_file, movies)

    print(f"\n✅ Movie '{title}' added successfully with ID {next_id}.\n")
    go_to("view_movies")

def edit_movie():
    clear_screen()
    print("\n✏️ Edit Movie")
    print("-" * 30)
    movies_file = 'data/movies.json'

    try:
        movies = load_data(movies_file)
    except FileNotFoundError:
        print("❌ No movies to edit.\n")
        return

    if not movies:
        print("❌ No movies available.\n")
        return

    available_movies = [m for m in movies if m.get('available', True)]

    if not available_movies:
        print("❌ No available movies to edit.\n")
        return

    while True:
        print("\nAvailable Movies:")
        for m in available_movies:
            print(f"ID: {m['id']} | Title: {m['title']} | Genre: {m['genre']} | Duration: {m['duration']} mins | "
                  f"Release Date: {m['release_date']} | Available: {'Yes' if m.get('available', True) else 'No'}")

        inp = input("\nEnter movie ID to edit (or type 'back' to cancel): ").strip()
        if inp.lower() == 'back':
            print("Operation cancelled.\n")
            return

        try:
            movie_id = int(inp)
        except ValueError:
            print("❌ Invalid movie ID. Please enter a number.\n")
            continue

        movie = next((m for m in available_movies if m['id'] == movie_id), None)
        if not movie:
            print("❌ Movie not found among available entries. Please try again.\n")
            continue

        print(f"\nEditing Movie ID {movie['id']}")
        print(f"Current Title: {movie['title']}")
        print(f"Current Genre: {movie['genre']}")
        print(f"Current Duration: {movie['duration']} mins")
        print(f"Current Release Date: {movie['release_date']}")
        print(f"Current Available Status: {'Yes' if movie.get('available', True) else 'No'}")

        print("\nPress Enter to keep the current value.")

        new_title = input(f"Title [{movie['title']}]: ").strip()
        new_genre = input(f"Genre [{movie['genre']}]: ").strip()
        new_duration = input(f"Duration (minutes) [{movie['duration']}]: ").strip()
        new_release_date = input(f"Release Date (YYYY-MM-DD) [{movie['release_date']}]: ").strip()
        new_available = input(f"Available (yes/no) [{ 'yes' if movie.get('available', True) else 'no' }]: ").strip().lower()

        if new_title:
            movie['title'] = new_title
        if new_genre:
            movie['genre'] = new_genre
        if new_duration:
            try:
                dur = int(new_duration)
                if dur > 0:
                    movie['duration'] = dur
                else:
                    print("❌ Duration must be positive. Keeping old value.")
            except ValueError:
                print("❌ Invalid duration input. Keeping old value.")
        if new_release_date:
            movie['release_date'] = new_release_date
        if new_available in ['yes', 'no']:
            movie['available'] = (new_available == 'yes')

        save_data(movies_file, movies)
        print(f"\n✅ Movie ID {movie_id} updated successfully.\n")
        go_to("view_movies")

def remove_movie():
    clear_screen()
    print("\n🗑️ Remove Movie")
    print("-" * 30)
    movies_file = 'data/movies.json'

    try:
        movies = load_data(movies_file)
    except FileNotFoundError:
        print("❌ No movies to remove.\n")
        return

    if not movies:
        print("❌ No movies available.\n")
        return

    available_movies = [m for m in movies if m.get('available', True)]

    if not available_movies:
        print("❌ No available movies to remove.\n")
        return

    while True:
        print("\nAvailable Movies:")
        for m in available_movies:
            print(f"ID: {m['id']} | Title: {m['title']}")

        inp = input("\nEnter movie ID to remove (or type 'back' to cancel): ").strip()
        if inp.lower() == 'back':
            print("Operation cancelled.\n")
            return

        try:
            movie_id = int(inp)
        except ValueError:
            print("❌ Invalid ID. Please enter a number.\n")
            continue

        movie = next((m for m in available_movies if m['id'] == movie_id), None)
        if not movie:
            print("❌ Movie not found among available entries. Please try again.\n")
            continue

        confirm = input(f"⚠️ Are you sure you want to remove '{movie['title']}'? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("❎ Deletion cancelled.\n")
            return

        movies = [m for m in movies if m['id'] != movie_id]
        save_data(movies_file, movies)
        print(f"\n✅ Movie '{movie['title']}' removed successfully.\n")
        go_to("view_movies")

def generate_seat_labels(total_seats, seats_per_row=10):
    """
    Generate seat labels like A1, A2, ..., B1, B2, ... up to total_seats.
    """
    rows = math.ceil(total_seats / seats_per_row)
    seats = {}
    seat_count = 0

    for r in range(rows):
        row_letter = chr(65 + r)  # A, B, C...
        for c in range(1, seats_per_row + 1):
            seat_count += 1
            if seat_count > total_seats:
                break
            seat_id = f"{row_letter}{c}"
            seats[seat_id] = "available"

    return seats

def add_showtime():
    clear_screen()
    print("\n🕒 Add Showtime")
    print("-" * 30)
    movies_file = 'data/movies.json'
    showtimes_file = 'data/showtimes.json'

    try:
        movies = load_data(movies_file)
    except FileNotFoundError:
        print("❌ No movies found. Add one first.\n")
        return

    if not movies:
        print("❌ No movies available.\n")
        return

    # Show available movies
    print("\n🎬 Available Movies:")
    for m in movies:
        print(f"{m['id']}: {m['title']}")

    try:
        movie_id = int(input("Enter movie ID: ").strip())
    except ValueError:
        print("❌ Invalid movie ID.\n")
        return

    if not any(m['id'] == movie_id for m in movies):
        print("❌ Movie not found.\n")
        return

    datetime_str = input("Enter showtime datetime (YYYY-MM-DD HH:MM): ").strip()
    try:
        datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("❌ Invalid datetime format. Use YYYY-MM-DD HH:MM.\n")
        return

    try:
        num_seats = int(input("Enter number of seats: ").strip())
        if num_seats <= 0:
            print("❌ Seat number must be positive.\n")
            return
    except ValueError:
        print("❌ Invalid seat number.\n")
        return

    try:
        showtimes = load_data(showtimes_file)
    except FileNotFoundError:
        showtimes = []

    next_id = max((s['id'] for s in showtimes), default=0) + 1
    seats = generate_seat_labels(num_seats)

    showtimes.append({
        "id": next_id,
        "movie_id": movie_id,
        "datetime": datetime_str,
        "number_of_seats": num_seats,
        "seats": seats
    })

    save_data(showtimes_file, showtimes)
    print(f"\n✅ Showtime added with ID {next_id} for movie ID {movie_id} with {num_seats} labeled seats.\n")

def edit_showtime():
    clear_screen()
    print("\n✏️ Edit Showtime")
    print("-" * 30)
    showtimes_file = 'data/showtimes.json'
    movies_file = 'data/movies.json'

    try:
        showtimes = load_data(showtimes_file)
    except FileNotFoundError:
        print("❌ No showtimes to edit.\n")
        return

    if not showtimes:
        print("❌ No showtimes available.\n")
        return

    try:
        movies = load_data(movies_file)
    except FileNotFoundError:
        movies = []

    while True:
        # List showtimes with index
        print("\nAvailable Showtimes:")
        for idx, st in enumerate(showtimes, start=1):
            movie_title = next((m['title'] for m in movies if m['id'] == st['movie_id']), "Unknown Movie")
            print(f"{idx}. ID: {st['id']} | Movie: {movie_title} | Date & Time: {st['datetime']} | Seats: {st['number_of_seats']}")

        choice = input("Enter the number of the showtime to edit (or type 'back' to cancel): ").strip()
        if choice.lower() == 'back':
            print("Operation cancelled.\n")
            return

        try:
            choice_num = int(choice)
            if not (1 <= choice_num <= len(showtimes)):
                print("❌ Number out of range. Please try again.\n")
                continue
        except ValueError:
            print("❌ Invalid input. Please enter a number.\n")
            continue

        showtime = showtimes[choice_num - 1]

        # Display current values
        movie_title = next((m['title'] for m in movies if m['id'] == showtime['movie_id']), "Unknown Movie")
        print(f"\nEditing Showtime ID {showtime['id']}")
        print(f"Current Movie: {movie_title} (ID: {showtime['movie_id']})")
        print(f"Current Date & Time: {showtime['datetime']}")
        print(f"Current Number of Seats: {showtime['number_of_seats']}")

        # Edit fields
        print("\nPress Enter to keep the current value.")

        # Edit movie id
        print("\nAvailable Movies:")
        for m in movies:
            print(f"ID: {m['id']} | Title: {m['title']}")
        new_movie_id = input(f"New Movie ID [{showtime['movie_id']}]: ").strip()
        if new_movie_id:
            try:
                new_movie_id_int = int(new_movie_id)
                if any(m['id'] == new_movie_id_int for m in movies):
                    showtime['movie_id'] = new_movie_id_int
                else:
                    print("❌ Movie ID not found. Keeping old movie ID.")
            except ValueError:
                print("❌ Invalid input for movie ID. Keeping old movie ID.")

        # Edit datetime
        new_datetime = input(f"New Date & Time [{showtime['datetime']}]: ").strip()
        if new_datetime:
            showtime['datetime'] = new_datetime

        # Edit number of seats
        new_num_seats = input(f"New Number of Seats [{showtime['number_of_seats']}]: ").strip()
        if new_num_seats:
            try:
                new_num_seats_int = int(new_num_seats)
                if new_num_seats_int > 0:
                    old_num_seats = showtime['number_of_seats']
                    showtime['number_of_seats'] = new_num_seats_int

                    # Update seats dict
                    current_seats = showtime.get('seats', {})
                    if new_num_seats_int > old_num_seats:
                        # Add new seats as available
                        for i in range(old_num_seats + 1, new_num_seats_int + 1):
                            current_seats[str(i)] = "available"
                    elif new_num_seats_int < old_num_seats:
                        # Remove seats exceeding new count
                        for i in range(new_num_seats_int + 1, old_num_seats + 1):
                            current_seats.pop(str(i), None)
                    showtime['seats'] = current_seats
                else:
                    print("❌ Number of seats must be positive. Keeping old value.")
            except ValueError:
                print("❌ Invalid input for number of seats. Keeping old value.")

        # Save updated showtimes
        save_data(showtimes_file, showtimes)
        print(f"\n✅ Showtime ID {showtime['id']} updated successfully.\n")
        break


def remove_showtime():
    clear_screen()
    print("\n🗑️ Remove Showtime")
    print("-" * 30)
    showtimes_file = 'data/showtimes.json'

    try:
        showtimes = load_data(showtimes_file)
    except FileNotFoundError:
        print("❌ No showtimes to remove.\n")
        return

    if not showtimes:
        print("❌ No showtimes available.\n")
        return

    movies = []
    try:
        movies = load_data('data/movies.json')
    except FileNotFoundError:
        pass

    while True:
        for st in showtimes:
            movie_title = next((m['title'] for m in movies if m['id'] == st['movie_id']), "Unknown Movie")
            print(f"ID: {st['id']} | Movie: {movie_title} | Date & Time: {st['datetime']}")

        inp = input("Enter showtime ID to remove (or type 'back' to cancel): ").strip()
        if inp.lower() == 'back':
            print("Operation cancelled.\n")
            return

        try:
            showtime_id = int(inp)
        except ValueError:
            print("❌ Invalid showtime ID. Please enter a number.\n")
            continue

        showtime = next((s for s in showtimes if s['id'] == showtime_id), None)
        if not showtime:
            print("❌ Showtime not found. Please try again.\n")
            continue

        showtimes = [s for s in showtimes if s['id'] != showtime_id]
        save_data(showtimes_file, showtimes)
        print(f"\n✅ Showtime ID {showtime_id} removed successfully.\n")
        break


# ------------------ Shared ------------------
def view_movies(only_available=True):
    while True:
        clear_screen()
        try:
            movies = load_data('data/movies.json')
        except FileNotFoundError:
            print("❌ No movies available.\n")
            return

        if only_available:
            movies = [movie for movie in movies if movie.get("available", False)]

        if not movies:
            print("❌ No movies found.\n")
        else:
            print("\n🎬 Available Movies:")
            print("-" * 50)
            for movie in movies:
                print(f"ID: {movie['id']} | Title: {movie['title']} | Genre: {movie['genre']} | Duration: {movie['duration']} mins | Release Date: {movie['release_date']}")
            print("-" * 50)

        print("\nOptions:")
        print("1. Back")
        print("2. Logout")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            return  
        elif choice == '2':
            logout()
            return
        else:
            print("❌ Invalid input. Try again.\n")


# ------------------ User Features -----------------------
def view_showtimes(only_available=True):
    while True:
        clear_screen()
        print("\n🎥 Showtimes List")
        print("-" * 30)

        try:
            movies = load_data('data/movies.json')
            showtimes = load_data('data/showtimes.json')
        except FileNotFoundError:
            print("❌ Required data not found.\n")
            return

        if only_available:
            movies = [m for m in movies if m.get("available", False)]

        if not movies:
            print("❌ No available movies.\n")
        else:
            now = datetime.now()
            print("\n📅 Upcoming Showtimes:")
            print("-" * 60)
            for movie in movies:
                for st in showtimes:
                    if st['movie_id'] == movie['id']:
                        show_dt = datetime.strptime(st['datetime'], "%Y-%m-%d %H:%M")
                        if show_dt > now:
                            available_seats = sum(1 for s in st['seats'].values() if s == "available")
                            print(f"Movie: {movie['title']} | ID: {st['id']} | Date & Time: {st['datetime']} | "
                                  f"Total Seats: {st['number_of_seats']} | Available: {available_seats}")
            print("-" * 60)

        print("\nOptions:")
        print("1. Back")
        print("2. Logout")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            return 
        elif choice == '2':
            logout()
            return
        else:
            print("❌ Invalid input. Try again.\n")

def book_seats():
    clear_screen()
    print("\n🎫 Book Seats")
    print("-" * 30)
    movies_file = 'data/movies.json'
    showtimes_file = 'data/showtimes.json'
    users_file = 'data/users.json'

    try:
        movies = load_data(movies_file)
    except FileNotFoundError:
        print("❌ No movies available.\n")
        return

    available_movies = [m for m in movies if m.get("available", False)]
    if not available_movies:
        print("❌ No available movies to book.\n")
        return

    while True:
        print("\n🎬 Available Movies:")
        for idx, m in enumerate(available_movies, 1):
            print(f"{idx}. {m['title']} ({m['genre']}, {m['duration']} mins)")
        print("Type 'back' to return.")

        choice = input("Select a movie by number: ").strip()
        if choice.lower() == 'back':
            print("🔙 Returning to previous menu...\n")
            return

        try:
            movie_idx = int(choice)
            if 1 <= movie_idx <= len(available_movies):
                selected_movie = available_movies[movie_idx - 1]
                break
            else:
                print("❌ Invalid choice. Try again.")
        except ValueError:
            print("❌ Please enter a valid number.")

    try:
        showtimes = load_data(showtimes_file)
    except FileNotFoundError:
        print("❌ No showtimes available.\n")
        return

    now = datetime.now()
    upcoming = [
        st for st in showtimes
        if st['movie_id'] == selected_movie['id'] and datetime.strptime(st['datetime'], "%Y-%m-%d %H:%M") > now
    ]

    if not upcoming:
        print("❌ No upcoming showtimes for this movie.\n")
        return

    print(f"\n📅 Showtimes for '{selected_movie['title']}':")
    for st in upcoming:
        available_seats = sum(1 for s in st['seats'].values() if s == "available")
        print(f"ID: {st['id']} | {st['datetime']} | Total: {st['number_of_seats']} | Available: {available_seats}")
    print("Type 'back' to return.")

    while True:
        st_choice = input("Enter showtime ID to proceed: ").strip()
        if st_choice.lower() == 'back':
            return
        try:
            showtime_id = int(st_choice)
            selected_showtime = next((s for s in upcoming if s['id'] == showtime_id), None)
            if selected_showtime:
                break
            else:
                print("❌ Invalid showtime ID.")
        except ValueError:
            print("❌ Please enter a number.")

    available_seats = [seat for seat, status in selected_showtime['seats'].items() if status == "available"]
    print(f"\n💺 Available Seats ({len(available_seats)}): {', '.join(available_seats)}")

    seat_input = input("Enter seat numbers to book (comma separated) or type 'back' to cancel: ").strip()
    if seat_input.lower() == 'back':
        return

    requested_seats = [s.strip() for s in seat_input.split(",")]
    invalid_seats = [s for s in requested_seats if s not in available_seats]

    if invalid_seats:
        print(f"❌ These seats are invalid or unavailable: {', '.join(invalid_seats)}")
        return

    confirm = input(f"⚠️ Confirm booking seats {', '.join(requested_seats)}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❎ Booking cancelled.\n")
        return

   
    for seat in requested_seats:
        selected_showtime['seats'][seat] = current_user['username']

    
    try:
        save_data(showtimes_file, showtimes)
        users = load_data(users_file)
        for user in users:
            if user['username'] == current_user['username']:
                user.setdefault('bookings', []).append({
                    "movie_id": selected_movie['id'],
                    "showtime_id": selected_showtime['id'],
                    "seats": requested_seats,
                    "datetime": selected_showtime['datetime']
                })
                break
        save_data(users_file, users)
        print(f"\n✅ Seats booked successfully: {', '.join(requested_seats)}")
    except Exception as e:
        print(f"❌ Failed to book seats: {e}")


def cancel_booking():
    clear_screen()
    print("\n❌ Cancel Booking")
    print("-" * 30)

    users = load_data('data/users.json')
    for user in users:
        if user['username'] == current_user['username']:
            current_user.update(user)
            break

    if not current_user or not current_user.get("bookings"):
        print("⚠️ You have no bookings to cancel.\n")
        input("Press Enter to return to menu...")
        return

    showtimes_file = 'data/showtimes.json'

    try:
        showtimes = load_data(showtimes_file)
    except FileNotFoundError:
        print("❌ Showtime data missing.\n")
        input("Press Enter to return to menu...")
        return

    bookings = current_user.get("bookings", [])
    if not bookings:
        print("⚠️ No bookings found.\n")
        input("Press Enter to return to menu...")
        return

    print("\n🎟️ Your Bookings:")
    for idx, booking in enumerate(bookings, 1):
        showtime = next((s for s in showtimes if s['id'] == booking['showtime_id']), None)
        if not showtime:
            continue
        print(f"{idx}. Booking ID: {idx} | Movie ID: {showtime['movie_id']} | Showtime ID: {showtime['id']} | Seats: {', '.join(booking['seats'])} | DateTime: {showtime['datetime']}")

    print("Type 'back' to return.")
    choice = input("Enter the booking number to manage: ").strip()
    if choice.lower() == 'back':
        print("🔙 Returning to previous menu...\n")
        return

    try:
        booking_idx = int(choice) - 1
        if not (0 <= booking_idx < len(bookings)):
            print("❌ Invalid booking selection.\n")
            input("Press Enter to return...")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.\n")
        input("Press Enter to return...")
        return

    booking = bookings[booking_idx]
    showtime = next((s for s in showtimes if s['id'] == booking['showtime_id']), None)
    if not showtime:
        print("❌ Showtime not found. Cannot modify this booking.\n")
        input("Press Enter to return...")
        return

    print(f"\n🪑 Seats in this booking: {', '.join(booking['seats'])}")
    print("Enter seat numbers to cancel (comma separated), or 'all' to cancel the whole booking.")
    seat_input = input("Seats to cancel: ").strip().lower()

    if seat_input == 'all':
        seats_to_cancel = booking['seats']
    else:
        seats_to_cancel = [s.strip() for s in seat_input.split(',') if s.strip() in booking['seats']]
        if not seats_to_cancel:
            print("❌ No valid seats selected.\n")
            input("Press Enter to return...")
            return

    confirm = input(f"⚠️ Confirm cancellation of seat(s): {', '.join(seats_to_cancel)}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❎ Cancellation aborted.\n")
        input("Press Enter to return...")
        return

    # Mark selected seats as available
    for seat in seats_to_cancel:
        if seat in showtime['seats']:
            showtime['seats'][seat] = "available"

    # Update user's booking
    remaining_seats = [s for s in booking['seats'] if s not in seats_to_cancel]
    if remaining_seats:
        current_user['bookings'][booking_idx]['seats'] = remaining_seats
    else:
        current_user['bookings'].pop(booking_idx)

    # Save updated data
    save_data(showtimes_file, showtime)
    update_users_data(current_user)

    print(f"\n✅ Seat(s) {', '.join(seats_to_cancel)} canceled successfully.\n")
    input("Press Enter to return to menu...")

# ------------------ Route Registration ------------------

screen_router = {
    "main_menu": main_menu,
    "admin_menu": admin_menu,
    "user_menu": user_menu,
    "add_movie": add_movie,
    "edit_movie": edit_movie,
    "remove_movie": remove_movie,
    "view_movies": view_movies,
    "add_showtime": add_showtime,
    "edit_showtime": edit_showtime,
    "remove_showtime": remove_showtime,


    "view_showtimes": view_showtimes,
    "book_seats": book_seats, 
    "cancel_booking": cancel_booking,



   
}

# ------------------ Start Application ------------------

if __name__ == "__main__":
    main_menu()
