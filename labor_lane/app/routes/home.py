from flask import Blueprint, render_template, session

home_bp = Blueprint('home', __name__)

@home_bp.route('/') 
def home(): 
    if 'usuario' in session:
        return render_template('home.html', nombre=session['usuario'])
    return render_template('home.html') 

