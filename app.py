from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!<br><a href='/dashboard'>Go to Dashboard</a>"

@app.route('/student')
def get_student():
    return jsonify({
        "name": "Your Name",
        "grade": 10,
        "section": "Zechariah"
    })

@app.route('/dashboard')
def dashboard():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #f8f9fa;
                margin-top: 60px;
                font-family: Arial, sans-serif;
            }
            .card {
                max-width: 400px;
                margin: auto;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h1 class="mb-4">🎓 Student Dashboard</h1>
            <div class="card p-4">
                <h4 id="name">Name: Loading...</h4>
                <h5 id="grade">Grade: </h5>
                <h5 id="section">Section: </h5>
            </div>
            <a href="/" class="btn btn-primary mt-4">← Back to API Home</a>
        </div>

        <script>
            fetch('/student')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('name').textContent = "Name: " + data.name;
                    document.getElementById('grade').textContent = "Grade: " + data.grade;
                    document.getElementById('section').textContent = "Section: " + data.section;
                })
                .catch(error => console.error('Error:', error));
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
