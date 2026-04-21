import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="NBA All-Star Predictor",
    page_icon="🏀",
    layout="wide"
)

# =============================================================================
# LOAD ARTIFACTS
# =============================================================================
@st.cache_resource
def load_artifacts():
    with open('model_artifacts.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_players():
    return pd.read_csv('current_season_stats.csv')

artifacts = load_artifacts()
players_df = load_players()

log_model = artifacts['log_model']
rf_model = artifacts['rf_model']
gb_model = artifacts['gb_model']
scaler = artifacts['scaler']
features = artifacts['features']
display_names = artifacts['display_names']
results_df = artifacts['results_df']

model_dict = {
    'Random Forest': rf_model,
    'Logistic Regression': log_model,
    'Gradient Boosting': gb_model
}

# =============================================================================
# HEADER
# =============================================================================
st.title("🏀 NBA All-Star Predictor")
st.markdown(
    "Predict whether an NBA player will be selected as an All-Star based on "
    "their regular-season per-game statistics. Built with 10 seasons of data "
    "(2014-15 to 2023-24) and three ML models."
)

st.divider()

# =============================================================================
# SIDEBAR — MODEL SELECTION
# =============================================================================
st.sidebar.header("Model Settings")
selected_model_name = st.sidebar.selectbox(
    "Choose a model",
    list(model_dict.keys()),
    index=0,
    help="Random Forest achieved the best F1 score on the test set."
)
selected_model = model_dict[selected_model_name]
needs_scaling = selected_model_name == 'Logistic Regression'

st.sidebar.divider()
st.sidebar.subheader("Model Performance (Test Set)")
for _, row in results_df.iterrows():
    label = "→ " + row.name if row.name == selected_model_name else row.name
    st.sidebar.caption(f"**{label}** — F1: {row['F1']:.3f}, AUC: {row['AUC-ROC']:.3f}")

st.sidebar.divider()
st.sidebar.caption(
    "⚠️ **Predictive importance, not causal effect.** "
    "This model predicts All-Star selection from stats — it does not claim "
    "that changing any stat causes selection. Fan voting, media narratives, "
    "and market size also influence outcomes."
)

# =============================================================================
# TABS
# =============================================================================
tab1, tab2, tab3 = st.tabs(["📊 Player Lookup", "🎛️ Custom Stats", "📈 Model Comparison"])

# =============================================================================
# TAB 1 — PLAYER LOOKUP
# =============================================================================
with tab1:
    st.subheader("Look Up a Player")
    st.markdown("Select a player from the most recent season to see their predicted All-Star probability.")

    col1, col2 = st.columns([1, 2])

    with col1:
        player_list = sorted(players_df['player'].unique())
        selected_player = st.selectbox("Select a player", player_list, index=player_list.index('LeBron James') if 'LeBron James' in player_list else 0)

        player_row = players_df[players_df['player'] == selected_player].iloc[0]

        st.markdown(f"**Team:** {player_row['team']}  |  **Position:** {player_row['pos']}  |  **Age:** {int(player_row['age'])}")
        st.markdown(f"**Games:** {int(player_row['g'])}  |  **Actual All-Star:** {'Yes ⭐' if player_row['all_star'] == 1 else 'No'}")

        # Show key stats
        st.markdown("---")
        stat_cols = st.columns(3)
        stat_cols[0].metric("PTS", f"{player_row['pts_per_game']:.1f}")
        stat_cols[1].metric("AST", f"{player_row['ast_per_game']:.1f}")
        stat_cols[2].metric("TRB", f"{player_row['trb_per_game']:.1f}")

        stat_cols2 = st.columns(3)
        stat_cols2[0].metric("STL", f"{player_row['stl_per_game']:.1f}")
        stat_cols2[1].metric("BLK", f"{player_row['blk_per_game']:.1f}")
        stat_cols2[2].metric("MP", f"{player_row['mp_per_game']:.1f}")

    with col2:
        # Get prediction
        X_player = player_row[features].values.reshape(1, -1).astype(float)
        if needs_scaling:
            X_player_input = scaler.transform(X_player)
        else:
            X_player_input = X_player

        prob = selected_model.predict_proba(X_player_input)[0][1]
        pred = "All-Star" if prob >= 0.5 else "Non All-Star"

        # Probability gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            number={'suffix': '%', 'font': {'size': 48}},
            title={'text': f"All-Star Probability ({selected_model_name})", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': '#FF6B35' if prob >= 0.5 else '#4A90D9'},
                'bgcolor': 'white',
                'steps': [
                    {'range': [0, 30], 'color': '#E8F0FE'},
                    {'range': [30, 60], 'color': '#FFF3E0'},
                    {'range': [60, 100], 'color': '#FBE9E7'}
                ],
                'threshold': {
                    'line': {'color': 'black', 'width': 3},
                    'thickness': 0.8,
                    'value': 50
                }
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(t=60, b=20, l=40, r=40))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown(f"**Prediction:** {pred} (threshold = 50%)")

        # Confidence from all 3 models
        probs_all = {}
        for mname, mobj in model_dict.items():
            if mname == 'Logistic Regression':
                Xp = scaler.transform(X_player)
            else:
                Xp = X_player
            probs_all[mname] = mobj.predict_proba(Xp)[0][1]

        st.markdown("**All model probabilities:**")
        prob_cols = st.columns(3)
        for i, (mname, mprob) in enumerate(probs_all.items()):
            prob_cols[i].metric(mname, f"{mprob:.1%}")

# =============================================================================
# TAB 2 — CUSTOM STATS
# =============================================================================
with tab2:
    st.subheader("Enter Custom Stats")
    st.markdown("Adjust the sliders to explore how different stat lines affect All-Star probability.")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("**Counting Stats**")
        pts = st.slider("Points Per Game (PTS)", 0.0, 40.0, 20.0, 0.1)
        ast = st.slider("Assists Per Game (AST)", 0.0, 15.0, 5.0, 0.1)
        trb = st.slider("Rebounds Per Game (TRB)", 0.0, 16.0, 6.0, 0.1)
        stl = st.slider("Steals Per Game (STL)", 0.0, 4.0, 1.0, 0.1)
        blk = st.slider("Blocks Per Game (BLK)", 0.0, 4.0, 0.5, 0.1)
        mp = st.slider("Minutes Per Game (MP)", 10.0, 42.0, 32.0, 0.1)
        tov = st.slider("Turnovers Per Game (TOV)", 0.0, 7.0, 2.5, 0.1)

    with col_right:
        st.markdown("**Shooting & Season Info**")
        fg_pct = st.slider("Field Goal % (FG%)", 0.0, 0.7, 0.45, 0.01)
        x3p_pct = st.slider("3-Point % (3P%)", 0.0, 0.5, 0.36, 0.01)
        ft_pct = st.slider("Free Throw % (FT%)", 0.0, 1.0, 0.80, 0.01)
        age = st.slider("Age", 19, 42, 27, 1)
        games = st.slider("Games Played (G)", 20, 82, 65, 1)
        games_started = st.slider("Games Started (GS)", 0, 82, 60, 1)

    # Build input
    custom_input = np.array([[pts, ast, trb, stl, blk, mp, fg_pct, x3p_pct, ft_pct, tov, age, games, games_started]])

    if needs_scaling:
        custom_scaled = scaler.transform(custom_input)
    else:
        custom_scaled = custom_input

    custom_prob = selected_model.predict_proba(custom_scaled)[0][1]

    # Results
    st.divider()
    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        st.metric("All-Star Probability", f"{custom_prob:.1%}")
        st.markdown(f"**Model:** {selected_model_name}")
        st.markdown(f"**Prediction:** {'⭐ All-Star' if custom_prob >= 0.5 else 'Non All-Star'}")

    with res_col2:
        # Bar chart comparing custom stats to All-Star averages
        allstar_data = pd.read_csv('nba_allstar_dataset.csv')
        as_means = allstar_data[allstar_data['all_star'] == 1][['pts_per_game', 'ast_per_game', 'trb_per_game', 'stl_per_game', 'blk_per_game', 'mp_per_game']].mean()
        custom_vals = [pts, ast, trb, stl, blk, mp]
        stat_labels = ['PTS', 'AST', 'TRB', 'STL', 'BLK', 'MP']

        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(
            name='Your Stats', x=stat_labels, y=custom_vals,
            marker_color='#FF6B35'
        ))
        fig_compare.add_trace(go.Bar(
            name='All-Star Average', x=stat_labels, y=as_means.values,
            marker_color='#4A90D9'
        ))
        fig_compare.update_layout(
            barmode='group', title='Your Stats vs. All-Star Average',
            height=350, margin=dict(t=40, b=20)
        )
        st.plotly_chart(fig_compare, use_container_width=True)

