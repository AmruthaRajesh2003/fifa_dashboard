import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data import get_match_data, get_top_scorers, get_team_stats, get_upcoming_matches, get_team_history, get_venue_map_data
from live_data import get_wc_matches, get_wc_standings, get_wc_scorers
from data import get_match_data, get_top_scorers,get_team_stats,get_upcoming_matches,get_team_history,get_venue_map_data, get_player_history
from streamlit_autorefresh import st_autorefresh

# Page Config
st.set_page_config(
    page_title="FIFA World Cup 2026 Dashboard",
    page_icon="⚽",
    layout="wide"
)
st.markdown("""
<style>
/* Mild dark background */
.stApp {
    background: linear-gradient(135deg, #0d2818 0%, #1a3a4a 40%, #0a1f35 100%);
}

/* Mild green/teal accents instead of bright yellow */
h1, h2, h3 { color: #4fc3a1 !important; }
.stMetric { background: rgba(79, 195, 161, 0.1); border-radius: 10px; }
            
@keyframes bounce{
    0% { top: 10%; }
    50% { top: 80%; }
    100% { left: 10%; }
            }

@keyframes run {
    0% { left: -8%; }
    100% { left: 108%; }
}
@keyframes runLeft {
    0% { left: 108%; }
    100% { left: -8%; }
}

.player-run {
    position: fixed;
    font-size: 3.5rem;
    opacity: 0.35;
    z-index: 0;
    pointer-events: none;
    animation: run linear infinite;
}
.player-run-left {
    position: fixed;
    font-size: 3.5rem;
    opacity: 0.35;
    z-index: 0;
    pointer-events: none;
    animation: runLeft linear infinite;
    transform: scaleX(-1);
}
</style>

<!-- Players running left to right -->
<div class="player-run" style="top:15%; animation-duration:12s;">🏃⚽</div>
<div class="player-run" style="top:45%; animation-duration:16s; animation-delay:4s;">🏃</div>
<div class="player-run" style="top:75%; animation-duration:14s; animation-delay:8s;">🏃⚽</div>

<!-- Players running right to left -->
<div class="player-run-left" style="top:30%; animation-duration:13s; animation-delay:2s;">🏃</div>
<div class="player-run-left" style="top:60%; animation-duration:15s; animation-delay:6s;">🏃⚽</div>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #0a1628; }
    .title-container {
        background: linear-gradient(135deg, #1a472a, #2d6a4f, #1a472a);
        padding: 30px; border-radius: 15px; text-align: center;
        margin-bottom: 20px; border: 2px solid #FFD700;
        box-shadow: 0 0 30px rgba(255,215,0,0.3);
    }
    .title-text { color: #FFD700; font-size: 42px; font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5); margin: 0; }
    .subtitle-text { color: #90EE90; font-size: 16px; margin-top: 5px; }
    .kpi-card {
        background: linear-gradient(135deg, #1a472a, #2d6a4f);
        border-radius: 12px; padding: 20px; text-align: center;
        border: 1px solid #FFD700;
        box-shadow: 0 4px 15px rgba(255,215,0,0.2); margin: 5px;
    }
    .kpi-number { color: #FFD700; font-size: 36px; font-weight: 900; margin: 0; }
    .kpi-label { color: #90EE90; font-size: 14px; margin: 0; }
    .player-card {
        background: linear-gradient(135deg, #1a3a5c, #0d2137);
        border-radius: 12px; padding: 15px; text-align: center;
        border: 1px solid #4a90d9;
        box-shadow: 0 4px 15px rgba(74,144,217,0.2); margin: 8px;
    }
    .player-flag { font-size: 40px; margin-bottom: 8px; }
    .player-name { color: #FFD700; font-size: 16px; font-weight: 700; margin: 5px 0; }
    .player-country { color: #90EE90; font-size: 13px; margin: 3px 0; }
    .player-goals {
        background: #FFD700; color: #000; border-radius: 20px;
        padding: 3px 12px; font-weight: 900; font-size: 14px;
        display: inline-block; margin-top: 5px;
    }
    .team-card {
        background: linear-gradient(135deg, #2d1b4e, #1a0f2e);
        border-radius: 12px; padding: 15px; text-align: center;
        border: 1px solid #9b59b6; margin: 8px;
    }
    .upcoming-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 12px; padding: 15px; text-align: center;
        border: 1px solid #0f3460; margin: 8px;
        box-shadow: 0 4px 15px rgba(15,52,96,0.4);
    }
    .predict-card {
        background: linear-gradient(135deg, #0d1b2a, #1b2838);
        border-radius: 15px; padding: 25px; text-align: center;
        border: 2px solid #4a90d9;
        box-shadow: 0 0 25px rgba(74,144,217,0.3);
    }
    .live-badge {
        background: #e74c3c; color: white; border-radius: 20px;
        padding: 3px 10px; font-size: 12px; font-weight: 700;
        display: inline-block; animation: pulse 1s infinite;
    }
    .section-header {
        color: #FFD700; font-size: 24px; font-weight: 800;
        border-left: 4px solid #FFD700;
        padding-left: 10px; margin: 20px 0 15px 0;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Auto Refresh every 5 minutes
st_autorefresh(interval=300000, key="fifa_refresh")

# Title
st.markdown("""
<div class="title-container">
    <p class="title-text">⚽ FIFA World Cup 2026</p>
    <p class="subtitle-text">🏟️ USA • Canada • Mexico | 
    <span class="live-badge">🔴 LIVE</span> Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Load Simulated Data
matches = get_match_data()
scorers = get_top_scorers()
teams = get_team_stats()
upcoming = get_upcoming_matches()
history = get_team_history()
venues = get_venue_map_data()

# Load Live Data
live_matches = get_wc_matches()
live_standings = get_wc_standings()
live_scorers = get_wc_scorers()

# Live Status
st.markdown('<p class="section-header">🔴 Live Data Status</p>',
            unsafe_allow_html=True)
col_l1, col_l2, col_l3 = st.columns(3)
with col_l1:
    if live_matches is not None and len(live_matches) > 0:
        st.success(f"✅ Live Matches: {len(live_matches)} loaded")
    else:
        st.warning("⚠️ Using simulated match data")
with col_l2:
    if live_standings is not None and len(live_standings) > 0:
        st.success("✅ Live Standings loaded")
    else:
        st.warning("⚠️ Using simulated standings")
with col_l3:
    if live_scorers is not None and len(live_scorers) > 0:
        st.success(f"✅ Live Scorers: {len(live_scorers)} loaded")
    else:
        st.warning("⚠️ Using simulated scorers")

st.markdown("---")

# Use live or fallback
matches_data = live_matches if (live_matches is not None and len(live_matches) > 0) else matches
scorers_data = live_scorers if (live_scorers is not None and len(live_scorers) > 0) else scorers

# Flags
flags = {
    'Brazil':'🇧🇷','France':'🇫🇷','Germany':'🇩🇪','Argentina':'🇦🇷',
    'Spain':'🇪🇸','Portugal':'🇵🇹','England':'🏴󠁧󠁢󠁥󠁮󠁧󠁿','Netherlands':'🇳🇱',
    'Belgium':'🇧🇪','Croatia':'🇭🇷','Denmark':'🇩🇰','Serbia':'🇷🇸',
    'USA':'🇺🇸','Mexico':'🇲🇽','Canada':'🇨🇦','Ecuador':'🇪🇨',
    'Uruguay':'🇺🇾','Colombia':'🇨🇴','Japan':'🇯🇵','South Korea':'🇰🇷',
    'Australia':'🇦🇺','Morocco':'🇲🇦','Senegal':'🇸🇳','Ghana':'🇬🇭',
    'Norway':'🇳🇴','Switzerland':'🇨🇭','Cameroon':'🇨🇲','Tunisia':'🇹🇳',
    'Iran':'🇮🇷','Saudi Arabia':'🇸🇦'
}

# KPI Cards
st.markdown('<p class="section-header">📊 Tournament Overview</p>',
            unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-number">🏟️ {len(matches_data)}</p>
        <p class="kpi-label">Total Matches</p></div>""",
        unsafe_allow_html=True)
with col2:
    if 'Total_Goals' in matches_data.columns:
        total_goals = int(matches_data['Total_Goals'].sum())
    else:
        g1 = pd.to_numeric(matches_data.get('Team1_Goals', pd.Series([0])), errors='coerce').fillna(0)
        g2 = pd.to_numeric(matches_data.get('Team2_Goals', pd.Series([0])), errors='coerce').fillna(0)
        total_goals = int((g1 + g2).sum())
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-number">⚽ {total_goals}</p>
        <p class="kpi-label">Total Goals</p></div>""",
        unsafe_allow_html=True)
with col3:
    avg_goals = round(total_goals / max(len(matches_data), 1), 2)
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-number">📈 {avg_goals}</p>
        <p class="kpi-label">Avg Goals/Match</p></div>""",
        unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="kpi-card">
        <p class="kpi-number">🌍 48</p>
        <p class="kpi-label">Teams Competing</p></div>""",
        unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📋 Match Results",
    "📅 Upcoming Matches",
    "🔮 Prediction",
    "🥅 Top Scorers",
    "🏆 Team Stats & History",
    "🗺️ Venue Map",
    "📊 Live Standings",
    "👤 Player History",
    "📈 Analytics Dashboard",
    "⚔️ Team Comparison"
])

