from flask import Flask # type: ignore
from flask import render_template # type: ignore
from flask import request # type: ignore
from flask import redirect # type: ignore
from flask import url_for # type: ignore
from collections import Counter

import os
import sqlite3
import joblib # type: ignore

from utils import (
    extract_text,
    clean_text,
    extract_skills,
    calculate_score,
    extract_name,
    extract_email,
    extract_phone,
    extract_education,
    get_rating
)
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load AI Model

model = joblib.load(
    "models/model.pkl"
)

tfidf = joblib.load(
    "models/tfidf.pkl"
)

encoder = joblib.load(
    "models/encoder.pkl"
)

@app.route("/")
def home():

    return render_template(
        "index.html"
    )
    

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    files = request.files.getlist(
        "resume"
    )

    conn = sqlite3.connect(
        "database.db"
    )

    cursor = conn.cursor()

    for file in files:

        filename = file.filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        text = extract_text(filepath)

        candidate_name = extract_name(text)

        email = extract_email(text)

        phone = extract_phone(text)

        education = extract_education(text)

        print("\n")
        print("========== RESUME TEXT ==========")
        print(text[:1000])
        print("=================================")

        print("EMAIL:", email)
        print("PHONE:", phone)
        print("EDUCATION:", education)
        print("\n")

        cleaned = clean_text(text)

        vector = tfidf.transform(
            [cleaned]
        )

        prediction = model.predict(
            vector
        )
        
        probabilities = model.predict_proba(
            vector
        )[0]

        all_roles = encoder.classes_

        role_probs = list(
            zip(all_roles, probabilities)
        )

        role_probs.sort(
            key=lambda x: x[1],
            reverse=True
        )

        confidence = round(
            role_probs[0][1] * 100,
            2
        )

        second_role = role_probs[1][0]

        second_confidence = round(
            role_probs[1][1] * 100,
            2
        )

        role = encoder.inverse_transform(
            prediction
        )[0]

        skills = extract_skills(
            cleaned
        )

        score = calculate_score(
            skills
        )

        cursor.execute(
        """
        INSERT INTO candidates
        (
            name,
            email,
            phone,
            education,
            role,
            score,
            skills,
            resume_path,
            confidence,
            second_role,
            second_confidence
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            candidate_name,
            email,
            phone,
            education,
            role,
            score,
            ",".join(skills),
            filepath,
            confidence,
            second_role,
            second_confidence
        )
        )

    conn.commit()
    conn.close()

    return redirect(
        url_for("results")
    )
    

@app.route("/results")
def results():

    conn = sqlite3.connect(
        "database.db"
    )

    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT *
    FROM candidates
    ORDER BY role,score DESC
    """
    )

    candidates = cursor.fetchall()

    conn.close()

    grouped = {}

    for candidate in candidates:

        role = candidate[5]

        if role not in grouped:

            grouped[role] = []

        grouped[role].append(
            candidate
        )
    
    total_candidates = len(candidates)
    
    role_counts = {}

    for role, candidates_list in grouped.items():
        role_counts[role] = len(candidates_list)
    
    avg_score = 0
    
    for c in candidates:
        print(c)

    if candidates:
        avg_score = round(
            sum(c[6] for c in candidates if c[6] is not None) / len(candidates),
            2
        )

    return render_template(
        "results.html",
        grouped=grouped,
        role_counts=role_counts,
        total_candidates=total_candidates,
        avg_score=avg_score
    )
    

@app.route(
    "/candidate/<int:id>"
)
def candidate(id):

    conn = sqlite3.connect(
        "database.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM candidates
        WHERE id=?
        """,
        (id,)
    )

    candidate = cursor.fetchone()

    conn.close()

    rating = get_rating(candidate[6])

    return render_template(
        "candidate.html",
        candidate=candidate,
        rating=rating
    )
    

if __name__ == "__main__":

    app.run(
        debug=True
    )