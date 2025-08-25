## External API Integration – Cinemix

This document explains how Cinemix integrates with the **OMDb API** to provide movie data and search functionality.
It covers endpoints, rate limiting, error handling, and the integration flow within our backend.

---

### Purpose

Cinemix does not expose OMDb directly to the frontend.
Instead, the backend acts as a **proxy layer** with caching, error handling, and rate limiting strategies.
This ensures:

- A stable user experience regardless of OMDb downtime
- Reduced API quota usage (via Redis caching)
- Consistent response formats for the frontend (using DTOs)

---

### Key Points

- **Unified Interface** → Cinemix applications only call `/api/search` and `/api/details`
- **Caching Layer** → Redis reduces OMDb requests and improves response times
- **Error Handling** → Centralized error messages and rate-limit handling
- **DTO Models** → All responses are validated and structured with Pydantic models

---

### OMDb API Endpoints

The API handles all requests at the same endpoint:
`GET /api/`

#### 1. Movie Search

- **Parameters**

  - `s` — query

- **Request Example**

  ```
  GET /api/?s=<query>&apikey=<api_key>
  ```

- **Response Example**

  ```json
  {
  	"Search": [
  		{
  			"Title": "string",
  			"Year": "string",
  			"imdbID": "string",
  			"Type": "string",
  			"Poster": "string"
  		}
  	],
  	"totalResults": "string",
  	"Response": "string"
  }
  ```

#### 2. Movie Details

- **Parameters**

  - `i` — IMDb ID

- **Request Example**

  ```
  GET /api/?i=<query>&apikey=<api_key>
  ```

- **Response Example**

  ```json
  {
  	"Title": "string",
  	"Year": "string",
  	"Rated": "string",
  	"Released": "string",
  	"Runtime": "string",
  	"Genre": "string",
  	"Director": "string",
  	"Writer": "string",
  	"Actors": "string",
  	"Plot": "string",
  	"Language": "string",
  	"Country": "string",
  	"Awards": "string",
  	"Poster": "string",
  	"Ratings": [
  		{
  			"Source": "string",
  			"Value": "string"
  		}
  	],
  	"Metascore": "string",
  	"imdbRating": "string",
  	"imdbVotes": "string",
  	"imdbID": "string",
  	"Type": "string",
  	"totalSeasons": "string",
  	"Response": "string"
  }
  ```

---

### Environment Variables

```env
OMDb_API_KEY=your_real_key_here
OMDb_BASE_URL=http://www.omdbapi.com/
```

---

### Error Handling

All errors are standardized by the Cinemix API layer.
The frontend never receives raw OMDb errors — only normalized JSON responses.

#### Common OMDb Error Responses

1. **Invalid Request**

   ```json
   {
   	"Response": "False",
   	"Error": "..."
   }
   ```

   - **Status Code**: `200`

2. **Not Found**

   ```json
   {
   	"Response": "False",
   	"Error": "Movie not found!"
   }
   ```

   - **Status Code**: `200`

3. **Rate Limit Exceeded**

   ```json
   {
   	"Response": "False",
   	"Error": "..."
   }
   ```

   - **Status Code**: `429`

4. **Invalid or Missing API Key**

   ```json
   {
   	"Response": "False",
   	"Error": "No API key provided."
   }
   ```

   - **Status Code**: `401`

---

### Rate Limiting

- OMDb Free Tier: **1,000 requests per day**

---

### Architecture Overview

```
[Frontend App]  →  [Cinemix API Layer]  →  [Redis Cache]
                                   ↓
                              [OMDb API]
```

---

### Important Notes

- Always review this documentation before implementing or modifying API integration code.
- Keep **DTOs and documentation synchronized** — if you change a field in code, update this file.
- Never hardcode API keys or base URLs — always use environment variables.
