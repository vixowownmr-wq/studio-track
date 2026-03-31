from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    db.create_all()
    # Agregar columna aprobada si no existe
    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE phase ADD COLUMN aprobada BOOLEAN DEFAULT FALSE'))
            conn.commit()
    except Exception:
        pass  # La columna ya existe

if __name__ == '__main__':
    app.run(debug=True)