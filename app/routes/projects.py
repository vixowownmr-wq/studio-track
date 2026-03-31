from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Project, ProjectParticipant, Phase, Version, User
import os
from werkzeug.utils import secure_filename
from app.models import Project, ProjectParticipant, Phase, Version, User, Comment
import cloudinary.uploader
from app.email import enviar_notificacion_version
from app.email import enviar_notificacion_version, enviar_notificacion_comentario

projects_bp = Blueprint('projects', __name__)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'aiff', 'flac', 'ogg', 'm4a'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Dashboard principal ---
@projects_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'producer':
            projects = Project.query.filter_by(producer_id=current_user.id).all()
        else:
            participaciones = ProjectParticipant.query.filter_by(user_id=current_user.id).all()
            projects = [p.project for p in participaciones]
        return render_template('projects/index.html', projects=projects)
    return render_template('landing.html')@projects_bp.route('/')



# --- Crear proyecto ---
@projects_bp.route('/proyecto/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_proyecto():
    if current_user.role != 'producer':
        flash('Solo los productores pueden crear proyectos.', 'danger')
        return redirect(url_for('projects.index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
            return render_template('projects/nuevo_proyecto.html')

        proyecto = Project(
            name=nombre,
            description=descripcion,
            producer_id=current_user.id
        )
        db.session.add(proyecto)
        db.session.commit()

        # Fases por defecto
        fases_default = ['Grabación', 'Maqueta', 'Mezcla', 'Master']
        for i, nombre_fase in enumerate(fases_default):
            fase = Phase(name=nombre_fase, order=i, project_id=proyecto.id)
            db.session.add(fase)
        db.session.commit()

        flash(f'Proyecto "{nombre}" creado con éxito.', 'success')
        return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))

    return render_template('projects/nuevo_proyecto.html')


# --- Ver proyecto ---
@projects_bp.route('/proyecto/<int:proyecto_id>')
@login_required
def ver_proyecto(proyecto_id):
    proyecto = Project.query.get_or_404(proyecto_id)

    # Verificar acceso
    es_productor = proyecto.producer_id == current_user.id
    es_participante = ProjectParticipant.query.filter_by(
        project_id=proyecto_id, user_id=current_user.id
    ).first()

    if not es_productor and not es_participante:
        flash('No tienes acceso a este proyecto.', 'danger')
        return redirect(url_for('projects.index'))

    return render_template('projects/ver_proyecto.html',
                           proyecto=proyecto,
                           es_productor=es_productor)


# --- Agregar artista al proyecto ---
@projects_bp.route('/proyecto/<int:proyecto_id>/agregar_artista', methods=['POST'])
@login_required
def agregar_artista(proyecto_id):
    proyecto = Project.query.get_or_404(proyecto_id)
    if proyecto.producer_id != current_user.id:
        flash('No tienes permiso para hacer eso.', 'danger')
        return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto_id))

    username = request.form.get('username')
    artista = User.query.filter_by(username=username).first()

    if not artista:
        flash(f'No existe un usuario con el nombre "{username}".', 'danger')
    elif artista.id == current_user.id:
        flash('No puedes agregarte a ti mismo.', 'danger')
    elif ProjectParticipant.query.filter_by(project_id=proyecto_id, user_id=artista.id).first():
        flash(f'{username} ya está en el proyecto.', 'danger')
    else:
        participante = ProjectParticipant(project_id=proyecto_id, user_id=artista.id)
        db.session.add(participante)
        db.session.commit()
        flash(f'{username} agregado al proyecto.', 'success')

    return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto_id))


# --- Agregar fase ---
@projects_bp.route('/proyecto/<int:proyecto_id>/nueva_fase', methods=['POST'])
@login_required
def nueva_fase(proyecto_id):
    proyecto = Project.query.get_or_404(proyecto_id)
    if proyecto.producer_id != current_user.id:
        flash('No tienes permiso.', 'danger')
        return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto_id))

    nombre = request.form.get('nombre_fase')
    if nombre:
        orden = len(proyecto.phases)
        fase = Phase(name=nombre, order=orden, project_id=proyecto_id)
        db.session.add(fase)
        db.session.commit()
        flash(f'Fase "{nombre}" agregada.', 'success')

    return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto_id))


