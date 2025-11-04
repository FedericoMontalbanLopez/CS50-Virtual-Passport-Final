import os

from dotenv import load_dotenv
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

load_dotenv() 

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Renders the appropriate home page based on login status."""
    if session.get("user_id"):
        # If logged in, redirect to the Passport Dashboard
        return redirect("/passport")
    else:
        # If logged out, show the welcome page
        return render_template("home.html")

@app.route("/passport")
@login_required
def passport():
    """Welcome page. Show user's passport summary, including stamp count."""

    user_id = session["user_id"]
    # Query the username
    user_rows = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = user_rows[0]["username"].capitalize() if user_rows else "Traveler"

    # Query the count of stamps
    stamp_count_rows = db.execute("SELECT COUNT(id) AS total FROM stamps WHERE user_id = ?", user_id)
    stamp_count = stamp_count_rows[0]["total"] if stamp_count_rows else 0
    
    return render_template("passport.html", username=username, stamp_count=stamp_count)

@app.route("/history")
@login_required
def history():
    """Show history of stamps with additive pagination and media statistics."""
    
    # 1. Get current total stamps to display (default to 5)
    try:
        current_total = int(request.args.get("offset", 5))
        if current_total < 5:
            current_total = 5
    except ValueError:
        current_total = 5

    user_id = session["user_id"]
    limit = current_total 

    # 2. FETCH PAGINATED STAMPS (2 placeholders, 2 values: user_id, limit)
    stamps = db.execute(
        "SELECT id, location_name, source, means, timestamp FROM stamps "
        "WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        user_id, limit
    )

    # Process stamps to extract only the date in Python
    for stamp in stamps:
        # We split by space and take the first element (the date)
        stamp['date_only'] = stamp['timestamp'].split(' ')[0]

    # 3. FETCH MEDIA STATISTICS (1 placeholder, 1 value: user_id)
    media_stats = db.execute(
        "SELECT means, COUNT(means) AS count FROM stamps "
        "WHERE user_id = ? GROUP BY means ORDER BY count DESC",
        user_id
    )

    real_fiction = db.execute(
        "SELECT location_type, COUNT(location_type) AS count FROM stamps "
        "WHERE user_id = ? GROUP BY location_type ORDER BY count DESC",
        user_id     
    )

    # 4. CHECK FOR MORE STAMPS (3 placeholders, 3 values: user_id, 1, limit)
    # This query uses 3 placeholders for security and filtering.
    next_stamps_check = db.execute(
        "SELECT id FROM stamps WHERE user_id = ? "
        "ORDER BY timestamp DESC LIMIT ? OFFSET ?",
        user_id, 1, limit
    )

    has_more = len(next_stamps_check) > 0
    next_offset = limit + 5
    stamps_loaded = limit 

    return render_template(
        "history.html",
        stamps=stamps,
        has_more=has_more,
        next_offset=next_offset,
        stamps_loaded=stamps_loaded,
        media_stats=media_stats,
        real_fiction =real_fiction
    )

