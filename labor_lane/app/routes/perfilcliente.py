from flask import Blueprint, render_template, session, redirect, url_for


perfilcliente_bp = Blueprint('perfilcliente', __name__)

@perfilcliente_bp.route('/perfilcliente', methods=['GET'])   
def perfilcliente():
    if 'usuario' in session:
        return render_template('perfilcliente.html', nombre=session['usuario'])
    return redirect(url_for('login'))


