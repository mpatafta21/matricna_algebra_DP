from flask import Flask, request, jsonify, render_template
import subprocess
import re

app = Flask(__name__)

# Funkcija za izvršavanje Prolog upita
def execute_prolog_query(query):
    process = subprocess.Popen(
        ["/home/maxfakta/software/Flora-2/XSB/bin/xsb", "--noprompt"],  # Zamijeni "/path/to/xsb" stvarnom putanjom do XSB
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Učitaj logika.P i izvrši upit
    prolog_command = f"[logika].\n{query}.\nhalt.\n"
    stdout, stderr = process.communicate(prolog_command)
    
    if stderr.strip():
        print(f"XSB Error: {stderr.strip()}")  
    
    # Obradi rezultat kako bi se izbjegle sistemske poruke iz XSB-a
    result_lines = stdout.strip().split("\n")

    print("STDOUT LINES:", result_lines)  
    print("Prolog upit:", query)  

 # Provjeri rezultat koristeći regex
    result_match = re.search(r"Rezultat\s*=\s*(\[.*\]|\-?\d+(\.\d+)?)(?=no|$)", "\n".join(result_lines))
    if result_match:
        try:
            result = result_match.group(1)
            if result.startswith("["):  
                final_result = eval(result)  
            else:  
                final_result = float(result) if "." in result else int(result)
        except Exception as e:
            final_result = f"Error parsing result: {e}"
    else:
        final_result = "Nema rezultata."

    if isinstance(final_result, (int, float)):
        return {"result": f"{final_result}"}
    
    return {"result": final_result}


@app.route('/')
def index():
    return render_template('index.html')

# Ruta za determinantu
@app.route('/determinant', methods=['POST'])
def determinant():
    data = request.json
    matrix = data.get('matrix')
    print("Received matrix:", matrix)  
    if not matrix:
        return jsonify({"error": "Matrica nije poslana."}), 400
    
    # Kreiraj Prolog upit
    query = f"determinanta({matrix}, Rezultat)"
    response = execute_prolog_query(query)
    return jsonify(response)

# Ruta za transponiranje matrice
@app.route('/transpose', methods=['POST'])
def transpose():
    data = request.json
    print("Primljeni podaci za transponiranje:", data)  
    matrix = data.get('matrix')
    if not matrix:
        return jsonify({"error": "Matrica nije poslana."}), 400
    
    query = f"transponiraj({matrix}, Rezultat)"
    response = execute_prolog_query(query)

    if isinstance(response['result'], list):
        return jsonify({"result": response['result']})
    else:
        return jsonify({"error": "Neuspješno transponiranje matrice."}), 500


# Ruta za množenje matrica
@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.json
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')

    print("Received Matrix 1:", matrix1)
    print("Received Matrix 2:", matrix2)

    if not matrix1 or not matrix2:
        return jsonify({"error": "Matrice nisu poslane."}), 400
    
    query = f"pomnozi_matrice({matrix1}, {matrix2}, Rezultat)"
    response = execute_prolog_query(query)
    return jsonify(response)


# Ruta za zbrajanje matrica
@app.route('/add_matrices', methods=['POST'])
def add_matrices():
    data = request.json
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')

    print("Received Matrix 1:", matrix1)
    print("Received Matrix 2:", matrix2)

    if not matrix1 or not matrix2:
        return jsonify({"error": "Matrice nisu poslane."}), 400
    
    query = f"zbroji_matrice({matrix1}, {matrix2}, Rezultat)"
    response = execute_prolog_query(query)
    return jsonify(response)


# Ruta za oduzimanje matrica
@app.route('/subtract_matrices', methods=['POST'])
def subtract_matrices():
    data = request.json
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')

    if not matrix1 or not matrix2:
        return jsonify({"error": "Matrice nisu poslane."}), 400

    query = f"oduzmi_matrice({matrix1}, {matrix2}, Rezultat)"
    response = execute_prolog_query(query)
    
    return jsonify(response)


# Ruta za skalar matrice
@app.route('/scale', methods=['POST'])
def scale():
    data = request.json
    matrix = data.get('matrix')
    scalar = data.get('scalar')
    if not matrix or scalar is None:
        return jsonify({"error": "Matrica ili skalar nisu poslani."}), 400
    
    query = f"skaliraj_matricu({matrix}, {scalar}, Rezultat)"
    response = execute_prolog_query(query)
    return jsonify(response)



# Ruta za zbrajanje redaka matrice
@app.route('/add_rows', methods=['POST'])
def add_rows():
    data = request.json
    row1 = data.get('row1')
    row2 = data.get('row2')
    if not row1 or not row2:
        return jsonify({"error": "Redovi nisu poslani."}), 400
    
    query = f"zbroji_retke({row1}, {row2}, Rezultat)"
    response = execute_prolog_query(query)
    return jsonify(response)

# Ruta za skalarni produkt
@app.route('/dot_product', methods=['POST'])
def dot_product():
    data = request.json
    vector1 = data.get('vector1')
    vector2 = data.get('vector2')
    if not vector1 or not vector2:
        return jsonify({"error": "Vektori nisu poslani."}), 400
    
    query = f"skalarni_produkt({vector1}, {vector2}, Rezultat)"
    response = execute_prolog_query(query)
    return jsonify(response)

# Ruta za dobivanje stupca matrice
@app.route('/column', methods=['POST'])
def column():
    data = request.json
    matrix = data.get('matrix')
    index = data.get('index')
    if not matrix or index is None:
        return jsonify({"error": "Matrica ili indeks nisu poslani."}), 400
    
    query = f"stupac({matrix}, {index}, Rezultat)"
    response = execute_prolog_query(query)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
