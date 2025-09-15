from flask import Flask, render_template, request, jsonify
import re
import math

app = Flask(__name__)

@app.route('/')
def calculator():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        
        # Remove any spaces
        expression = expression.replace(' ', '')
        
        # Security: Only allow specific characters
        allowed_chars = '0123456789+-*/().√^'
        if not all(c in allowed_chars for c in expression):
            return jsonify({'error': 'Invalid characters in expression'})
        
        # Replace special operators
        expression = expression.replace('√', 'sqrt(')
        expression = expression.replace('^', '**')
        
        # Count parentheses for sqrt
        sqrt_count = expression.count('sqrt(')
        open_parens = expression.count('(')
        close_parens = expression.count(')')
        
        # Add missing closing parentheses for sqrt
        if sqrt_count > (close_parens - open_parens + sqrt_count):
            expression += ')' * (sqrt_count - (close_parens - open_parens + sqrt_count))
        
        # Replace sqrt with math.sqrt
        expression = expression.replace('sqrt', 'math.sqrt')
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}, "math": math})
        
        # Format result
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
        
        return jsonify({'result': str(result)})
    
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'})
    except ValueError as e:
        return jsonify({'error': 'Math error'})
    except Exception as e:
        return jsonify({'error': 'Invalid expression'})

if __name__ == '__main__':
    app.run(debug=True)