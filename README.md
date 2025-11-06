# 🌍 Fictional Passport

**CS50 Final Project | 2025**  
**Author:** Federico Montalbán López

---

## Project Concept & Theme

**Fictional Passport** is a web application that tracks journeys made through imagination — letting users log both **real** and **fictional** destinations inspired by the stories they love.  

From *Venice* to *Middle Earth*, from *Albuquerque* to *Gotham City*, users can record every place they’ve "visited" through books, comics, movies, series, or songs.

This web is inspired by a line from the Dao De Jing:

> _"They know the world without even going out the door."_ (poem 47, translated by Thomas Cleary)


---

## Technical Stack

- **Backend:** Python, Flask  
- **Database:** SQLite3  
- **Frontend:** HTML, Jinja, JavaScript, Tailwind CSS (for responsive and modern design)  
- **External APIs:**  
  - **Google Gemini API** (AI-powered travel planner)  
  - **Leaflet.js** (interactive world map)

---

## Key Features & Technical Achievements

### 1. AI Adventure Planner (Gemini API Integration)


- **Client-Side Fetch:** The Gemini API is called securely from the browser using `fetch`, ensuring fast, non-blocking responses.  
- **System Persona:** The LLM is instructed to act as a *“whimsical and knowledgeable Fiction Travel Agent.”*  
- **Grounding:** Google Search grounding ensures accurate, up-to-date references to real books, movies, and series.  
- **Security:** API key loaded from a local `.env` file using `python-dotenv`; never committed to GitHub.

---

### 2. Interactive Map (Leaflet.js)
A creative “stamping” interface that visually tracks each destination.

- **Dynamic Centering:** Automatically centers on the user’s most recent stamp.  
- **Geocoding Search:** Users can search for a city (e.g., *“Albuquerque”*) to quickly place a pin.  
- **Fictional Mode:** Choosing “Fictional” automatically drops a random pin within a defined square (of pure water) in the midlle of Atlantic Ocean.

---

### 3. Data Management & User Interface
Secure, responsive, and optimized for smooth performance.

- **Responsive History Log:** Uses SQL `LIMIT` and `OFFSET` to implement pagination that loads entries in blocks of 5 without reloading the page.  
- **Data Insights:** Displays statistics showing the user’s travel frequency by media type (*Book*, *Movie*, *TV Series*) and real destinatios vs. fictional destinations. 
- **Security & Deletion:** Passwords are hashed using `generate_password_hash`. Stamps can only be deleted by the logged-in user who created them.

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/FedericoMontalbanLopez/CS50-Virtual-Passport-Final.git
cd CS50-Virtual-Passport-Final
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate     # On Windows: .\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install Flask flask-session cs50 werkzeug python-dotenv
```

### 4. Database Setup
- Create an empty SQLite file named `project.db` in the project root.
- **Initialize the tables** by executing the SQL commands in `schema.sql`.

```bash
sqlite3 project.db < schema.sql
```


### 5. Configure Your Gemini API Key
Create a `.env` file in the project root:
```bash
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 6. Run the Application
```bash
flask run
```
Access the app at: http://127.0.0.1:5000

## Demo 

**Demo Video:** https://youtu.be/MBBFH-Dfjtg  


## Reflection

**Fictional Passport** blends imagination and technology, turning every story into a destination.  
This project combines **web development, AI integration, and secure data handling** to celebrate the worlds we explore through art, not just geography.


