from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory student data (you can later replace this with a database)
student_data = {
    "name": "Your Name",
    "grade": 10,
    "section": "Zechariah"
}

# --- API Routes ---

@app.route('/student', methods=['GET'])
def get_student():
    return jsonify(student_data)

@app.route('/student', methods=['POST'])
def update_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    # Update only fields that exist
    for key in student_data:
        if key in data:
            student_data[key] = data[key]

    return jsonify({
        "message": "Student data updated successfully!",
        "student": student_data
    })


# --- Dashboard Route (Default Page) ---
@app.route('/')
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
                max-width: 500px;
                margin: auto;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            input {
                margin-bottom: 10px;
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
                <hr>
                <h5>✏️ Edit Student Info</h5>
                <form id="updateForm">
                    <input type="text" id="inputName" class="form-control" placeholder="Enter new name" required>
                    <input type="number" id="inputGrade" class="form-control" placeholder="Enter new grade" required>
                    <input type="text" id="inputSection" class="form-control" placeholder="Enter new section" required>
                    <button type="submit" class="btn btn-primary w-100 mt-2">Update Student</button>
                </form>
                <p id="message" class="mt-3 text-success"></p>
            </div>
        </div>

        <script>
            function loadStudent() {
                fetch('/student')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('name').textContent = "Name: " + data.name;
                        document.getElementById('grade').textContent = "Grade: " + data.grade;
                        document.getElementById('section').textContent = "Section: " + data.section;

                        // Fill the form with current values
                        document.getElementById('inputName').value = data.name;
                        document.getElementById('inputGrade').value = data.grade;
                        document.getElementById('inputSection').value = data.section;
                    })
                    .catch(error => console.error('Error loading student data:', error));
            }

            document.getElementById('updateForm').addEventListener('submit', function(e) {
                e.preventDefault();

                const updatedData = {
                    name: document.getElementById('inputName').value,
                    grade: document.getElementById('inputGrade').value,
                    section: document.getElementById('inputSection').value
                };

                fetch('/student', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatedData)
                })
                .then(response => response.json())
                .then(result => {
                    document.getElementById('message').textContent = result.message;
                    loadStudent(); // refresh displayed info
                })
                .catch(error => console.error('Error updating student:', error));
            });

            // Load student info on page load
            loadStudent();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == '__main__':
    app.run(debug=True)
