# ADMIN DANREADME

This file contains basic instructions and testing information for the Admin.

## Admin Access
- **Admin Password:** admin456 (or custom set via ADMIN_PASSWORD environment variable)
- **Expert Password:** password123 (or custom set via EXPERT_PASSWORD environment variable)

## Testing Details
- The app uses local JSON files to store its state (`diagnostics_data.json`, `users_data.json`, `tutorials_data.json`).
- Uploaded files are stored in the `uploads/` directory, mapped by their unique Request ID.
- Admin panel can be accessed using the 🔐 ADMIN button in the bottom right corner of the app.
- You can create a test user directly through the UI or test login using predefined users.
- The Admin Panel provides a comprehensive overview of user activity, system metrics, and member management.
