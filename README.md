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

<!-- Add 2-3 screenshots here — hace una diferencia enorme -->
