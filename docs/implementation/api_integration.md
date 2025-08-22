# External API Integration – Cinemix

This document explains how Cinemix integrates with the **TMDb API** to provide movie data, trailers, and search functionality.  
It covers endpoints, caching, rate limiting handling, error responses, and the exact integration flow in our backend.

---

## 🎯 Purpose

Cinemix does not expose TMDb directly to the frontend.  
Instead, our backend acts as a **proxy layer** with caching, error handling, and rate limiting strategies.  
This ensures:  
- Stable experience regardless of TMDb downtime  
- Reduced API quota usage (via Redis cache)  
- Consistent response format for frontend (using DTOs)

---

## 🔑 Key Points

- ✅ **API Key Security** → TMDb key hidden in backend (`.env`), never exposed to frontend  
- ✅ **Unified Interface** → Cinemix apps only call `/api/search` & `/api/details`  
- ✅ **Caching Layer** → Redis reduces TMDb requests, speeds up responses  
- ✅ **Error Handling** → Centralized error messages and rate-limit handling  
- ✅ **DTO Models** → All responses validated/structured with Pydantic models

---

## 🌍 Endpoints Overview

### 1️⃣ `/api/search`

**Method:** `GET`  
**Query Params:**  
- `query` (string, required) → Search keyword  

**Description:**  
Returns an array of matching movies/shows from TMDb. Results cached for **1 hour** in Redis.

**DTO:** `SearchResponse` (with nested `SearchResult` items)

**Example Request:**  
```http
GET /api/search?query=Inception
```

**Example Response:**  
```json
{
  "results": [
    {
      "id": 27205,
      "title": "Inception",
      "release_date": "2010-07-15",
      "overview": "A thief who steals corporate secrets...",
      "poster_path": "/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg"
    }
  ]
}
```

---

### 2️⃣ `/api/details/{movie_id}`

**Method:** `GET`  
**Path Param:**  
- `movie_id` (integer, required) → TMDb movie ID  

**Description:**  
Returns **full details** for one movie (or show). Cached for **24 hours** in Redis.

**DTO:** `MovieDetails`

**Example Request:**  
```http
GET /api/details/27205
```

**Example Response:**  
```json
{
  "id": 27205,
  "title": "Inception",
  "release_date": "2010-07-15",
  "runtime": 148,
  "genres": [
    { "id": 28, "name": "Action" },
    { "id": 878, "name": "Science Fiction" }
  ],
  "overview": "Cobb, a skilled thief..."
}
```

---

### 3️⃣ `/api/trailer/{movie_id}` *(Optional / v2 Feature)*

**Method:** `GET`  
**Path Param:**  
- `movie_id` (integer, required) → TMDb movie ID  

**Description:**  
Fetches the official YouTube trailer link from TMDb video data.

**DTO:** `TrailerResponse`

**Example Request:**  
```http
GET /api/trailer/27205
```

**Example Response:**  
```json
{
  "id": 27205,
  "title": "Inception",
  "trailer_url": "https://www.youtube.com/watch?v=YoHD9XEInc0"
}
```
**Note:**
   this is an optional feature

---

## 🗄️ Caching Strategy

- **Search results** → Redis TTL = **1 hour**  
- **Movie details** → Redis TTL = **24 hours**  
- **Trailers** → Redis TTL = **24 hours**  

**Cache Keys:**  
- `search:{query}`  
- `details:{movie_id}`  
- `trailer:{movie_id}`  

---

## 🔒 Security

### 1️⃣ TMDb API Key

- Store only in **backend environment variables** (`.env`, secrets manager, or Docker secrets).  
- **Never expose** the key in frontend/mobile apps.  
- All external calls must go through the **proxy layer only**.

#### Example `.env`
```env
TMDB_API_KEY=your_real_key_here
TMDB_BASE_URL=https://api.themoviedb.org/3
CACHE_TTL=86400
```

#### Load in Backend (Python Example)
```python
import os

TMDB_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
CACHE_TTL = int(os.getenv("CACHE_TTL", 86400))
```

---

## ❌ Error Handling

All errors are normalized by the Cinemix API layer.  
Frontend never sees raw TMDb errors — only standardized JSON.

### Common Error Responses

1. **Invalid Request**
```json
{
  "error": "Invalid request",
  "message": "Query parameter 'query' is required."
}
```

2. **Not Found**
```json
{
  "error": "Not Found",
  "message": "Movie with ID 99999999 not found."
}
```

3. **TMDb Rate Limit Exceeded**
```json
{
  "error": "Rate Limit",
  "message": "Too many requests to TMDb. Please try again later."
}
```

4. **Internal Server Error**
```json
{
  "error": "Server Error",
  "message": "Unexpected error occurred. Please contact support."
}
```

**Design Decisions:**  
- Centralized exception handling in FastAPI middleware  
- TMDb raw errors never leak to client apps  
- Consistent error structure → always:  
```json
{ "error": string, "message": string }
```

---

## ⚖️ Rate Limiting Note

- TMDb Free Tier: **40 requests / 10 seconds / IP**  
- Cinemix includes an **internal sliding window rate limiter** (educational) to simulate production-ready handling.  
- Requests beyond limit return:  
```json
{
  "error": "Rate Limit",
  "message": "Too many requests to Cinemix API."
}
```

---

## 📊 Architecture Diagram

```
[Frontend App]  →  [Cinemix API Layer]  →  [Redis Cache] 
                                   ↓
                              [TMDb API]
```

---

## 📝 Important Notes

- Always **read this documentation first** before implementing or modifying API integration code.  
- Keep **DTOs and docs in sync** — if you change a field in code, update this file.  
- Never hardcode API keys or base URLs — always use environment variables. 

