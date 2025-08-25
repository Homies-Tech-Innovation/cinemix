# Documentation Implementation Guidance

This document outlines the research and documentation required for each component/section of the app.

---

## Backend API (Internal)

### To be worked on:

- **Request and Response DTOs**
  - Define data shape and naming conventions following REST API best practices.
  - Provide example payloads.
- **Endpoint Design**
  - URL patterns (`/api/version/..`).
  - Endpoint names.
  - HTTP method used for each.
- **Error Handling**
  - Whether FastAPI provides built-in error handling or not.
  - How to handle client and server-side errors (could be a bad request, External API failure, etc.).
- **Coding Standards**
  - Folder structure to follow.
  - FastAPI best practices for conventions and organization.
  - Conventions preference as per the team.
  - **Pick and decide on final conventions to be used during development.**

---

## External API Integration

### To be worked on:

- **Request and Response DTOs**
  - Provider's query parameters needed.
  - Response format for success and error cases.
  - Provide example payloads.
- **Rate Limits**
  - Provider's rate limit thresholds.
- **API Behavior**

  > [!IMPORTANT]
  > This aspect could significantly impact the app's design.

  - How the API handles movie/show searches and whether it affects our application architecture (e.g., if the API returns "best matches," we may need a separate search results endpoint before showing details)
  - What types of queries does the provider accept
  - What response format to expect for different query types, and how results are structured
  - Any other details like Auth methods, or any special requirements.

---

## Redis Caching

> Dependent on previous documentation to be completed first.

### To be worked on:

- **Setup Decision**
  - Local host vs managed cloud deployment options
- **TTL Policy**
  - Time limits for cache expiration.
- **Data Stucture**
  - Which data type to use.
  - The shape of data to be stored.
- **Function Signatures**
  - Core high-level functions for operations (`match_query`, `store_cache`, etc.).

---

## Rate Limiting

### To be worked on:

- **FastAPI**
  - Whether FastAPI provides built-in rate limits.
  - If so, how customizable are they, and how can they be customized.
- **Thresholds**
  - Rate limit decisions per user/IP/endpoint based on expected usage.
- **Algorithm Choice**
  - Which algorithm to use (token bucket, sliding window, etc.).
- **Description**
  - How will the rate-limiting flow operate and integrate with the app.
- **Function Signatures**
  - High-level function signatures.
