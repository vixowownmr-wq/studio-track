# 🎵 Studio Track

Collaborative project management web app for music producers and artists.  
Built as a full-stack personal project — live in production.

🔗 **Live demo:** [studio-track.up.railway.app](https://studio-track.up.railway.app)

## Features

- Role-based authentication (Producer / Artist)
- Audio file versioning with inline player
- AJAX comments per track version
- Phase approval workflow
- Invitation system via email (Resend)
- Cloudinary integration for audio storage

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python · Flask · SQLAlchemy |
| Database | PostgreSQL (Railway) |
| Frontend | HTML · CSS · JavaScript (Jinja2) |
| Storage | Cloudinary |
| Email | Resend API |
| Deploy | Railway |

## Run locally
```bash
git clone https://github.com/vixowownmr-wq/studio-track
cd studio-track
pip install -r requirements.txt
cp .env.example .env  # Add your keys
flask run
```

## Screenshots

<img width="1920" height="1080" alt="Captura de pantalla 2026-04-08 011326" src="https://github.com/user-attachments/assets/00c05548-934e-4279-82af-ce4bbb90a8de" />
<img width="1920" height="1080" alt="Captura de pantalla 2026-04-08 005737" src="https://github.com/user-attachments/assets/f2055292-7e91-4e29-8a08-f485357cdaea" />
<img width="1920" height="1080" alt="Captura de pantalla 2026-04-08 010759" src="https://github.com/user-attachments/assets/617996b3-55ff-423e-8ae6-4b64e942e724" />
<img width="1920" height="1080" alt="Captura de pantalla 2026-04-08 010946" src="https://github.com/user-attachments/assets/e88408a0-bdf1-4b32-98df-ff93a533d348" />

<!-- Add 2-3 screenshots here — hace una diferencia enorme -->

