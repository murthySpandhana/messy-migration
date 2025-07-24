## Overview
This document outlines major issues identified, changes made, assumptions, and future work during the refactoring of the Flask-based User Management API.

## Issues Identified

1.Passwords stored and compared in plain text

2.SQL injection vulnerabilities due to unsafe query construction

3.All logic in app.py, no modular separation

4.Lacked reusable functions and clear layering (routes/services/db)

5.No proper input validation on user data.

6.Error responses and HTTP status codes were inconsistent or missing.

7.API responses returned raw tuples or stringified data instead of structured JSON with meaningful keys.

8.Sensitive data such as password hashes were sometimes exposed in responses.

9.A single cursor was shared globally, potentially causing concurrency and thread safety issues.

10.No tests to validate core flows or endpoints

## Changes Made
1. **Refactored Project Structure**

   * Split code into multiple modules:

     * `app.py` for app initialization
     * `routes/user_routes.py` for route definitions
     * `services/user_service.py` for business logic and DB operations
     * `db.py` for database connection management
     * `utils/validators.py` for input validation
   * This separation improves maintainability, readability, and testability.

2. **Security Improvements**

   * Implemented password hashing (generate_password_hash) and secure verification (check_password_hash).
   * Converted all SQL queries to parameterized statements to prevent SQL injection.

3. **Input Validation**

   * Added regex-based email and password validation with clear error responses (HTTP 400).

4. **Error Handling and Status Codes**

   * Wrapped all database operations in try/except blocks with JSON error responses.
   * Used appropriate HTTP status codes (e.g., 200, 201, 400, 401, 404, 500).

5. **API Response Format**

   * Transformed database tuples into JSON objects with clear keys, excluding sensitive data.
   * Consistent JSON responses across all endpoints.

6. **Database Connection Management**

   * Created DB connections and cursors within service functions to improve concurrency safety.

7. **Testing**

   * Added Pytest tests covering key flows: user creation, login, retrieval, validation, and error cases.

   
## Assumptions or Trade-offs

* Kept SQLite as the database and continued using a global file-based DB for simplicity per original scope.
* Did not implement full authentication or session management (e.g., JWT tokens) as it was outside the scope.
* Password validation rules are basic; stricter policies can be added later.
* The project remains synchronous without async or multi-threaded DB handling given the challenge constraints.
* Test coverage is focused on critical paths, not exhaustive edge cases, to fit time constraints.


## What I Would Do With More Time

* Introduce a proper configuration system for environment variables, secrets, and DB connection strings.
* Switch from SQLite to a more scalable database like PostgreSQL or MySQL for better concurrency and larger data handling.
* Implement full user authentication and authorization (e.g., JWT or OAuth2).
* Add logging instead of print statements for better observability.
* Improve concurrency safety possibly by switching to a connection pool or more robust DB backend.
* Expand test coverage for edge cases and error scenarios.

