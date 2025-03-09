from flask import Flask, request, jsonify
from flask_cors import CORS  
import numpy as np

app = Flask(__name__)
CORS(app)  

# Define signal functions
def rect(t):
    return np.where(np.abs(t) <= 0.5, 1, 0)

def tri(t):
    return np.where(np.abs(t) <= 1, 1 - np.abs(t), 0)

def sinc(t):
    return np.sinc(t / np.pi)

def u(t):
    return np.where(t >= 0, 1, 0)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    formula = data.get('formula', '').strip()
    
    if not formula:
        return jsonify({"error": "No formula provided"}), 400

    t = np.linspace(-2, 2, 1000)  

    try:
        # Safe execution environment
        local_dict = {
            "t": t,
            "pi": np.pi,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": lambda x: np.log(np.abs(x) + 1e-9),
            "sqrt": lambda x: np.sqrt(np.abs(x)),
            "rect": rect,
            "tri": tri,
            "sinc": sinc,
            "u": u
        }

        y = eval(formula, {"__builtins__": {}}, local_dict)

        return jsonify({"t": t.tolist(), "y": y.tolist()})

    except Exception as e:
        return jsonify({"error": f"Error evaluating formula: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