@app.route("/delete_stamp", methods=["POST"])
@login_required
def delete_stamp():
    """Deletes a single stamp entry using the stamp_id provided via the form."""
    
    # 1. Ensure the stamp ID was provided
    stamp_id_str = request.form.get("stamp_id")
    if not stamp_id_str:
        flash("Error: No stamp ID provided for deletion.", "danger")
        return redirect("/history")

    try:
        # 2. Convert ID to integer
        stamp_id = int(stamp_id_str)
        user_id = session["user_id"]

        # 3. Execute the DELETE query
        # CRITICAL: We ensure the stamp belongs to the logged-in user for security.
        rows_deleted = db.execute(
            "DELETE FROM stamps WHERE id = ? AND user_id = ?",
            stamp_id,
            user_id
        )

        if rows_deleted > 0:
            flash("Stamp successfully deleted from your passport!", "success")
        else:
            # This happens if the stamp ID was invalid or didn't belong to the user
            flash("Error: Could not find or delete that stamp.", "danger")

    except ValueError:
        flash("Error: Invalid stamp ID format.", "danger")
    except Exception as e:
        flash(f"Database error during deletion: {e}", "danger")
        
    # Redirect back to the history page (where the deletion form was)
    return redirect("/history")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    
    # Handle POST request
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        # Convert username to lowercase to match to database storage
        username = request.form.get("username").lower()
                
        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(
            user[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)
        
        # Log user in by storing their id in session
        session["user_id"] = user[0]["id"]
        return redirect("/passport")
    
    # Handle GET request
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Handle POST request
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 400)
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 400)
        
        # Ensure password is at least 8 characters
        password = request.form.get("password")
        if len(password) < 8:
            return apology("Password must be at least 8 characters", 400)
        
        #ensure confirmation was submitted
        confirmation = request.form.get("confirmation")
        if not confirmation or password != confirmation:
            return apology("Passwords do not match", 400)
        
        # Hash password 
        hash = generate_password_hash(request.form.get("password"))
        username = request.form.get("username").lower()
        
        # Try to insert new user into users table
        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES(?, ?)",
                username,
                hash,
            )
        except Exception:
            return apology("Username already exists", 400)
        
        # Query database for username
        rows = db.execute("SELECT id FROM users WHERE username = ?", username)
        
        # Log user in by storing their id in session
        session["user_id"] = rows[0]["id"]

        flash("Successfully registered!")
        return redirect("/passport")
    
    # Handle GET request
    else:
        return render_template("register.html")
    
@app.route("/pin", methods=["POST"])
@login_required
def pin():
    """Handles the form submission from the map.html to save a new stamp."""

    # Retrieve data from the submitted form
    location_type = request.form.get("location_type")
    latitude_str = request.form.get("latitude")
    longitude_str = request.form.get("longitude")
    location_name = request.form.get("location_name")
    source = request.form.get("source")
    means = request.form.get("means")  
    user_id = session["user_id"]

    # Validation Checks
    if not location_type or not location_name or not source:
        return apology("Must provide a location type, a location name and source of fiction", 400)

    try:
        # Convert string coordinates to floats for database storage and validation
        latitude = float(latitude_str)
        longitude = float(longitude_str)
    except (ValueError, TypeError):
        return apology("Invalid coordinates received. Please click on the map.", 400)

    # Simple check to ensure coordinates are within valid range 
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return apology("Invalid geographic coordinates.", 400)


    # Insert the new stamp into the 'stamps' table
    try:
        db.execute(
            "INSERT INTO stamps (user_id, location_type, location_name, source, means, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?)",
            user_id,
            location_type,
            location_name,
            source,
            means,
            latitude,
            longitude
        )
        flash(f"Passport stamped for {location_name} (from {source})!")
        return redirect("/passport")

    except Exception:
        # Catch unexpected database errors
        return apology("An unexpected database error occurred while stamping your passport.", 500)
    

@app.route("/map")
@login_required
def map_page():
    user_id = session["user_id"]
    
    # Query all stamps for the current user
    stamps = db.execute(
        "SELECT location_type, location_name, source, latitude, longitude FROM stamps WHERE user_id = ?", 
        user_id
    )

    # NEW LOGIC: Find the last pinned location (the first one since we ordered by DESC in the original query)
    last_stamp = db.execute(
        "SELECT latitude, longitude FROM stamps "
        "WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1",
        user_id
    )
    
    # Set default coordinates (e.g., center of US) if no stamps exist
    center_lat = last_stamp[0]["latitude"] if last_stamp else 40
    center_lon = last_stamp[0]["longitude"] if last_stamp else -98
    
    return render_template(
        "map.html", 
        stamps=stamps, 
        center_lat=center_lat, 
        center_lon=center_lon
    )


@app.route("/plan")
@login_required
def plan():
    """Renders the AI Adventure Planner page."""

    # Securely retrieve the key from the environment variables
    gemini_key = os.getenv("GEMINI_API_KEY")

    # Renders the HTML template containing the client-side Gemini API call
    return render_template("plan.html", gemini_key=gemini_key)