# ── Tab 1: Match Results ──
with tab1:
    st.markdown('<p class="section-header">📋 Match Results</p>',
                unsafe_allow_html=True)
    if 'Group' in matches_data.columns:
        group_filter = st.selectbox(
            "🔍 Filter by Group",
            ["All"] + sorted(matches_data['Group'].dropna().unique().tolist())
        )
        filtered = matches_data if group_filter == "All" else matches_data[matches_data['Group'] == group_filter]
    else:
        filtered = matches_data

    display = filtered.copy()
    if 'Date' in display.columns:
        try:
            display['Date'] = pd.to_datetime(display['Date']).dt.strftime('%Y-%m-%d')
        except:
            pass
    if 'Team1' in display.columns:
        display['Team1'] = display['Team1'].apply(lambda x: f"{flags.get(x,'🏳️')} {x}")
    if 'Team2' in display.columns:
        display['Team2'] = display['Team2'].apply(lambda x: f"{flags.get(x,'🏳️')} {x}")
    st.dataframe(display, use_container_width=True, height=400)

# ── Tab 2: Upcoming Matches ──
with tab2:
    st.markdown('<p class="section-header">📅 Upcoming Matches</p>',
                unsafe_allow_html=True)

    # Show live upcoming if available
    if live_matches is not None and len(live_matches) > 0:
        upcoming_live = live_matches[live_matches['Status'].isin(
            ['SCHEDULED', 'TIMED'])] if 'Status' in live_matches.columns else pd.DataFrame()
        if len(upcoming_live) > 0:
            st.markdown("### 🔴 Live Schedule")
            st.dataframe(upcoming_live, use_container_width=True)
        else:
            st.info("No upcoming live matches found")
    else:
        st.markdown("### 🗓️ Scheduled Matches")
        for _, row in upcoming.iterrows():
            flag1 = flags.get(row['Team1'], '🏳️')
            flag2 = flags.get(row['Team2'], '🏳️')
            st.markdown(f"""
            <div class="upcoming-card">
                <div style="color:#aaa; font-size:12px; margin-bottom:8px">
                    📅 {row['Date']} &nbsp;|&nbsp; 🕐 {row['Time']} 
                    &nbsp;|&nbsp; 🏟️ {row['Venue']} 
                    &nbsp;|&nbsp; Group {row['Group']}
                </div>
                <div style="display:flex; justify-content:center;
                            align-items:center; gap:20px">
                    <div>
                        <div style="font-size:35px">{flag1}</div>
                        <div style="color:#FFD700; font-weight:700; font-size:16px">
                            {row['Team1']}</div>
                    </div>
                    <div style="color:#FFD700; font-size:28px; font-weight:900">VS</div>
                    <div>
                        <div style="font-size:35px">{flag2}</div>
                        <div style="color:#FFD700; font-weight:700; font-size:16px">
                            {row['Team2']}</div>
                    </div>
                </div>
            </div><br>
            """, unsafe_allow_html=True)

