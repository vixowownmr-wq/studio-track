from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import RegistroForm, LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('projects.index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Procesar invitación pendiente
        from flask import session
        from app.models import Invitation
        token = session.pop('invitation_token', None)
        if token:
            invitacion = Invitation.query.filter_by(token=token, accepted=False).first()
            if invitacion:
                participante = ProjectParticipant(project_id=invitacion.project_id, user_id=user.id)
                db.session.add(participante)
                invitacion.accepted = True
                db.session.commit()
                flash('Cuenta creada. Ya estás en el proyecto.', 'success')
                login_user(user)
                return redirect(url_for('projects.ver_proyecto', proyecto_id=invitacion.project_id))

        flash('Cuenta creada. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('projects.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email o contraseña incorrectos.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Procesar invitación pendiente
        from flask import session
        from app.models import Invitation
        token = session.pop('invitation_token', None)
        if token:
            invitacion = Invitation.query.filter_by(token=token, accepted=False).first()
            if invitacion:
                ya_participa = ProjectParticipant.query.filter_by(
                    project_id=invitacion.project_id, user_id=user.id
                ).first()
                if not ya_participa:
                    participante = ProjectParticipant(project_id=invitacion.project_id, user_id=user.id)
                    db.session.add(participante)
                    invitacion.accepted = True
                    db.session.commit()
                    flash(f'Te uniste al proyecto "{invitacion.project.name}".', 'success')
                login_user(user)
                return redirect(url_for('projects.ver_proyecto', proyecto_id=invitacion.project_id))

        login_user(user)
        return redirect(url_for('projects.index'))
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
