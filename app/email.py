import resend
from flask import current_app

def enviar_notificacion_version(proyecto, fase, version, artistas, productor_email):
    resend.api_key = current_app.config['RESEND_API_KEY']

    resend.Emails.send({
        "from": "Studio Track <onboarding@resend.dev>",
        "to": productor_email,
        "subject": f"Nueva versión subida en {proyecto.name}",
        "html": f"""
        <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 32px;">
            <div style="margin-bottom: 24px;">
                <span style="font-size: 16px; font-weight: 600;">● Studio Track</span>
            </div>

            <h2 style="font-size: 20px; font-weight: 600; margin-bottom: 8px;">
                Nueva versión subida
            </h2>

            <p style="font-size: 14px; color: #555; margin-bottom: 24px;">
                Se subió una nueva versión en el proyecto <strong>{proyecto.name}</strong>.
            </p>

            <div style="background: #f9f9f9; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                <p style="font-size: 13px; color: #888; margin-bottom: 4px;">Proyecto</p>
                <p style="font-size: 14px; font-weight: 600; margin-bottom: 12px;">{proyecto.name}</p>

                <p style="font-size: 13px; color: #888; margin-bottom: 4px;">Fase</p>
                <p style="font-size: 14px; font-weight: 600; margin-bottom: 12px;">{fase.name}</p>

                <p style="font-size: 13px; color: #888; margin-bottom: 4px;">Versión</p>
                <p style="font-size: 14px; font-weight: 600;">v{version.number} — {version.filename}</p>

                {f'<p style="font-size: 13px; color: #888; margin-top: 12px;">{version.notes}</p>' if version.notes else ''}
            </div>

            <a href="https://studio-track.up.railway.app"
               style="display: inline-block; background: #5a52d5; color: white;
                      text-decoration: none; padding: 10px 20px; border-radius: 7px;
                      font-size: 14px; font-weight: 500;">
                Ver proyecto
            </a>

            <p style="font-size: 12px; color: #bbb; margin-top: 32px;">
                Studio Track · Gestión de proyectos musicales
            </p>
        </div>
        """
    })

def enviar_notificacion_comentario(proyecto, fase, version, comentario, productor_email):
    resend.api_key = current_app.config['RESEND_API_KEY']

    resend.Emails.send({
        "from": "Studio Track <onboarding@resend.dev>",
        "to": productor_email,
        "subject": f"Nuevo comentario en {proyecto.name}",
        "html": f"""
        <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 32px;">
            <div style="margin-bottom: 24px;">
                <span style="font-size: 16px; font-weight: 600;">● Studio Track</span>
            </div>

            <h2 style="font-size: 20px; font-weight: 600; margin-bottom: 8px;">
                Nuevo comentario
            </h2>

            <p style="font-size: 14px; color: #555; margin-bottom: 24px;">
                <strong>{comentario.user.username}</strong> comentó en <strong>{proyecto.name}</strong>.
            </p>

            <div style="background: #f9f9f9; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                <p style="font-size: 13px; color: #888; margin-bottom: 4px;">Proyecto</p>
                <p style="font-size: 14px; font-weight: 600; margin-bottom: 12px;">{proyecto.name}</p>

                <p style="font-size: 13px; color: #888; margin-bottom: 4px;">Fase</p>
                <p style="font-size: 14px; font-weight: 600; margin-bottom: 12px;">{fase.name}</p>

                <p style="font-size: 13px; color: #888; margin-bottom: 4px;">Versión</p>
                <p style="font-size: 14px; font-weight: 600; margin-bottom: 12px;">v{version.number} — {version.filename}</p>

                <p style="font-size: 13px; color: #888; margin-bottom: 4px;">Comentario</p>
                <p style="font-size: 14px; color: #333; font-style: italic;">"{comentario.content}"</p>
            </div>

            <a href="https://studio-track.up.railway.app"
               style="display: inline-block; background: #5a52d5; color: white;
                      text-decoration: none; padding: 10px 20px; border-radius: 7px;
                      font-size: 14px; font-weight: 500;">
                Ver proyecto
            </a>

            <p style="font-size: 12px; color: #bbb; margin-top: 32px;">
                Studio Track · Gestión de proyectos musicales
            </p>
        </div>
        """
    })

def enviar_invitacion(proyecto, email, token):
    resend.api_key = current_app.config['RESEND_API_KEY']
    link = f"https://studio-track.up.railway.app/invitacion/{token}"

    resend.Emails.send({
        "from": "Studio Track <onboarding@resend.dev>",
        "to": email,
        "subject": f"Te invitaron a un proyecto en Studio Track",
        "html": f"""
        <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 32px;">
            <div style="margin-bottom: 24px;">
                <span style="font-size: 16px; font-weight: 600;">● Studio Track</span>
            </div>

            <h2 style="font-size: 20px; font-weight: 600; margin-bottom: 8px;">
                Te invitaron a un proyecto
            </h2>

            <p style="font-size: 14px; color: #555; margin-bottom: 24px;">
                Fuiste invitado a colaborar en <strong>{proyecto.name}</strong>.
            </p>

            <div style="background: #f9f9f9; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                <p style="font-size: 13px; color: #888; margin-bottom: 4px;">Proyecto</p>
                <p style="font-size: 14px; font-weight: 600;">{proyecto.name}</p>
            </div>

            <a href="{link}"
               style="display: inline-block; background: #5a52d5; color: white;
                      text-decoration: none; padding: 10px 20px; border-radius: 7px;
                      font-size: 14px; font-weight: 500;">
                Aceptar invitación
            </a>

            <p style="font-size: 12px; color: #bbb; margin-top: 32px;">
                Si no esperabas esta invitación puedes ignorar este email.
            </p>
        </div>
        """
    })