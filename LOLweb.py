import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# 웹사이트 기본 설정
st.set_page_config(page_title="LoL Worlds History & 2025 Recap", page_icon="🏆", layout="wide")

# 1. 프리미엄 e스포츠 테마 CSS 주입
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Noto+Sans+KR:wght@300;400;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Noto Sans KR', sans-serif !important;
    background-color: #0a0a0c !important; 
    color: #f0e6d2 !important; 
}

h1, h2, h3 {
    font-family: 'Oswald', 'Noto Sans KR', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #c8aa6e !important; 
}

.stTabs [data-baseweb="tab-list"] { gap: 24px; }
.stTabs [data-baseweb="tab"] { color: #a09b8c; font-weight: 600; padding-bottom: 10px; }
.stTabs [aria-selected="true"] { color: #c8aa6e !important; border-bottom-color: #c8aa6e !important; }

[data-testid="stDataFrame"] div { background-color: #111115 !important; color: #f0e6d2 !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 2. 데이터 세팅
# 역대 롤드컵 전체 결과 및 결승전 MVP 데이터 (2011-2025)
history_data = [
    {"Year": 2011, "Winner": "Fnatic", "Runner_up": "aAa", "Top_4": "-", "Top_8": "-", "Score": "2:0", "Host": "Sweden", "MVP": "Shushei"},
    {"Year": 2012, "Winner": "TPA", "Runner_up": "Azubu Frost", "Top_4": "-", "Top_8": "-", "Score": "3:1", "Host": "USA", "MVP": "Toyz"},
    {"Year": 2013, "Winner": "SKT T1", "Runner_up": "Royal Club", "Top_4": "-", "Top_8": "-", "Score": "3:0", "Host": "USA", "MVP": "Faker"},
    {"Year": 2014, "Winner": "SSW", "Runner_up": "Star Horn", "Top_4": "-", "Top_8": "-", "Score": "3:1", "Host": "South Korea", "MVP": "Mata"},
    {"Year": 2015, "Winner": "SKT T1", "Runner_up": "KOO Tigers", "Top_4": "-", "Top_8": "-", "Score": "3:1", "Host": "Europe", "MVP": "MaRin"},
    {"Year": 2016, "Winner": "SKT T1", "Runner_up": "SSG", "Top_4": "-", "Top_8": "-", "Score": "3:2", "Host": "USA", "MVP": "Faker"},
    {"Year": 2017, "Winner": "SSG", "Runner_up": "SKT T1", "Top_4": "-", "Top_8": "-", "Score": "3:0", "Host": "China", "MVP": "Ruler"},
    {"Year": 2018, "Winner": "IG", "Runner_up": "Fnatic", "Top_4": "-", "Top_8": "-", "Score": "3:0", "Host": "South Korea", "MVP": "Ning"},
    {"Year": 2019, "Winner": "FPX", "Runner_up": "G2 Esports", "Top_4": "-", "Top_8": "-", "Score": "3:0", "Host": "Europe", "MVP": "Tian"},
    {"Year": 2020, "Winner": "DWG", "Runner_up": "Suning", "Top_4": "-", "Top_8": "-", "Score": "3:1", "Host": "China", "MVP": "Canyon"},
    {"Year": 2021, "Winner": "EDG", "Runner_up": "DK", "Top_4": "-", "Top_8": "-", "Score": "3:2", "Host": "Iceland", "MVP": "Scout"},
    {"Year": 2022, "Winner": "DRX", "Runner_up": "T1", "Top_4": "-", "Top_8": "-", "Score": "3:2", "Host": "USA", "MVP": "Kingen"},
    {"Year": 2023, "Winner": "T1", "Runner_up": "WBG", "Top_4": "-", "Top_8": "-", "Score": "3:0", "Host": "South Korea", "MVP": "Zeus"},
    {"Year": 2024, "Winner": "T1", "Runner_up": "BLG", "Top_4": "-", "Top_8": "-", "Score": "3:2", "Host": "Europe", "MVP": "Faker"},
    {"Year": 2025, "Winner": "T1", "Runner_up": "KT Rolster", "Top_4": "T1, KT Rolster, BLG, WBG", "Top_8": "Gen.G, JDG, T1, KT Rolster, BLG, TES, G2 Esports, HLE", "Score": "3:2", "Host": "China", "MVP": "Faker"}
]
df_history = pd.DataFrame(history_data)

# 2025 스위스 스테이지 최종 결산 데이터
swiss_2025_data = [
    {"Group": "3승 0패 (8강 진출)", "Teams": "Gen.G (LCK), JDG (LPL)"},
    {"Group": "3승 1패 (8강 진출)", "Teams": "T1 (LCK), KT Rolster (LCK), BLG (LPL)"},
    {"Group": "3승 2패 (8강 진출)", "Teams": "TES (LPL), G2 Esports (LEC), HLE (LCK)"},
    {"Group": "2승 3패 (탈락)", "Teams": "DK (LCK), WBG (LPL), FLY (LCS)"},
    {"Group": "1승 3패 (탈락)", "Teams": "FNC (LEC), TL (LCS), PSG (PCS)"},
    {"Group": "0승 3패 (탈락)", "Teams": "GAM (VCS), PNG (CBLOL)"}
]
df_swiss = pd.DataFrame(swiss_2025_data)

# 2025 8강 진출팀 선수 라인업 데이터
lineup_2025_data = [
    {"Team": "Gen.G", "Region": "LCK", "Top": "Kiin", "Jungle": "Canyon", "Mid": "Chovy", "ADC": "Peyz", "Support": "Lehends"},
    {"Team": "JDG", "Region": "LPL", "Top": "Flandre", "Jungle": "Kanavi", "Mid": "Yagao", "ADC": "Ruler", "Support": "MISSING"},
    {"Team": "T1", "Region": "LCK", "Top": "Zeus", "Jungle": "Oner", "Mid": "Faker", "ADC": "Gumayusi", "Support": "Keria"},
    {"Team": "KT Rolster", "Region": "LCK", "Top": "PerfecT", "Jungle": "Pyosik", "Mid": "Bdd", "ADC": "Deft", "Support": "BeryL"},
    {"Team": "BLG", "Region": "LPL", "Top": "Bin", "Jungle": "Xun", "Mid": "knight", "ADC": "Elk", "Support": "ON"},
    {"Team": "TES", "Region": "LPL", "Top": "369", "Jungle": "Tian", "Mid": "Creme", "ADC": "JackeyLove", "Support": "Meiko"},
    {"Team": "G2 Esports", "Region": "LEC", "Top": "BrokenBlade", "Jungle": "Yike", "Mid": "Caps", "ADC": "Hans Sama", "Support": "Mikyx"},
    {"Team": "HLE", "Region": "LCK", "Top": "Doran", "Jungle": "Peanut", "Mid": "Zeka", "ADC": "Viper", "Support": "Delight"}
]
df_lineup = pd.DataFrame(lineup_2025_data)

# 역대 결승전 구장 데이터 (최근 대회 중심)
FINALS_VENUES = {
    "2025 청두 동안호 스포츠공원 (T1 우승)": {"lat": 30.6558, "lon": 104.2881, "desc": "2025 Worlds Final"},
    "2024 런던 O2 아레나 (T1 우승)": {"lat": 51.5030, "lon": 0.0032, "desc": "2024 Worlds Final"},
    "2023 서울 고척스카이돔 (T1 우승)": {"lat": 37.4982, "lon": 126.8670, "desc": "2023 Worlds Final"},
    "2022 샌프란시스코 체이스센터 (DRX 우승)": {"lat": 37.7680, "lon": -122.3877, "desc": "2022 Worlds Final"},
    "2018 인천 문학경기장 (IG 우승)": {"lat": 37.4340, "lon": 126.6934, "desc": "2018 Worlds Final"}
}

# 3. 레이아웃 렌더링
st.title("🏆 LoL WORLDS COMPREHENSIVE DASHBOARD")
st.markdown("<p style='color: #a09b8c; font-size: 1.1rem;'>역대 월드 챔피언십 전체 결과 및 2025 스위스 스테이지 결산</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["👑 역대 전체 대회 결과 & MVP", "⚔️ 2025 스위스 스테이지 결산", "⭐ 레전드 선수 지표", "🏟️ 역대 결승전 구장", "👥 2025 8강 팀 라인업"])

with tab1:
    st.subheader("ALL-TIME WORLDS CHAMPIONS & FINALS MVP (2011-2025)")
    st.dataframe(
        df_history,
        column_config={
            "Year": st.column_config.NumberColumn("연도", format="%d"),
            "Winner": st.column_config.TextColumn("우승팀"),
            "Runner_up": st.column_config.TextColumn("준우승팀"),
            "Top_4": st.column_config.TextColumn("4강 진출팀", width="large"),
            "Top_8": st.column_config.TextColumn("8강 진출팀", width="large"),
            "Score": st.column_config.TextColumn("결승 스코어"),
            "MVP": st.column_config.TextColumn("결승전 MVP"),
            "Host": st.column_config.TextColumn("개최지")
        },
        use_container_width=True,
        hide_index=True,
        height=650
    )

with tab2:
    st.subheader("2025 SWISS STAGE FINAL STANDINGS")
    st.markdown("중국 청두에서 진행된 **2025 월드 챔피언십 스위스 스테이지** 최종 진출 및 탈락 결과입니다.")
    
    st.dataframe(
        df_swiss,
        column_config={
            "Group": st.column_config.TextColumn("승패 그룹 (최종 상태)", width="medium"),
            "Teams": st.column_config.TextColumn("해당 팀", width="large")
        },
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.subheader("HALL OF FAME: LEGENDARY PLAYERS")
    df_legends = pd.DataFrame([
        {"Player": "Faker (이상혁)", "Role": "Mid", "Titles": 6, "Win_Years": "2013, 2015, 2016, 2023, 2024, 2025", "MVP_Count": 3},
        {"Player": "Bengi (배성웅)", "Role": "Jungle", "Titles": 3, "Win_Years": "2013, 2015, 2016", "MVP_Count": 0},
        {"Player": "Ruler (박재혁)", "Role": "Bot", "Titles": 1, "Win_Years": "2017", "MVP_Count": 1},
        {"Player": "ShowMaker (허수)", "Role": "Mid", "Titles": 1, "Win_Years": "2020", "MVP_Count": 0},
        {"Player": "Zeus (최우제)", "Role": "Top", "Titles": 2, "Win_Years": "2023, 2024", "MVP_Count": 1}
    ])
    
    st.dataframe(
        df_legends,
        column_config={
            "Player": st.column_config.TextColumn("선수명"),
            "Role": st.column_config.TextColumn("포지션"),
            "Titles": st.column_config.ProgressColumn("우승 횟수", min_value=0, max_value=6, format="%d회"),
            "Win_Years": st.column_config.TextColumn("우승 연도"),
            "MVP_Count": st.column_config.NumberColumn("결승 MVP 횟수", format="%d회")
        },
        use_container_width=True,
        hide_index=True
    )

with tab4:
    st.subheader("HISTORICAL FINALS VENUES (RECENT)")
    venue = st.selectbox("탐색할 결승전 개최지를 선택하세요", list(FINALS_VENUES.keys()))
    info = FINALS_VENUES[venue]
    
    m = folium.Map(location=[info["lat"], info["lon"]], zoom_start=14, tiles="CartoDB dark_matter")
    folium.Marker(
        [info["lat"], info["lon"]], 
        popup=venue, 
        tooltip=info["desc"],
        icon=folium.Icon(color="orange", icon="trophy", prefix="fa")
    ).add_to(m)
    st_folium(m, width=1000, height=450)

with tab5:
    st.subheader("2025 WORLDS QUARTERFINALISTS LINEUPS")
    st.markdown("2025 월드 챔피언십 8강에 진출한 각 팀의 주전 선수 라인업입니다.")
    st.dataframe(
        df_lineup,
        column_config={
            "Team": st.column_config.TextColumn("팀명"),
            "Region": st.column_config.TextColumn("소속 지역"),
            "Top": st.column_config.TextColumn("탑"),
            "Jungle": st.column_config.TextColumn("정글"),
            "Mid": st.column_config.TextColumn("미드"),
            "ADC": st.column_config.TextColumn("원거리 딜러"),
            "Support": st.column_config.TextColumn("서포터")
        },
        use_container_width=True,
        hide_index=True
    )