# Admin Basic Instructions
## Authentication
To access the standard Member Area, a pre-setup account is available:
* **Username (Email)**: DSSDiag
* **Password**: Danthrax123

To access the Expert Dashboard or the Admin Area, you **must** set the following environment variables. The application no longer uses default hardcoded passwords for security reasons. If these are not set, access is disabled.

* `EXPERT_PASSWORD`: Set this environment variable to your desired expert login password.
* `ADMIN_PASSWORD`: Set this environment variable to your desired admin login password.

Example usage to run the app locally:
```bash
EXPERT_PASSWORD="my_expert_password" ADMIN_PASSWORD="my_admin_password" streamlit run app.py
```

## Pre-Setup Member Account
A default member account is pre-configured for immediate use after deployment:

* **Username (Email):** DSSDiag
* **Password:** Danthrax123

> ⚠️ It is strongly recommended to change this password after first login or remove this account if it is not needed.

## Testing Aspects
* **Local JSON Storage**: This application currently uses local JSON files to store data (`diagnostics_data.json`, `users_data.json`, and `tutorials_data.json`).
* **Uploads**: Binary files are stored in a local `uploads/` directory.

These files are ignored in `.gitignore` to prevent committing generated or real user data to the repository.

