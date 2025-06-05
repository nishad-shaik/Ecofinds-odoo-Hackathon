from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from models import Complaint

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin/complaints')
@login_required  # Add admin check if needed
def view_complaints():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('admin/complaints.html', complaints=complaints)

@admin_bp.route('/admin/complaint/resolve/<int:complaint_id>')
@login_required
def resolve_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = 'Resolved'
    db.session.commit()
    flash('Complaint marked as resolved.')
    return redirect(url_for('admin_bp.view_complaints'))
