

---

```md
# 🎬 AI Movie Booking Chatbot

A full-stack GenAI-powered movie booking system built with:

- ⚡ FastAPI (Backend)
- 🧠 OpenAI (Chat + Tool Calling)
- 🗄️ Supabase (Database - PostgreSQL)
- 🎨 Vanilla HTML + JS (Frontend)

Users can:
- Get movie recommendations
- View shows & theatres
- Check seat availability
- Book tickets via AI chat

---

# 🚀 Features

- 🤖 AI chatbot for movie booking
- 🎥 Real-time movies, shows, and seats from database
- 🪑 Seat availability tracking
- 📅 Show timing selection
- 📦 Booking system (end-to-end flow)
- 🔧 Tool calling (OpenAI → Backend functions)

---

# 🏗️ Project Structure

```

movie-booking-app/
│
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── movies.py
│   │   ├── shows.py
│   │   ├── bookings.py
│   │   └── chat.py
│   ├── services/
│   │   ├── booking_service.py
│   │   └── openai_service.py
│   ├── schemas/
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── chat.html
│   └── js/script.js
│
└── README.md

````

---
git remote add origin https://github.com/dhruvDS13/Movie-Booking-With-Chatbot.git
git add .
git commit -m "your message"
git push
# ⚙️ Setup (Local Development)

### 1. Go to backend
```powershell
cd backend
````

### 2. Create virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Setup environment variables

Create `.env` file inside `backend/`:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

---

### 5. Run server

```powershell
uvicorn main:app --reload --port 9000
```

👉 Open in browser:

```
http://127.0.0.1:9000
```

---

# 🧪 API Endpoints

### Chat

```
POST /chat
```

### Movies

```
GET /movies
```

### Shows

```
GET /shows
```

### Seats

```
GET /shows/{show_id}/seats
```

### Book Tickets

```
POST /bookings
```

### User Bookings

```
GET /bookings/{user_id}
```

---

# 🧠 How AI Works

1. User sends message → `/chat`
2. Backend sends:

   * System prompt
   * Chat history
   * Available tools
3. OpenAI decides:

   * Normal reply OR
   * Call tool (get_movies, get_shows, etc.)
4. Backend executes tool
5. AI responds with final answer

---

# 🗄️ Database (Supabase)

Tables used:

* `movies`
* `theatres`
* `shows`
* `seats`
* `bookings`

---

# 🔐 RLS (Row Level Security)

Currently:

* Disabled (for development)

👉 In production:

* Enable RLS
* Add policies for user-based access

---

# ⚠️ Common Issues

### 1. OpenAI not working

* Check `.env`
* Restart server
* Ensure correct API key

---

### 2. "Offline mode" showing

* API key not loaded
* Wrong virtual environment

---

### 3. Import error (openai)

```bash
pip install openai
```

---

# 🚀 Production Deployment

### Frontend

* Deploy on: **Vercel**

### Backend

* Deploy on: **Northflank / Render / Railway**

### Database

* Supabase (already cloud hosted)

---

# 🔥 Future Improvements

* 🔐 User authentication (Supabase Auth)
* 💳 Payment integration (Razorpay/Stripe)
* 📊 Admin dashboard
* ⚡ Redis for chat memory
* 🎯 Recommendation engine (ML model)

---

# 👨‍💻 Author

Dhruv Kumar Singh
B.Tech CSE (Data Science)

---

# ⭐ Tip

Start simple:

1. Test `/movies`
2. Then `/shows`
3. Then `/chat`

Don’t jump directly to AI debugging.

---

```

---

If you want next upgrade, I can give you:

- ✅ Clean frontend UI (BookMyShow style)
- ✅ Full Supabase integration (production ready)
- ✅ AI booking flow with confirmations

Just say: **"make it production level"** 🚀
```
