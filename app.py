import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Sync-Up Pro", page_icon="🧬", layout="wide")

# Custom CSS for a centered, modern look
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        color: #1e40af;
        margin-top: -50px;
    }
    .sub-title {
        text-align: center;
        font-size: 20px;
        color: #64748b;
        margin-bottom: 40px;
    }
    .section-header {
        color: #1e293b;
        font-weight: 700;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .stButton>button { 
        background-color: #2563eb; 
        color: white; 
        border-radius: 8px; 
        width: 100%;
        height: 3.5em;
        font-size: 18px;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA GENERATION (Real Name Logic) ---
@st.cache_data
def load_data():
    first_names = ["Ahmed", "Zoya", "Mustafa", "Daniya", "Rayyan", "Sana", "Hashim", "Ayesha", "Usman", "Mehak"]
    last_names = ["Khan", "Ali", "Sheikh", "Ahmed", "Malik"]
    # Generate 50 unique full names
    names = [f"{fn} {ln}" for fn in first_names for ln in last_names] 
    
    data = {
        'Name': names,
        'GPA': np.round(np.random.uniform(2.8, 4.0, 50), 2),
        'AI_Usage': np.random.randint(1, 6, 50),      # 1=Anti-AI, 5=AI-First
        'Git_Skill': np.random.randint(1, 6, 50),     # 1=Manual, 5=DevOps
        'Logic_Focus': np.random.randint(1, 6, 50),   # 1=Frontend, 5=Backend
        'Deadline_Buffer': np.random.randint(1, 6, 50),
        'Comm_Style': np.random.randint(1, 6, 50)     # 1=Text, 5=Meetings
    }
    return pd.DataFrame(data)

df = load_data()

# --- 3. CENTERED HEADER ---
st.markdown('<p class="main-title">🤝 Sync-Up Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Stop gambling on group projects. Find partners who match your technical DNA.</p>', unsafe_allow_html=True)

# --- 4. THE CENTERED WORKFLOW ---
# Padding columns to keep the UI in the middle
col_p1, col_main, col_p2 = st.columns([1, 2.5, 1])

with col_main:
    st.markdown('<p class="section-header">Step 1: Your Project Partner Requirements</p>', unsafe_allow_html=True)
    st.write("Fill out the criteria below to run the vector compatibility scan.")
    
    with st.container(border=True):
        # Category A: Technical Alignment
        st.write("**Technical Standards**")
        u_gpa = st.slider("Minimum Acceptable GPA", 2.0, 4.0, 3.3)
        u_ai = st.select_slider("AI Usage Policy", options=[1, 2, 3, 4, 5], help="1: Manual only, 5: AI-Driven workflow")
        u_git = st.select_slider("Version Control Skills", options=[1, 2, 3, 4, 5], help="1: Uploads files, 5: Branches/PRs")
        
        st.divider()
        
        # Category B: Workflow Patterns
        st.write("**Workflow Patterns**")
        u_logic = st.select_slider("Role: Frontend Focus (1) vs Backend Focus (5)", options=[1, 2, 3, 4, 5])
        u_dead = st.select_slider("Deadline Management", options=[1, 2, 3, 4, 5], help="1: Final hour, 5: Days early")
        u_comm = st.select_slider("Communication Style", options=[1, 2, 3, 4, 5], help="1: Async/Slack, 5: Sync/Calls")
        
        st.write("")
        run_analysis = st.button("Run Compatibility Scan")

# --- 5. RESULTS ENGINE & DISPLAY ---
if run_analysis:
    # --- MATH: Vector Space Modeling ---
    filtered_df = df[df['GPA'] >= u_gpa].copy()
    
    if filtered_df.empty:
        st.error("No matches found. Try lowering your GPA threshold.")
    else:
        # Features for multi-dimensional analysis
        features = ['AI_Usage', 'Git_Skill', 'Logic_Focus', 'Deadline_Buffer', 'Comm_Style']
        
        # Scaling to [0,1] for accurate Cosine Similarity
        scaler = MinMaxScaler()
        db_scaled = scaler.fit_transform(filtered_df[features])
        user_vec = scaler.transform([[u_ai, u_git, u_logic, u_dead, u_comm]])
        
        # Calculate angular distance between student vectors
        scores = cosine_similarity(user_vec, db_scaled)[0]
        filtered_df['Match_Score'] = np.round(scores * 100, 1)
        
        # Identify top 3 matches
        results = filtered_df.sort_values(by='Match_Score', ascending=False).head(3)

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">Step 2: Analysis Results</p>', unsafe_allow_html=True)
        
        # Displaying the Results in Cards
        for i, (index, row) in enumerate(results.iterrows()):
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 2, 2.5])
                
                with c1:
                    st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={row['Name']}", width=120)
                    st.markdown(f"<p style='text-align: center; color: #2563eb;'><b>RANK #{i+1}</b></p>", unsafe_allow_html=True)
                
                with c2:
                    st.markdown(f"## {row['Name']}")
                    st.write(f"🎓 **GPA:** {row['GPA']}")
                    st.write(f"🧠 **Pattern Match:** {row['Match_Score']}%")
                    st.write(f"🛠️ **Focus:** {'Back-end Logic' if row['Logic_Focus'] > 3 else 'Front-end/Product'}")
                    
                with c3:
                    # Comparative Radar Chart for Pattern Overlap
                    categories = ['AI', 'Git', 'Logic', 'Deadlines', 'Comm']
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=[u_ai, u_git, u_logic, u_dead, u_comm],
                        theta=categories, fill='toself', name='You', line_color='#2563eb'
                    ))
                    fig.add_trace(go.Scatterpolar(
                        r=[row['AI_Usage'], row['Git_Skill'], row['Logic_Focus'], row['Deadline_Buffer'], row['Comm_Style']],
                        theta=categories, fill='toself', name=row['Name'], line_color='#f59e0b'
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=False, range=[0, 5])),
                        height=240, 
                        margin=dict(l=40, r=40, t=10, b=10),
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)

        # Global Data Perspective
        with st.expander("📊 View Mathematical Distribution of Eligible Partners"):
            fig_scatter = px.scatter(
                filtered_df, x='GPA', y='Match_Score', 
                size='Deadline_Buffer', color='AI_Usage', 
                hover_name='Name',
                title="Compatibility vs Academic Performance",
                color_continuous_scale='Bluered'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.write("This scatter plot maps every eligible student. The top-right quadrant identifies those who balance academic excellence with workflow compatibility.")