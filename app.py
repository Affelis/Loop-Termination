from flask import Flask, render_template, request
from programs.witness import find_witnesses

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/witness', methods=['GET', 'POST'])
def run_witness():
    results = None
    error = None
    
    #default_A = "1, 0, 0, 0\n0, 1, 0, 0\n-2, -1, 1, 0\n2, 1, -1, 0\n0, -1, 0, 1\n0, 1, 0, -1"
    #default_b = "0, 0, 0, 0, 1, -1"

    #point_A = "1, 0, 0, 0\n0, 1, 0, 0\n0, 0, 1, 0\n0, 0, 0, 1"
    #point_b = "0, 0, 0, 0"

    #ray_A = "1, 0, 0, 0\n0, 1, 0, 0\n0, -1, 0, 1\n0, 1, 0, -1"
    #ray_b = "0, 0, 1, -1"

    #line_A = ""
    #line_b = ""

    #half_plane_A = ""
    #half_plane_b = ""

    default_A = "2, 2, -1, 2\n1, 1, -2, 1\n1, 1, 1, 0\n1, 1, 0, -2"
    default_b = "-1, 0, 0, 2"

    if request.method == 'POST':
        raw_A = request.form.get('matrix_A', '')
        raw_b = request.form.get('vector_b', '')
        
        default_A = raw_A
        default_b = raw_b

        try:
            # Parse Matrix A
            parsed_A = []
            for line in raw_A.strip().splitlines():
                if not line.strip():
                    continue
                row = [float(x) for x in line.replace(',', ' ').split()]
                if len(row) != 4:
                    raise ValueError(f"Each row of Matrix A must have 4 numbers. Row '{line}' has {len(row)}.")
                parsed_A.append(row)

            # Parse Vector b
            parsed_b = [float(x) for x in raw_b.replace(',', ' ').replace('\n', ' ').split()]

            if len(parsed_A) != len(parsed_b):
                raise ValueError(f"Matrix A has {len(parsed_A)} rows, but Vector b has {len(parsed_b)} values. They must match.")

            # Run imported program
            results = find_witnesses(parsed_A, parsed_b)

        except Exception as e:
            error = str(e)

    return render_template('witness.html', results=results, error=error, default_A=default_A, default_b=default_b)

if __name__ == '__main__':
    app.run(debug=True)