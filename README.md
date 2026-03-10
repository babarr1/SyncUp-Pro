# SyncUp-Pro
🚩 The "Why" 
Let’s be honest: We’ve all survived a "Group Project from Hell."

As a CS student, I got tired of the "guess-and-hope" method of finding partners, only to end up with people who have zero ambition or a completely different work ethic. This project was born out of personal frustration and a need to stop mindless scrolling and start building something that actually solves a problem I face every semester.

Sync-Up Pro is a prototype for a peer-matching system that cares about how you actually work, not just who you happen to sit next to in the lab.

🧠 The Core Idea
Standard group formation is broken because it ignores operational alignment.
This app uses Vector Space Modeling to map your project DNA. We aren't just matching names; we are calculating the "angular distance" between your habits and your peers' habits using Cosine Similarity.

Current "DNA" Metrics (The Basics):

AI Ethics: Do you automate everything with LLMs or do you prefer the manual grind?

Git Proficiency: Are you a git push --force person or do you actually understand branches?

Role Specialization: Identifying the "Frontend vs. Backend" split early to avoid overlap.

The "Crunch" Factor: Matching the "48-hours early" crowd with their own kind.

Communication: Sync vs. Async—finding people who match your meeting energy.

🛠️ Tech Stack & Constraints
Python 3.13 + Scikit-Learn: The mathematical heart of the engine.

Streamlit: Used for the UI for the sake of simplicity and speed.

The Vision: This is a Proof of Concept. While Streamlit is great for a fast prototype, the real value is the underlying logic that could be scaled into a full-stack platform or integrated into university portals.

🚀 What's Missing? (Future Roadmap)
This was built while I was being impatient and needed to put my time to good use. It’s a baseline, and there is room for so much more:

GitHub API Integration: No more sliders. The app should fetch your commit history to verify your "Git Proficiency" and tech stack automatically.

Automated Role Balancing: An algorithm that ensures a team isn't just four "Logic/Backend" devs with no one to build the UI.

Historical Peer Reviews: Incorporating a "Trust Score" based on anonymous feedback from partners in previous semesters.

Scalability: Moving beyond a generated database to a real-time database (SQL/Firebase) for an entire batch.

📈 Final Thoughts
This project is raw, basic, and a direct result of choosing "Building" over "Scrolling." It’s an attempt to quantify the "vibe" and turn group projects from a source of trauma into a streamlined, predictable process.

🏁 How to Run
pip install -r requirements.txt

streamlit run app.py
