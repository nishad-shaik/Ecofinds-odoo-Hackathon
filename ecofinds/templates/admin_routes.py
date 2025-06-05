from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import db, Complaint

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/complaints')
@login_required  # Add admin check later
def view_complaints():
    complaints = Complaint.query.all()
    return render_template('admin/complaints.html', complaints=complaints)

@admin_bp.route('/complaint/resolve/<int:complaint_id>')
@login_required
def resolve_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = 'Resolved'
    db.session.commit()
    flash('Complaint resolved.')
    return redirect(url_for('admin_bp.view_complaints'))
