from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory list of students (you can replace this with a database later)
students = [
    {"name": "Your Name", "grade": 10, "section": "Zechariah"}
]

# --- API Routes ---

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "grade", "section")):
        return jsonify({"error": "Invalid data"}), 400

    students.append(data)
    return jsonify({"message": "✅ Student added successfully!", "students": students})

@app.route('/students/<int:index>', methods=['DELETE'])
def delete_student(index):
    if 0 <= index < len(students):
        removed = students.pop(index)
        return jsonify({"message": f"🗑️ Student {removed['name']} removed!", "students": students})
    else:
        return jsonify({"error": "Invalid student index"}), 400


# --- Dashboard Route ---
@app.route('/')
def dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Student Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                min-height: 100vh;
                font-family: "Poppins", sans-serif;
                color: #333;
                padding-top: 40px;
            }
            .container {
                max-width: 800px;
            }
            .card {
                border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.2);
                margin-bottom: 20px;
            }
            h1 {
                color: white;
                text-shadow: 1px 2px 5px rgba(0,0,0,0.3);
                font-weight: 700;
                text-align: center;
                margin-bottom: 30px;
            }
            button {
                border-radius: 10px;
                font-weight: 600;
            }
            table {
                margin-top: 15px;
                border-radius: 10px;
                overflow: hidden;
            }
            thead {
                background-color: #4a0dc1;
                color: white;
            }
            .btn-danger {
                background-color: #dc3545;
                border: none;
            }
            .btn-danger:hover {
                background-color: #bb2d3b;
            }
            footer {
                text-align: center;
                color: rgba(255,255,255,0.9);
                margin-top: 20px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Student Dashboard</h1>

            <div class="card p-4">
                <h4 class="text-secondary mb-3">➕ Add New Student</h4>
                <form id="addForm">
                    <div class="row g-2">
                        <div class="col-md-4">
                            <input type="text" id="inputName" class="form-control" placeholder="Full Name" required>
                        </div>
                        <div class="col-md-4">
                            <input type="number" id="inputGrade" class="form-control" placeholder="Grade" required>
                        </div>
                        <div class="col-md-4">
                            <input type="text" id="inputSection" class="form-control" placeholder="Section" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 mt-3">💾 Add Student</button>
                </form>
                <p id="message" class="mt-3 text-success"></p>
            </div>

            <div class="card p-4">
                <h4 class="text-secondary mb-3">📋 Student List</h4>
                <table class="table table-bordered table-hover align-middle text-center">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Grade</th>
                            <th>Section</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody id="studentTable"></tbody>
                </table>
            </div>

            <footer>
                © 2025 Student Dashboard | Built with Flask & Bootstrap 💻
            </footer>
        </div>

        <script>
            // Load all students into table
            function loadStudents() {
                fetch('/students')
                    .then(response => response.json())
                    .then(data => {
                        const table = document.getElementById('studentTable');
                        table.innerHTML = "";
                        data.forEach((student, index) => {
                            const row = `
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${student.name}</td>
                                    <td>${student.grade}</td>
                                    <td>${student.section}</td>
                                    <td>
                                        <button class="btn btn-danger btn-sm" onclick="deleteStudent(${index})">Delete</button>
                                    </td>
                                </tr>`;
                            table.innerHTML += row;
                        });
                    })
                    .catch(error => console.error('Error loading students:', error));
            }

            // Add student
            document.getElementById('addForm').addEventListener('submit', function(e) {
                e.preventDefault();

                const newStudent = {
                    name: document.getElementById('inputName').value,
                    grade: document.getElementById('inputGrade').value,
                    section: document.getElementById('inputSection').value
                };

                fetch('/students', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(newStudent)
                })
                .then(response => response.json())
                .then(result => {
                    document.getElementById('message').textContent = result.message;
                    loadStudents();
                    document.getElementById('addForm').reset();
                    setTimeout(() => document.getElementById('message').textContent = "", 2500);
                })
                .catch(error => console.error('Error adding student:', error));
            });

            // Delete student
            function deleteStudent(index) {
                fetch('/students/' + index, { method: 'DELETE' })
                    .then(response => response.json())
                    .then(result => {
                        document.getElementById('message').textContent = result.message;
                        loadStudents();
                        setTimeout(() => document.getElementById('message').textContent = "", 2500);
                    })
                    .catch(error => console.error('Error deleting student:', error));
            }

            // Load on page start
            loadStudents();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == '__main__':
    app.run(debug=True)
