# NewSIP - MicroSIP Clone with API

A lightweight Windows VoIP softphone with a built-in REST API for integration with web apps.

## Features
- Full SIP support (via PJSIP)
- Local REST API for call control
- System tray integration
- Automated Windows builds via GitHub Actions

## API Endpoints
The app runs a local API server on `http://127.0.0.1:8000`.

- **POST `/api/register`**: Register a SIP account.
  ```json
  {"server": "sip.provider.com", "username": "100", "password": "abc"}
  ```
- **POST `/api/call`**: Make an outgoing call.
  ```json
  {"destination": "sip:200@sip.provider.com"}
  ```
- **POST `/api/hangup`**: Hang up the current call.
- **GET `/api/status`**: Get registration and call status.

## How to get the Windows App
1. Go to the **Actions** tab in this GitHub repository.
2. Select the latest "Build Windows App" run.
3. Download the **NewSIP-Windows** artifact.
4. Run `NewSIP.exe`.

## Version
1.0.1 (Triggered Build)
- Required: Python 3.10+
- Install dependencies: `pip install -r requirements.txt`
- Run: `python main.py`

