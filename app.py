import os
import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------
# ページ設定
# --------------------------------
st.set_page_config(
    page_title="BayStars Stats 2026",
    layout="wide"
)

# --------------------------------
# ベイスターズ風CSS（高級感溢れる球団ネイビー＆ブルー）
# --------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #dff3ff;
    background-image: linear-gradient(to bottom, #dff3ff, #f7fbff);
    font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", sans-serif;
}
.main-title {
    font-size: 38px;
    font-weight: bold;
    color: #005bac;
    text-align: center;
    margin-bottom: 5px;
    letter-spacing: 2px;
}
.sub-title {
    font-size: 18px;
    text-align: center;
    color: #5c7080;
    margin-bottom: 30px;
    font-weight: 500;
}
.stats-card {
    background-color: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.05);
    margin-bottom: 30px;
}
.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #031c3c;
    border-left: 6px solid #005bac;
    padding-left: 12px;
    margin-bottom: 15px;
}

/* 👑 チーム比較用：2列グリッドのタイル */
.cl-king-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}
.cl-king-card {
    background: linear-gradient(135deg, #ffffff 0%, #f1f8ff 100%);
    border: 1px solid #cce4ff;
    border-radius: 12px;
    padding: 15px 10px;
    text-align: center;
    box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
}
.cl-king-title {
    font-size: 12px;
    color: #5c7080;
    font-weight: bold;
    margin-bottom: 4px;
}
.cl-king-team {
    font-size: 16px;
    color: #031c3c;
    font-weight: bold;
}
.cl-king-value {
    font-size: 18px;
    color: #005bac;
    font-weight: bold;
    margin-top: 2px;
}

/* 🧮 サイドバー設定 */
[data-testid="stSidebar"] {
    background-color: #031c3c !important;
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
    color: #ffffff !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #111111 !important;
}

/* 予測結果カード */
.sim-result-box-blacktext {
    background-color: #e6f2ff;
    border-left: 6px solid #005bac;
    padding: 15px;
    border-radius: 0 12px 12px 0;
    margin-top: 15px;
}
.sim-result-box-blacktext span, 
.sim-result-box-blacktext b, 
.sim-result-box-blacktext small {
    color: #111111 !important;
    font-weight: bold !important;
}

/* 👑 選手用の王様タイル */
.trophy-grid-compact-2col {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
}
.trophy-card-luxury-mini {
    background: linear-gradient(135deg, #fffef9 0%, #fffbdf 100%);
    border: 1px solid #ffe599;
    border-radius: 8px;
    padding: 8px 10px;
    text-align: center;
}
.trophy-title-luxury-mini {
    font-size: 11px;
    color: #b38600;
    font-weight: bold;
}
.trophy-name-luxury-mini {
    font-size: 15px;
    color: #031c3c;
    font-weight: bold;
}
.trophy-value-luxury-mini {
    font-size: 13px;
    color: #cc0000;
    font-weight: bold;
}

/* テーブル調整 */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* メインタブ（大きなタブ）のスタイルカスタム */
.stTabs [data-baseweb="tab"] {
    font-size: 16px !important;
    font-weight: bold !important;
    color: #005bac !important;
    padding: 10px 20px !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# タイトル
# --------------------------------
st.markdown('<div class="main-title">横浜DeNAベイスターズ 成績アプリ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026 SEASON STATS</div>', unsafe_allow_html=True)

# --------------------------------
# ファイル読み込み
# --------------------------------
batting_csv_path = "baystars_batting.csv"
pitching_csv_path = "baystars_pitching.csv"
cl_batting_csv_path = "central_league_stats.csv"       # 打撃比較用
cl_pitching_csv_path = "central_league_pitching.csv"   # 投手比較用

try:
    batting_df = pd.read_csv(batting_csv_path)
    pitching_df = pd.read_csv(pitching_csv_path)
    
    # 打撃比較
    if os.path.exists(cl_batting_csv_path):
        cl_bat_df = pd.read_csv(cl_batting_csv_path)
        if "出塁率" in cl_bat_df.columns and "長打率" in cl_bat_df.columns:
            cl_bat_df["チームOPS"] = cl_bat_df["出塁率"] + cl_bat_df["長打率"]
    else:
        cl_bat_df = pd.DataFrame()
        
    # 投手比較
    if os.path.exists(cl_pitching_csv_path):
        cl_pitch_df = pd.read_csv(cl_pitching_csv_path)
    else:
        cl_pitch_df = pd.DataFrame()
        
except Exception as e:
    st.error(f"⚠️ データの読み込み中にエラーが発生しました。")
    st.stop()


# --------------------------------
# 🧮 サイドバー予測
# --------------------------------
st.sidebar.markdown("<h2>🧮 フル出場シミュレーター</h2>", unsafe_allow_html=True)
sim_mode = st.sidebar.radio("設定する対象", ["打者を選ぶ", "投手を選ぶ"])

if sim_mode == "打者を選ぶ":
    selected_player = st.sidebar.selectbox("選手名", batting_df["選手名"].unique())
    p_data = batting_df[batting_df["選手名"] == selected_player].iloc[0]
    current_pa = p_data.get("打席", p_data.get("打席数", 0))
    if current_pa > 0:
        target_pa = st.sidebar.slider("目標の年間総打席数", 100, 650, 443, 10)
        scale = target_pa / current_pa
        pred_hr = round(p_data.get("本塁打", 0) * scale, 1)
        pred_rbi = round(p_data.get("打点", 0) * scale, 1)
        pred_hits = round(p_data.get("安打", 0) * scale, 1)
        st.sidebar.markdown(f"""
        <div class="sim-result-box-blacktext">
            <span>🦖 予測本塁打: <b>{pred_hr}</b> 本</span><br>
            <span>🔥 予測打点: <b>{pred_rbi}</b> 点</span><br>
            <span>⚔️ 予測安打: <b>{pred_hits}</b> 本</span>
        </div>
        """, unsafe_allow_html=True)
else:
    selected_player = st.sidebar.selectbox("選手名", pitching_df["選手名"].unique())
    p_data = pitching_df[pitching_df["選手名"] == selected_player].iloc[0]
    current_ip = p_data.get("投球回", 0)
    if current_ip > 0:
        target_ip = st.sidebar.slider("目標の年間総投球回", 10, 200, 143, 5)
        scale = target_ip / current_ip
        pred_so = round(p_data.get("奪三振", 0) * scale, 1)
        pred_w = round(p_data.get("勝利", 0) * scale, 1)
        st.sidebar.markdown(f"""
        <div class="sim-result-box-blacktext">
            <span>⛑️ 予測奪三振: <b>{pred_so}</b> 個</span><br>
            <span>👑 予測勝利数: <b>{pred_w}</b> 勝</span><br>
            <span>⭐ 防御率: <b>{p_data.get('防御率', 0)}</b></span>
        </div>
        """, unsafe_allow_html=True)


# --------------------------------
# 📊 Plotlyグラフ用共通関数
# --------------------------------
def create_custom_chart(df, y_column, label_text, is_ascending=False, x_column="選手名"):
    if y_column not in df.columns: return None
    df_sorted = df.sort_values(by=y_column, ascending=is_ascending)
    text_fmt = ".3f" if any(x in y_column for x in ["打率", "OPS", "出塁", "長打"]) else None
    fig = px.bar(df_sorted, x=x_column, y=y_column, text=y_column)
    if x_column == "チーム":
        colors = ["#005bac" if "ベイスターズ" in str(team) else "#a0b2c6" for team in df_sorted[x_column]]
        fig.update_traces(marker_color=colors)
    else:
        fig.update_traces(marker_color="#005bac")
    fig.update_layout(xaxis_title=None, yaxis_title=None, font=dict(color="#111111"), margin=dict(l=10, r=10, t=25, b=40), height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    if text_fmt: fig.update_traces(texttemplate='%{text:' + text_fmt + '}', textposition='outside', textfont=dict(color="#111111", weight="bold"))
    return fig


# --------------------------------
# 🏟️ セ・リーグ チームスタッツ比較（打撃・投手切り替えタブ化）
# --------------------------------
st.markdown('<div class="stats-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">セ・リーグ チームスタッツ比較 (CENTRAL LEAGUE)</div>', unsafe_allow_html=True)

# 球団カラーマッピングの定義
team_colors = {
    "横浜DeNAベイスターズ": "#005bac", 
    "阪神タイガース": "#ffc107", 
    "読売ジャイアンツ": "#ff6600", 
    "東京ヤクルトスワローズ": "#228b22", 
    "広島東洋カープ": "#ff0000", 
    "中日ドラゴンズ": "#002f6c"
}

# 大きなタブで打撃と投手を切り替え
main_tabs = st.tabs(["🏏 チーム打撃成績比較", "🛑 チーム投球成績比較"])

# --- 1. 打撃成績タブ ---
with main_tabs[0]:
    if not cl_bat_df.empty:
        st.dataframe(cl_bat_df, use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)

        cl_col_radar, cl_col_kings = st.columns([6, 4])
        with cl_col_radar:
            radar_features = ["チーム打率", "チームOPS", "本塁打", "得点", "打点", "安打", "四球", "三振", "併殺打", "出塁率"]
            actual_features = [f for f in radar_features if f in cl_bat_df.columns]
            radar_df_list = []
            for idx, row in cl_bat_df.iterrows():
                for f in actual_features:
                    max_v, min_v = cl_bat_df[f].max(), cl_bat_df[f].min()
                    if f in ["三振", "併殺打"]:
                        score = (max_v - row[f]) / (max_v - min_v) if max_v != min_v else 1.0
                    else:
                        score = row[f] / max_v if max_v != 0 else 0.0
                    radar_df_list.append({"チーム": row["チーム"], "項目": f, "スコア": score, "値": row[f]})
            
            fig_radar = px.line_polar(pd.DataFrame(radar_df_list), r="スコア", theta="項目", color="チーム", line_close=True)
            for trace in fig_radar.data:
                matched_color = team_colors.get(trace.name, "#a0b2c6")
                trace.line.color = matched_color
                if "ベイスターズ" in trace.name:
                    trace.line.width = 5; trace.fill = "toself"; trace.fillcolor = "rgba(0, 91, 172, 0.2)"
                else:
                    trace.line.width = 2
            
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 1.1])), legend_font_color="#111111", font=dict(color="#111111"), height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

        with cl_col_kings:
            st.markdown('<div style="font-weight: bold; color: #b38600; text-align: center; margin-bottom: 10px;">👑 セ・リーグ打撃部門トップ</div>', unsafe_allow_html=True)
            k_avg = cl_bat_df.sort_values(by="チーム打率", ascending=False).iloc[0]
            k_hr = cl_bat_df.sort_values(by="本塁打", ascending=False).iloc[0]
            k_ops = cl_bat_df.sort_values(by="チームOPS", ascending=False).iloc[0]
            k_runs = cl_bat_df.sort_values(by="得点", ascending=False).iloc[0]
            k_obp = cl_bat_df.sort_values(by="出塁率", ascending=False).iloc[0]
            k_sb = cl_bat_df.sort_values(by="盗塁", ascending=False).iloc[0]

            st.markdown(f"""
            <div class="cl-king-grid">
                <div class="cl-king-card"><div class="cl-king-title">打率王</div><div class="cl-king-team">{k_avg['チーム']}</div><div class="cl-king-value">{k_avg['チーム打率']:.3f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">本塁打王</div><div class="cl-king-team">{k_hr['チーム']}</div><div class="cl-king-value">{int(k_hr['本塁打'])}本</div></div>
                <div class="cl-king-card"><div class="cl-king-title">OPS王</div><div class="cl-king-team">{k_ops['チーム']}</div><div class="cl-king-value">{k_ops['チームOPS']:.3f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">得点王</div><div class="cl-king-team">{k_runs['チーム']}</div><div class="cl-king-value">{int(k_runs['得点'])}点</div></div>
                <div class="cl-king-card"><div class="cl-king-title">出塁率王</div><div class="cl-king-team">{k_obp['チーム']}</div><div class="cl-king-value">{k_obp['出塁率']:.3f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">盗塁王</div><div class="cl-king-team">{k_sb['チーム']}</div><div class="cl-king-value">{int(k_sb['盗塁'])}個</div></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 GitHubに `central_league_stats.csv` をアップロードしてください。")

# --- 2. 投手成績タブ（新規追加！） ---
with main_tabs[1]:
    if not cl_pitch_df.empty:
        st.dataframe(cl_pitch_df, use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)

        cl_pitch_radar, cl_pitch_kings = st.columns([6, 4])
        with cl_pitch_radar:
            # 投手力を測る10個の主要指標
            pitch_features = ["防御率", "失点", "自責点", "安打", "本塁打", "四球", "三振", "WHIP", "セーブ", "ホールド"]
            actual_pitch_features = [f for f in pitch_features if f in cl_pitch_df.columns]
            
            pitch_radar_list = []
            for idx, row in cl_pitch_df.iterrows():
                for f in actual_pitch_features:
                    max_v, min_v = cl_pitch_df[f].max(), cl_pitch_df[f].min()
                    
                    # 💡 低いほうが優秀な指標（防御率、失点、自責点、被安打、被本塁打、与四球、WHIP）は計算を反転！
                    if f in ["防御率", "失点", "自責点", "安打", "本塁打", "四球", "WHIP"]:
                        score = (max_v - row[f]) / (max_v - min_v) if max_v != min_v else 1.0
                        label_name = f"{f}(少)"
                    else:
                        # 高いほうが優秀な指標（三振、セーブ、ホールド）
                        score = row[f] / max_v if max_v != 0 else 0.0
                        label_name = f
                        
                    pitch_radar_list.append({"チーム": row["チーム"], "項目": label_name, "スコア": score, "値": row[f]})
            
            fig_pitch_radar = px.line_polar(pd.DataFrame(pitch_radar_list), r="スコア", theta="項目", color="チーム", line_close=True)
            for trace in fig_pitch_radar.data:
                matched_color = team_colors.get(trace.name, "#a0b2c6")
                trace.line.color = matched_color
                if "ベイスターズ" in trace.name:
                    trace.line.width = 5; trace.fill = "toself"; trace.fillcolor = "rgba(0, 91, 172, 0.2)"
                else:
                    trace.line.width = 2
            
            fig_pitch_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 1.1])), legend_font_color="#111111", font=dict(color="#111111"), height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pitch_radar, use_container_width=True, config={'displayModeBar': False})

        with cl_pitch_kings:
            st.markdown('<div style="font-weight: bold; color: #b38600; text-align: center; margin-bottom: 10px;">👑 セ・リーグ投手部門トップ</div>', unsafe_allow_html=True)
            
            # 各部門トップチームの計算（低いほうが良いもの、高いほうが良いものを考慮）
            kp_era = cl_pitch_df.sort_values(by="防御率", ascending=True).iloc[0]
            kp_so = cl_pitch_df.sort_values(by="三振", ascending=False).iloc[0]
            kp_whip = cl_pitch_df.sort_values(by="WHIP", ascending=True).iloc[0]
            kp_bb = cl_pitch_df.sort_values(by="四球", ascending=True).iloc[0]
            kp_sv = cl_pitch_df.sort_values(by="セーブ", ascending=False).iloc[0]
            kp_win = cl_pitch_df.sort_values(by="勝利", ascending=False).iloc[0]

            st.markdown(f"""
            <div class="cl-king-grid">
                <div class="cl-king-card"><div class="cl-king-title">最優秀防御率王</div><div class="cl-king-team">{kp_era['チーム']}</div><div class="cl-king-value">{kp_era['防御率']:.2f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">奪三振王</div><div class="cl-king-team">{kp_so['チーム']}</div><div class="cl-king-value">{int(kp_so['三振'])}個</div></div>
                <div class="cl-king-card"><div class="cl-king-title">鉄壁王 (WHIP)</div><div class="cl-king-team">{kp_whip['チーム']}</div><div class="cl-king-value">{kp_whip['WHIP']:.2f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">無四球王 (少四球)</div><div class="cl-king-team">{kp_bb['チーム']}</div><div class="cl-king-value">{int(kp_bb['四球'])}個</div></div>
                <div class="cl-king-card"><div class="cl-king-title">守護神王 (セーブ)</div><div class="cl-king-team">{kp_sv['チーム']}</div><div class="cl-king-value">{int(kp_sv['セーブ'])}S</div></div>
                <div class="cl-king-card"><div class="cl-king-title">最多勝王</div><div class="cl-king-team">{kp_win['チーム']}</div><div class="cl-king-value">{int(kp_win['勝利'])}勝</div></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 GitHubに `central_league_pitching.csv` をアップロードすると、ここに投手レーダーチャートが自動生成されます。")

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------
# 🏏 個人打撃・投手セクション
# --------------------------------
st.markdown('<div class="stats-card"><div class="section-title">個人打撃成績</div>', unsafe_allow_html=True)
col_search_bat, _ = st.columns([2, 1])
bat_search = col_search_bat.text_input("選手名検索", key="sb", label_visibility="collapsed", placeholder="選手名検索（例：牧）")
disp_b = batting_df[batting_df["選手名"].str.contains(bat_search, na=False)] if bat_search else batting_df
st.dataframe(disp_b, use_container_width=True, hide_index=True)
st.plotly_chart(create_custom_chart(batting_df, "打率", "打率"), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="stats-card"><div class="section-title">個人投手成績</div>', unsafe_allow_html=True)
st.dataframe(pitching_df, use_container_width=True, hide_index=True)
st.plotly_chart(create_custom_chart(pitching_df, "防御率", "防御率", True), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align: center; color: #5c7080; font-size: 12px; margin-top: 50px;">© YOKOHAMA DeNA BAYSTARS</div>', unsafe_allow_html=True)