# ── Tab 3: Prediction ──
with tab3:
    st.markdown('<p class="section-header">🔮 Match Prediction</p>',
                unsafe_allow_html=True)
    st.markdown("#### Select two teams to predict the winner!")

    all_teams = teams['Team'].tolist()
    col1, col2 = st.columns(2)
    with col1:
        team_a = st.selectbox("🔵 Team A", all_teams, index=0)
    with col2:
        team_b = st.selectbox("🔴 Team B", all_teams, index=1)

    if st.button("🔮 Predict Winner!", use_container_width=True):
        if team_a == team_b:
            st.warning("⚠️ Please select two different teams!")
        else:
            a = teams[teams['Team'] == team_a].iloc[0]
            b = teams[teams['Team'] == team_b].iloc[0]

            score_a = (a['Wins']*3 + a['Draws'] + a['Points'] +
                      a['Goals_For'] - a['Goals_Against'])
            score_b = (b['Wins']*3 + b['Draws'] + b['Points'] +
                      b['Goals_For'] - b['Goals_Against'])
            total = score_a + score_b

            prob_a = round((score_a / total) * 100, 1)
            prob_b = round((score_b / total) * 100, 1)

            winner = team_a if prob_a > prob_b else (team_b if prob_b > prob_a else "Draw")
            winner_flag = flags.get(winner, '🤝')
            fa = flags.get(team_a, '🏳️')
            fb = flags.get(team_b, '🏳️')

            st.markdown(f"""
            <div class="predict-card">
                <div style="font-size:18px; color:#aaa; margin-bottom:15px">
                    🔮 Prediction Result
                </div>
                <div style="display:flex; justify-content:center;
                            align-items:center; gap:30px; margin-bottom:20px">
                    <div>
                        <div style="font-size:50px">{fa}</div>
                        <div style="color:#FFD700; font-size:18px; font-weight:700">
                            {team_a}</div>
                        <div style="color:#2ecc71; font-size:28px; font-weight:900">
                            {prob_a}%</div>
                    </div>
                    <div style="color:#FFD700; font-size:32px; font-weight:900">VS</div>
                    <div>
                        <div style="font-size:50px">{fb}</div>
                        <div style="color:#FFD700; font-size:18px; font-weight:700">
                            {team_b}</div>
                        <div style="color:#e74c3c; font-size:28px; font-weight:900">
                            {prob_b}%</div>
                    </div>
                </div>
                <div style="font-size:28px; margin-top:15px">🏆</div>
                <div style="color:#FFD700; font-size:22px; font-weight:900">
                    Predicted Winner: {winner_flag} {winner}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📊 Head to Head Comparison")
            comp = pd.DataFrame({
                'Stat': ['Wins','Draws','Losses','Goals For','Goals Against','Points'],
                team_a: [a['Wins'],a['Draws'],a['Losses'],
                         a['Goals_For'],a['Goals_Against'],a['Points']],
                team_b: [b['Wins'],b['Draws'],b['Losses'],
                         b['Goals_For'],b['Goals_Against'],b['Points']]
            })
            fig_comp = px.bar(
                comp, x='Stat', y=[team_a, team_b],
                barmode='group', title='Head to Head Stats',
                color_discrete_sequence=['#2ecc71','#e74c3c']
            )
            fig_comp.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig_comp, use_container_width=True)

# ── Tab 4: Top Scorers ──
with tab4:
    st.markdown('<p class="section-header">🥅 Top Scorers</p>',
                unsafe_allow_html=True)

    display_scorers = scorers_data.head(10) if len(scorers_data) > 0 else scorers

    cols = st.columns(5)
    for i, row in display_scorers.iterrows():
        with cols[i % 5]:
            country = row.get('Country', row.get('team', ''))
            flag = flags.get(country, '🏳️')
            goals = row.get('Goals', row.get('goals', 0))
            assists = row.get('Assists', row.get('assists', 0))
            player = row.get('Player', row.get('player', 'Unknown'))
            st.markdown(f"""
            <div class="player-card">
                <div class="player-flag">{flag}</div>
                <div class="player-name">{player}</div>
                <div class="player-country">{country}</div>
                <div class="player-goals">⚽ {goals} Goals</div>
                <div style="color:#aaa; font-size:12px; margin-top:5px">
                    🎯 {assists} Assists</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    fig_scorers = px.bar(
        display_scorers,
        x=display_scorers.get('Goals', display_scorers.columns[2]),
        y=display_scorers.get('Player', display_scorers.columns[0]),
        orientation='h',
        color='Goals' if 'Goals' in display_scorers.columns else display_scorers.columns[2],
        color_continuous_scale='YlOrRd',
        title='⚽ Top Goal Scorers',
        text='Goals' if 'Goals' in display_scorers.columns else display_scorers.columns[2]
    )
    fig_scorers.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white', title_font_size=20,
        yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_scorers, use_container_width=True)

