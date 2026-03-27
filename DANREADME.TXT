# Admin Reference (DAN)

## Credentials
- **Expert Password**: `password123` (Configurable via `EXPERT_PASSWORD`)
- **Admin Password**: `admin456` (Configurable via `ADMIN_PASSWORD`)

## Storage Files
- **Diagnostics Data**: `diagnostics_data.json` (Configurable via `DIAGNOSTICS_DATA_FILE`)
- **Users Data**: `users_data.json` (Configurable via `DIAGNOSTICS_USERS_FILE`)
- **Tutorials Data**: `tutorials_data.json` (Configurable via `DIAGNOSTICS_TUTORIALS_FILE`)
- **Uploads Directory**: `uploads/`

## Testing Notes
- The app uses `pytest` for testing.
- Unit tests for storage mock the data files using `tmp_path` and `monkeypatch`.
- To run tests: `PYTHONPATH=. pytest`
