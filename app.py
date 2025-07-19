"""Flask calculator application main module.

This module provides a simple web calculator with basic arithmetic operations.
"""

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'calculator_secret_key_2025'


@app.route('/')
def index():
    """Render the main calculator page."""
    display = session.get('display', '')
    error = session.get('error', '')
    
    # Clear error after displaying it once
    if 'error' in session:
        session.pop('error')
    
    return render_template('calculator.html', display=display, error=error)


@app.route('/input')
def input_value():
    """Handle number and operator input via query parameter."""
    value = request.args.get('value', '')
    
    current_display = session.get('display', '')
    
    # If display is empty or shows '0', replace with new value
    if current_display == '' or current_display == '0':
        session['display'] = value
    else:
        session['display'] = current_display + value
    
    return redirect(url_for('index'))


@app.route('/clear')
def clear():
    """Clear the entire display."""
    session['display'] = ''
    if 'error' in session:
        session.pop('error')
    return redirect(url_for('index'))


@app.route('/clear_entry')
def clear_entry():
    """Clear the current entry."""
    session['display'] = ''
    if 'error' in session:
        session.pop('error')
    return redirect(url_for('index'))


@app.route('/backspace')
def backspace():
    """Delete the last character."""
    current_display = session.get('display', '')
    
    if len(current_display) > 1:
        session['display'] = current_display[:-1]
    else:
        session['display'] = ''
    
    if 'error' in session:
        session.pop('error')
    
    return redirect(url_for('index'))


@app.route('/calculate')
def calculate():
    """Process calculation and return result."""
    expression = session.get('display', '')
    
    if not expression:
        session['error'] = 'No expression provided'
        return redirect(url_for('index'))
    
    try:
        # Basic validation - only allow numbers and basic operators
        allowed_chars = set('0123456789+-*/.()')
        if not all(char in allowed_chars for char in expression):
            session['error'] = 'Invalid characters in expression'
            return redirect(url_for('index'))
        
        # Additional validation for common invalid patterns
        if (expression.endswith(('+', '-', '*', '/')) or 
            expression.startswith(('*', '/')) or
            '++' in expression or '--' in expression or 
            '**' in expression or '//' in expression or
            expression.count('(') != expression.count(')')):
            session['error'] = 'Invalid expression'
            return redirect(url_for('index'))
        
        # Evaluate the expression safely
        result = eval(expression)
        session['display'] = str(result)
        
        # Clear any previous errors
        if 'error' in session:
            session.pop('error')
            
    except ZeroDivisionError:
        session['error'] = 'Division by zero'
    except Exception as e:
        session['error'] = 'Invalid expression'
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