# ── Tab 5: Team Stats & History ──
with tab5:
    st.markdown('<p class="section-header">🏆 Team Stats & History</p>',
                unsafe_allow_html=True)

    cols = st.columns(5)
    for i, row in teams.iterrows():
        with cols[i % 5]:
            flag = flags.get(row['Team'], '🏳️')
            h = history.get(row['Team'], {})
            st.markdown(f"""
            <div class="team-card">
                <div style="font-size:35px">{flag}</div>
                <div style="color:#FFD700; font-weight:700; font-size:14px; margin:5px 0">
                    {row['Team']}</div>
                <div style="color:#2ecc71; font-size:12px">✅ W: {row['Wins']}</div>
                <div style="color:#f39c12; font-size:12px">🤝 D: {row['Draws']}</div>
                <div style="color:#e74c3c; font-size:12px">❌ L: {row['Losses']}</div>
                <div style="color:#aaa; font-size:11px; margin-top:5px">
                    🏆 Titles: {h.get('WC_Titles','?')}</div>
                <div style="color:#aaa; font-size:11px">
                    📅 2022: {h.get('Last_WC','?')}</div>
                <div style="background:#FFD700; color:#000; border-radius:10px;
                            padding:2px 8px; font-weight:900; margin-top:8px; font-size:13px">
                    {row['Points']} pts</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📖 Team World Cup History")
    selected_team = st.selectbox(
        "Select a team",
        list(history.keys()),
        format_func=lambda x: f"{flags.get(x,'🏳️')} {x}"
    )
    h = history[selected_team]
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="kpi-card">
        <p class="kpi-number">{h['WC_Titles']} 🏆</p>
        <p class="kpi-label">WC Titles</p></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="kpi-card">
        <p class="kpi-number">{h['Finals']}</p>
        <p class="kpi-label">Finals Played</p></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="kpi-card">
        <p class="kpi-number" style="font-size:18px">{h['Best']}</p>
        <p class="kpi-label">Best Result</p></div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div class="kpi-card">
        <p class="kpi-number" style="font-size:18px">{h['Last_WC']}</p>
        <p class="kpi-label">Last WC 2022</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    fig_teams = px.bar(
        teams, x='Team', y=['Wins','Draws','Losses'],
        title='🏆 Win/Draw/Loss by Team', barmode='group',
        color_discrete_map={'Wins':'#2ecc71','Draws':'#f39c12','Losses':'#e74c3c'}
    )
    fig_teams.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white', title_font_size=20
    )
    st.plotly_chart(fig_teams, use_container_width=True)

# ── Tab 6: Venue Map ──
with tab6:
    st.markdown('<p class="section-header">🗺️ Match Venues — USA 2026</p>',
                unsafe_allow_html=True)
    fig_map = px.scatter_mapbox(
        venues, lat='Lat', lon='Lon',
        hover_name='City',
        hover_data={'Stadium':True,'Capacity':True,'Matches':True,
                    'Lat':False,'Lon':False},
        size='Matches', color='Matches',
        color_continuous_scale='YlOrRd',
        size_max=25, zoom=3,
        title='🏟️ FIFA WC 2026 Stadiums'
    )
    fig_map.update_layout(
        mapbox_style='open-street-map',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white', height=500,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("#### 🏟️ Stadium Details")
    st.dataframe(venues, use_container_width=True)

# ── Tab 7: Live Standings ──
with tab7:
    st.markdown('<p class="section-header">📊 Group Stage Standings</p>',
                unsafe_allow_html=True)

    if live_standings is not None and len(live_standings) > 0:
        st.success("🔴 Live Standings from API!")
        groups = live_standings['Group'].unique()
        for group in groups:
            st.markdown(f"#### Group {group}")
            group_df = live_standings[live_standings['Group'] == group]
            group_df['Team'] = group_df['Team'].apply(
                lambda x: f"{flags.get(x,'🏳️')} {x}")
            st.dataframe(group_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Live standings unavailable — showing simulated data")
        from data import get_group_standings
        try:
            standings = get_group_standings()
            groups = standings['Group'].unique()
            cols = st.columns(2)
            for idx, group in enumerate(groups):
                with cols[idx % 2]:
                    st.markdown(f"#### ⚽ Group {group}")
                    group_df = standings[standings['Group'] == group][
                        ['Team','Played','Wins','Draws','Losses',
                         'GF','GA','GD','Points']].copy()
                    group_df['Team'] = group_df['Team'].apply(
                        lambda x: f"{flags.get(x,'🏳️')} {x}")
                    st.dataframe(group_df, use_container_width=True,
                                hide_index=True)
        except:
            st.info("Add get_group_standings() to data.py to see standings!")

 # ── Tab 8: Player History ──
with tab8:
    st.markdown('<p class="section-header">👤 Player History & Career Stats</p>',
                unsafe_allow_html=True)

    from data import get_player_history
    player_history = get_player_history()

    # Player selector
    selected_player = st.selectbox(
        "🔍 Select a Player",
        list(player_history.keys())
    )

# ── Tab 9: Analytics Dashboard 
with tab9:
    st.subheader("📈 Tournament Analytics")

fig = px.bar(
    teams,
    x="Team",
    y="Goals_For",
    title="Goals Scored by Teams"
)
st.plotly_chart(fig, use_container_width=True)

fig2 = px.pie(
    teams,
    names="Team",
    values="Points",
    title="Points Distribution"
)
st.plotly_chart(fig2, use_container_width=True)
# ── Tab 10:Team Comparison
team1 = st.selectbox(
    "Team A",
    teams["Team"].tolist(),
    key="t1"
)

team2 = st.selectbox(
    "Team B",
    teams["Team"].tolist(),
    key="t2"
)

if team1 != team2:

    t1 = teams[teams["Team"] == team1].iloc[0]
    t2 = teams[teams["Team"] == team2].iloc[0]

    comparison = pd.DataFrame({
        "Stat": ["Wins","Goals_For","Goals_Against","Points"],
        team1: [
            t1["Wins"],
            t1["Goals_For"],
            t1["Goals_Against"],
            t1["Points"]
        ],
        team2: [
            t2["Wins"],
            t2["Goals_For"],
            t2["Goals_Against"],
            t2["Points"]
        ]
    })

    st.dataframe(comparison)

    fig = px.bar(
        comparison,
        x="Stat",
        y=[team1, team2],
        barmode="group"
    )

    st.plotly_chart(fig)
    p = player_history[selected_player]
    flag = flags.get(p['Country'], '🏳️')

    # Player Header Card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a3a5c, #0d2137);
                border-radius: 15px; padding: 25px; text-align: center;
                border: 2px solid #4a90d9; margin-bottom: 20px;
                box-shadow: 0 0 25px rgba(74,144,217,0.3);">
        <div style="font-size: 60px">{flag}</div>
        <div style="color: #FFD700; font-size: 28px; font-weight: 900;
                    margin: 10px 0">{selected_player}</div>
        <div style="color: #90EE90; font-size: 16px">{p['Country']} | {p['Club']}</div>
        <div style="color: #aaa; font-size: 14px; margin-top: 5px">
            {p['Position']} | Age: {p['Age']}
        </div>
        <div style="background: #FFD700; color: #000; border-radius: 20px;
                    padding: 5px 15px; font-weight: 900; font-size: 14px;
                    display: inline-block; margin-top: 10px">
            💬 {p['Fun_Fact']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Career Stats
    st.markdown("#### 📊 Career Statistics")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="kpi-card">
        <p class="kpi-number">⚽ {p['Career_Goals']}</p>
        <p class="kpi-label">Career Goals</p></div>""",
        unsafe_allow_html=True)
    c2.markdown(f"""<div class="kpi-card">
        <p class="kpi-number">🎯 {p['Career_Assists']}</p>
        <p class="kpi-label">Career Assists</p></div>""",
        unsafe_allow_html=True)
    c3.markdown(f"""<div class="kpi-card">
        <p class="kpi-number" style="font-size:18px">{p['WC_2018']}</p>
        <p class="kpi-label">WC 2018</p></div>""",
        unsafe_allow_html=True)
    c4.markdown(f"""<div class="kpi-card">
        <p class="kpi-number" style="font-size:18px">{p['WC_2022']}</p>
        <p class="kpi-label">WC 2022</p></div>""",
        unsafe_allow_html=True)

    # Goals vs Assists Chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📈 All Players — Goals vs Assists")
    player_df = pd.DataFrame([
        {
            'Player': name,
            'Goals': data['Career_Goals'],
            'Assists': data['Career_Assists'],
            'Country': data['Country'],
            'Club': data['Club']
        }
        for name, data in player_history.items()
    ])

    fig_scatter = px.scatter(
        player_df,
        x='Goals', y='Assists',
        text='Player',
        color='Country',
        size='Goals',
        title='Career Goals vs Assists',
        hover_data=['Club'],
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=20,
        height=500
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # All Players Table
    st.markdown("#### 📋 All Players Overview")
    st.dataframe(player_df, use_container_width=True, hide_index=True) 

# Footer
st.markdown("""
<div style='text-align:center; padding:20px;
            background:linear-gradient(135deg,#1a472a,#2d6a4f);
            border-radius:10px; margin-top:20px; border:1px solid #FFD700'>
    <p style='color:#FFD700; font-size:16px; margin:0'>
        ⚽ FIFA World Cup 2026 Analytics Dashboard
    </p>
    <p style='color:#90EE90; font-size:12px; margin:5px 0 0 0'>
        🔴 Live Data • Made with ❤️ using Python & Streamlit
    </p>
</div>
""", unsafe_allow_html=True)