# --- Subir versión ---
@projects_bp.route('/fase/<int:fase_id>/subir', methods=['POST'])
@login_required
def subir_version(fase_id):
    fase = Phase.query.get_or_404(fase_id)
    proyecto = fase.project

    es_productor = proyecto.producer_id == current_user.id
    es_participante = ProjectParticipant.query.filter_by(
        project_id=proyecto.id, user_id=current_user.id
    ).first()

    if not es_productor and not es_participante:
        flash('No tienes acceso.', 'danger')
        return redirect(url_for('projects.index'))

    archivo = request.files.get('archivo')
    notas = request.form.get('notas', '')

    if not archivo or archivo.filename == '':
        flash('Selecciona un archivo.', 'danger')
        return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))

    if not allowed_file(archivo.filename):
        flash('Formato no permitido. Usa mp3, wav, aiff, flac, ogg o m4a.', 'danger')
        return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))

    # Número de versión automático
    ultima = Version.query.filter_by(phase_id=fase_id).order_by(Version.number.desc()).first()
    numero = (ultima.number + 1) if ultima else 1

    # Subir a Cloudinary
    import cloudinary.uploader
    resultado = cloudinary.uploader.upload(
        archivo,
        resource_type='video',  # Cloudinary usa 'video' para audio también
        folder=f'studio_track/{proyecto.id}/{fase_id}',
        public_id=f'v{numero}_{secure_filename(archivo.filename)}'
    )

    version = Version(
        number=numero,
        filename=archivo.filename,
        file_path=resultado['secure_url'],
        notes=notas,
        phase_id=fase_id,
        uploaded_by=current_user.id
    )
    db.session.add(version)
    db.session.commit()

    flash(f'Versión {numero} subida con éxito.', 'success')
    # Notificar a los artistas
    # Notificar a los artistas
    # Notificar al productor
    try:
        enviar_notificacion_version(proyecto, fase, version, proyecto.participants, proyecto.producer.email)
    except Exception as e:
        print(f"ERROR EMAIL: {e}")
    flash(f'Versión {numero} subida con éxito.', 'success')
    return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))

# --- Agregar comentario ---
@projects_bp.route('/version/<int:version_id>/comentar', methods=['POST'])
@login_required
def comentar(version_id):
    version = Version.query.get_or_404(version_id)
    proyecto = version.phase.project

    es_productor = proyecto.producer_id == current_user.id
    es_participante = ProjectParticipant.query.filter_by(
        project_id=proyecto.id, user_id=current_user.id
    ).first()

    if not es_productor and not es_participante:
        return 'Sin acceso', 403

    contenido = request.form.get('contenido', '').strip()
    if not contenido:
        return 'Vacío', 400

    comentario = Comment(
        content=contenido,
        version_id=version_id,
        user_id=current_user.id
    )
    db.session.add(comentario)
    db.session.commit()

    # Notificar al productor si quien comenta es un artista
    if current_user.id != proyecto.producer_id:
        try:
            enviar_notificacion_comentario(proyecto, version.phase, version, comentario, proyecto.producer.email)
        except Exception as e:
            print(f"ERROR EMAIL COMENTARIO: {e}")

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return 'ok', 200

    flash('Comentario agregado.', 'success')
    return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))

@projects_bp.route('/version/<int:version_id>/eliminar', methods=['POST'])
@login_required
def eliminar_version(version_id):
    version = Version.query.get_or_404(version_id)
    proyecto = version.phase.project

    if proyecto.producer_id != current_user.id:
        flash('Solo el productor puede eliminar versiones.', 'danger')
        return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))

    # Eliminar de Cloudinary
    try:
        public_id = f'studio_track/{proyecto.id}/{version.phase_id}/v{version.number}_{secure_filename(version.filename)}'
        cloudinary.uploader.destroy(public_id, resource_type='video')
    except Exception:
        pass  # Si falla Cloudinary igual eliminamos de la base de datos

    db.session.delete(version)
    db.session.commit()

    flash('Versión eliminada.', 'success')
    return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))

@projects_bp.route('/fase/<int:fase_id>/aprobar', methods=['POST'])
@login_required
def aprobar_fase(fase_id):
    fase = Phase.query.get_or_404(fase_id)
    proyecto = fase.project

    if proyecto.producer_id != current_user.id:
        flash('Solo el productor puede aprobar fases.', 'danger')
        return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))

    fase.aprobada = not fase.aprobada  # Toggle: aprueba o desaprueba
    db.session.commit()

    estado = 'aprobada' if fase.aprobada else 'desaprobada'
    flash(f'Fase "{fase.name}" {estado}.', 'success')
    return redirect(url_for('projects.ver_proyecto', proyecto_id=proyecto.id))