
from flask import Flask, request, jsonify, send_from_directory
from pypdf import PdfReader
from io import BytesIO

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

KNOWN_SKILLS = [
    "python", "java", "javascript", "html", "css",
    "react", "sql", "excel", "power bi", "machine learning",
    "data analysis", "communication", "git", "flask",
    "c++", "c", "node.js", "figma"
]


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/style.css")
def stylesheet():
    return send_from_directory(".", "style.css")


@app.route("/api/suggest", methods=["POST"])
def suggest():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    branch = str(data.get("branch", "")).strip()
    interest = str(data.get("interest", "")).strip()
    skills = str(data.get("skills", "")).strip().lower()

    if not name or not branch or not interest:
        return jsonify({
            "error": "Please fill in all required fields."
        }), 400

    career_options = {
        "coding": (
            "Software Developer",
            "Learn programming, Git, and build two projects."
        ),
        "data": (
            "Data Analyst",
            "Learn Excel, SQL, Python, and data visualization."
        ),
        "design": (
            "UI/UX Designer",
            "Learn Figma, design principles, and create a portfolio."
        ),
        "networks": (
            "Network or Cybersecurity Analyst",
            "Learn networking, Linux, and security fundamentals."
        )
    }

    career, next_steps = career_options.get(
        interest,
        (
            "Explore beginner-friendly careers",
            "Start with computer fundamentals and practical projects."
        )
    )

    if "python" in skills:
        next_steps += " Practise Python and build a small application."

    return jsonify({
        "name": name,
        "branch": branch,
        "career": career,
        "next_steps": next_steps
    })


@app.route("/api/resume", methods=["POST"])
def check_resume():
    uploaded_file = request.files.get("resume")

    if not uploaded_file or not uploaded_file.filename:
        return jsonify({
            "error": "Please choose a PDF resume."
        }), 400

    if not uploaded_file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Please upload a PDF file."
        }), 400

    try:
        pdf = PdfReader(BytesIO(uploaded_file.read()))

        if pdf.is_encrypted:
            return jsonify({
                "error": "Please upload an unlocked PDF."
            }), 400

        if len(pdf.pages) > 20:
            return jsonify({
                "error": "PDF must have 20 pages or fewer."
            }), 400

        extracted_text = " ".join(
            page.extract_text() or ""
            for page in pdf.pages
        )

        if not extracted_text.strip():
            return jsonify({
                "error": "No readable text found. Please use a text-based PDF."
            }), 400

        text_lower = extracted_text.lower()

        found_skills = [
            skill for skill in KNOWN_SKILLS
            if skill in text_lower
        ]

        return jsonify({
            "filename": uploaded_file.filename,
            "skills": found_skills,
            "skill_count": len(found_skills),
            "message": (
                "Resume scanned successfully."
                if found_skills
                else "No matching skills detected. Review your resume manually."
            )
        })

    except Exception:
        return jsonify({
            "error": "Could not read this PDF. Please try another PDF resume."
        }), 400


@app.route("/api/skill-gap", methods=["POST"])
def skill_gap():
    data = request.get_json(silent=True) or {}

    role = str(data.get("role", "")).strip().lower()
    resume_skills = data.get("skills", [])

    if not isinstance(resume_skills, list):
        return jsonify({
            "error": "Skills must be a list."
        }), 400

    role_skills = {
        "python developer": [
            "python", "sql", "git", "flask", "problem solving"
        ],
        "data analyst": [
            "excel", "sql", "python", "power bi", "data analysis"
        ],
        "web developer": [
            "html", "css", "javascript", "react", "git"
        ]
    }

    if role not in role_skills:
        return jsonify({
            "error": "Please select a supported career role."
        }), 400

    current_skills = {
        str(skill).strip().lower()
        for skill in resume_skills
    }

    required = role_skills[role]

    matched = [
        skill for skill in required
        if skill in current_skills
    ]

    missing = [
        skill for skill in required
        if skill not in current_skills
    ]

    return jsonify({
        "role": role.title(),
        "matched_skills": matched,
        "missing_skills": missing,
        "message": "Practise missing skills and build projects."
    })


if __name__ == "__main__":
    app.run(debug=True)