# =============================================================================
# TAB 3 — MODEL COMPARISON
# =============================================================================
with tab3:
    st.subheader("Model Comparison")
    st.markdown("Performance of all three models on the held-out test set (20% of data).")

    # Results table
    st.dataframe(results_df.style.highlight_max(axis=0, color='#FFE0B2'), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # Metrics comparison bar chart
        metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1', 'AUC-ROC']
        fig_metrics = go.Figure()
        colors = ['#4A90D9', '#FF6B35', '#2ECC71']
        for i, model_name in enumerate(results_df.index):
            fig_metrics.add_trace(go.Bar(
                name=model_name,
                x=metrics_to_plot,
                y=[results_df.loc[model_name, m] for m in metrics_to_plot],
                marker_color=colors[i]
            ))
        fig_metrics.update_layout(
            barmode='group', title='Test Set Metrics Comparison',
            yaxis_range=[0, 1], height=400
        )
        st.plotly_chart(fig_metrics, use_container_width=True)

    with col2:
        # Feature importance from Random Forest
        rf = artifacts['rf_model']
        imp_df = pd.DataFrame({
            'Feature': [display_names[f] for f in features],
            'Importance': rf.feature_importances_
        }).sort_values('Importance', ascending=True)

        fig_imp = px.bar(imp_df, x='Importance', y='Feature', orientation='h',
                         title='Random Forest Feature Importance',
                         color='Importance', color_continuous_scale='OrRd')
        fig_imp.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_imp, use_container_width=True)

    st.info(
        "⚠️ **Predictive importance, not causal effect.** Feature importance reflects "
        "which stats are most useful for the model's predictions — not that changing a stat "
        "causes All-Star selection. Fan voting, coach picks, media narratives, and team market "
        "size all influence selection but are not captured in this model."
    )
