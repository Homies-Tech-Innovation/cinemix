# 📚 Project Documentation

This folder contains **all technical and implementation documentation** for the project.  
It is organized so that each component has its own dedicated file to avoid clutter and merge conflicts.

---

## 📂 Folder Structure

```
docs/
    architecture/
        system_overview.md # High-level architecture explanation
        sequence_diagram.png # Flow diagram of request cycle
    implementation/
        api_integration.md # Internal & external API integration guidance
        caching.md # Redis caching setup and usage
        rate_limiting.md # Internal rate-limiting implementation
        implementation_guidance.md # Guidance on researching and implementing documentation
env_variables.md # Centralized list of environment variables
README.md # This file
```

---

## 🗂 What Goes Where

### **1. `architecture/`**

For **big-picture** system documentation.

- **`system_overview.md`** – Explain how major components interact, supported with diagrams.
- **`sequence_diagram.png`** – The main request flow (cache hit, cache miss, rate limit, API call).

### **2. `implementation/`**

For **component-level** implementation guidance.
Each file is a **guidance doc** for researching, deciding, and implementing a specific part of the system.

| File                         | Purpose                                                              |
| ---------------------------- | -------------------------------------------------------------------- |
| `api_integration.md`         | External API usage, request/response DTOs, rate limits, query types. |
| `caching.md`                 | Redis setup, TTL policies, data formats, function signatures.        |
| `rate_limiting.md`           | Algorithm choice, thresholds, middleware flow, function signatures.  |
| `implementation_guidance.md` | Guidance on what to research and how to implement documentation.     |

### **3. `env_variables.md`**

- The **only file** for documenting environment variables.
- Each time a new variable is added, update:
  - **Variable name**
  - **Purpose**
  - **Required/Optional**
  - **Example value (safe)**

---

## 🛠 How to Contribute to Documentation

1. **Pick the correct file** — Only edit the file related to your change.
2. **Be specific** — Keep updates scoped to your component.
3. **Avoid dumping unrelated changes** into a single commit.
4. **Use Markdown headings** — Keep structure clear for easy navigation.
5. **Commit messages** — Use clear commit messages for doc changes:

```
docs(caching): add TTL policy section
docs(api_integration): update rate limit details
```

---

## 📌 Tips for Keeping Docs Clean

- **Don’t mix components** — API guidance doesn’t go into caching.md.
- **Keep diagrams updated** when architecture changes.
- **Use examples** — Code snippets, request/response samples make docs more useful.
- **Keep it short** — Link to external sources for deep explanations.

---

✅ Following this structure will make sure docs stay clean, easy to navigate, and helpful for onboarding new developers.
