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
# ベイスターズ風CSS（高級感溢れるネイビー＆ブルー）
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

/* 🏆 個人タイトル用の豪華なゴールドミニタイル */
.trophy-grid-compact {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 10px;
    margin-bottom: 20px;
}
.trophy-card-luxury {
    background: linear-gradient(135deg, #fffef9 0%, #fffbdf 100%);
    border: 1px solid #ffe599;
    border-radius: 10px;
    padding: 12px 8px;
    text-align: center;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.03);
}
.trophy-title-luxury {
    font-size: 11px;
    color: #b38600;
    font-weight: bold;
}
.trophy-name-luxury {
    font-size: 16px;
    color: #031c3c;
    font-weight: bold;
}
.trophy-value-luxury {
    font-size: 13px;
    color: #cc0000;
    font-weight: bold;
}

/* 🧭 指標解説用のスタイル */
.desc-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 15px;
    margin-top: 20px;
}
.desc-card-blue {
    background-color: #f4f9ff;
    border: 1px solid #cce2ff;
    border-radius: 8px;
    padding: 15px;
}
.desc-card-yellow {
    background-color: #fffde6;
    border: 1px solid #efecb3;
    border-radius: 8px;
    padding: 15px;
}
.desc-title {
    font-size: 14px;
    font-weight: bold;
    color: #031c3c;
    margin-bottom: 6px;
    border-bottom: 1px solid rgba(0,0,0,0.1);
    padding-bottom: 3px;
}
.desc-text {
    font-size: 12px;
    color: #4a5568;
    line-height: 1.5;
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
.sim-result-box-blacktext span {
    color: #111111 !important;
    font-weight: bold !important;
}

/* テーブル調整 */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* タブのスタイルカスタム */
.stTabs [data-baseweb="tab"] {
    font-size: 15px !important;
    font-weight: bold !important;
    color: #005bac !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# タイトル
# --------------------------------
st.markdown('<div class="main-title">横浜DeNAベイスターズ 成績アプリ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026 SEASON STATS</div>', unsafe_allow_html=True)

# --------------------------------
# ファイル読み込み＆安全な指標計算
# --------------------------------
batting_csv_path = "baystars_batting.csv"
pitching_csv_path = "baystars_pitching.csv"
cl_batting_csv_path = "central_league_stats.csv"       # 打撃比較用
cl_pitching_csv_path = "central_league_pitching.csv"   # 投手比較用

try:
    batting_df = pd.read_csv(batting_csv_path)
    pitching_df = pd.read_csv(pitching_csv_path)
    
    # 💥 個人打撃：安全にアドバンスド指標を計算
    if "出塁率" in batting_df.columns and "長打率" in batting_df.columns:
        batting_df["OPS"] = batting_df["出塁率"] + batting_df["長打率"]
    elif "OPS" not in batting_df.columns:
        batting_df["OPS"] = 0.0

    if "長打率" in batting_df.columns and "打率" in batting_df.columns:
        batting_df["ISO"] = batting_df["長打率"] - batting_df["打率"]
    elif "ISO" not in batting_df.columns:
        batting_df["ISO"] = 0.0

    if "BABIP" not in batting_df.columns:
        if all(x in batting_df.columns for x in ["安打", "本塁打", "打数", "三振", "犠飛"]):
            batting_df["BABIP"] = (batting_df["安打"] - batting_df["本塁打"]) / (batting_df["打数"] - batting_df["三振"] - batting_df["本塁打"] + batting_df["犠飛"])
            batting_df["BABIP"] = batting_df["BABIP"].round(3).fillna(0.000)
        else:
            batting_df["BABIP"] = 0.000

    # 💥 個人投手：安全にアドバンスド指標を計算
    if "投球回" in pitching_df.columns and pitching_df["投球回"].max() > 0:
        if "奪三振" in pitching_df.columns and "K/9" not in pitching_df.columns:
            pitching_df["K/9"] = round((pitching_df["奪三振"] * 9) / pitching_df["投球回"], 2)
        if "四球" in pitching_df.columns and "BB/9" not in pitching_df.columns:
            pitching_df["BB/9"] = round((pitching_df["四球"] * 9) / pitching_df["投球回"], 2)
    if "奪三振" in pitching_df.columns and "四球" in pitching_df.columns and "K/BB" not in pitching_df.columns:
        pitching_df["K/BB"] = pitching_df.apply(lambda r: round(r["奪三振"] / r["四球"], 2) if r["四球"] > 0 else r["奪三振"], axis=1)

    # 💥 チーム比較データの読み込みとOPS補正
    cl_bat_df = pd.read_csv(cl_batting_csv_path) if os.path.exists(cl_batting_csv_path) else pd.DataFrame()
    if not cl_bat_df.empty and "出塁率" in cl_bat_df.columns and "長打率" in cl_bat_df.columns:
        cl_bat_df["チームOPS"] = cl_bat_df["出塁率"] + cl_bat_df["長打率"]
        
    cl_pitch_df = pd.read_csv(cl_pitching_csv_path) if os.path.exists(cl_pitching_csv_path) else pd.DataFrame()
        
except Exception as e:
    st.error(f"⚠️ データの読み込みまたは計算中にエラーが発生しました: {e}")
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
        st.sidebar.markdown(f"""
        <div class="sim-result-box-blacktext">
            <span>🦖 予測本塁打: <b>{round(p_data.get('本塁打', 0) * scale, 1)}</b> 本</span><br>
            <span>🔥 予測打点: <b>{round(p_data.get('打点', 0) * scale, 1)}</b> 点</span><br>
            <span>⚔️ 予測安打: <b>{round(p_data.get('安打', 0) * scale, 1)}</b> 本</span>
        </div>
        """, unsafe_allow_html=True)
else:
    selected_player = st.sidebar.selectbox("選手名", pitching_df["選手名"].unique())
    p_data = pitching_df[pitching_df["選手名"] == selected_player].iloc[0]
    current_ip = p_data.get("投球回", 0)
    if current_ip > 0:
        target_ip = st.sidebar.slider("目標の年間総投球回", 10, 200, 143, 5)
        scale = target_ip / current_ip
        st.sidebar.markdown(f"""
        <div class="sim-result-box-blacktext">
            <span>⛑️ 予測奪三振: <b>{round(p_data.get('奪三振', 0) * scale, 1)}</b> 個</span><br>
            <span>👑 予測勝利数: <b>{round(p_data.get('勝利', 0) * scale, 1)}</b> 勝</span><br>
            <span>⭐ 防御率: <b>{p_data.get('防御率', 0)}</b></span>
        </div>
        """, unsafe_allow_html=True)


# --------------------------------
# 📊 Plotlyグラフ用共通関数
# --------------------------------
def create_custom_chart(df, y_column, is_ascending=False):
    if y_column not in df.columns: return None
    if df[y_column].abs().sum() == 0: return None
    
    df_sorted = df.sort_values(by=y_column, ascending=is_ascending)
    text_fmt = ".3f" if any(x in y_column for x in ["打率", "OPS", "ISO", "BABIP", "得点圏"]) else None
    fig = px.bar(df_sorted, x="選手名", y=y_column, text=y_column)
    fig.update_traces(marker_color="#005bac")
    fig.update_layout(xaxis_title=None, yaxis_title=None, font=dict(color="#111111"), margin=dict(l=10, r=10, t=25, b=40), height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    if text_fmt: fig.update_traces(texttemplate='%{text:' + text_fmt + '}', textposition='outside', textfont=dict(color="#111111", weight="bold"))
    return fig


# --------------------------------
# 🏟️ セ・リーグ チームスタッツ比較（レーダー＆チーム王 完全復活！）
# --------------------------------
st.markdown('<div class="stats-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">セ・リーグ チームスタッツ比較 (CENTRAL LEAGUE)</div>', unsafe_allow_html=True)

team_colors = {
    "横浜DeNAベイスターズ": "#005bac", "阪神タイガース": "#ffc107", 
    "読売ジャイアンツ": "#ff6600", "東京ヤクルトスワローズ": "#228b22", 
    "広島東洋カープ": "#ff0000", "中日ドラゴンズ": "#002f6c"
}

main_tabs = st.tabs(["🏏 チーム打撃成績比較", "🛑 チーム投球成績比較"])

# --- 1. チーム打撃成績タブ ---
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
            
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 1.1])), legend_font_color="#111111", font=dict(color="#111111"), height=420, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

        with cl_col_kings:
            st.markdown('<div style="font-weight: bold; color: #b38600; text-align: center; margin-bottom: 10px;">👑 セ・リーグ打撃部門トップ</div>', unsafe_allow_html=True)
            k_avg = cl_bat_df.sort_values(by="チーム打率", ascending=False).iloc[0]
            k_hr = cl_bat_df.sort_values(by="本塁打", ascending=False).iloc[0]
            k_ops = cl_bat_df.sort_values(by="チームOPS", ascending=False).iloc[0] if "チームOPS" in cl_bat_df.columns else cl_bat_df.sort_values(by="チーム打率", ascending=False).iloc[0]
            k_runs = cl_bat_df.sort_values(by="得点", ascending=False).iloc[0]

            st.markdown(f"""
            <div class="cl-king-grid">
                <div class="cl-king-card"><div class="cl-king-title">打率王</div><div class="cl-king-team">{k_avg['チーム']}</div><div class="cl-king-value">{k_avg['チーム打率']:.3f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">本塁打王</div><div class="cl-king-team">{k_hr['チーム']}</div><div class="cl-king-value">{int(k_hr['本塁打'])}本</div></div>
                <div class="cl-king-card"><div class="cl-king-title">OPS王</div><div class="cl-king-team">{k_ops['チーム']}</div><div class="cl-king-value">{k_ops.get('チームOPS', 0.000):.3f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">得点王</div><div class="cl-king-team">{k_runs['チーム']}</div><div class="cl-king-value">{int(k_runs['得点'])}点</div></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 GitHubに `central_league_stats.csv` をアップロードしてください。")

# --- 2. チーム投手成績タブ ---
with main_tabs[1]:
    if not cl_pitch_df.empty:
        st.dataframe(cl_pitch_df, use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)

        cl_pitch_radar, cl_pitch_kings = st.columns([6, 4])
        with cl_pitch_radar:
            pitch_features = ["防御率", "失点", "自責点", "安打", "本塁打", "四球", "三振", "WHIP", "セーブ", "ホールド"]
            actual_pitch_features = [f for f in pitch_features if f in cl_pitch_df.columns]
            
            pitch_radar_list = []
            for idx, row in cl_pitch_df.iterrows():
                for f in actual_pitch_features:
                    max_v, min_v = cl_pitch_df[f].max(), cl_pitch_df[f].min()
                    if f in ["防御率", "失点", "自責点", "安打", "本塁打", "四球", "WHIP"]:
                        score = (max_v - row[f]) / (max_v - min_v) if max_v != min_v else 1.0
                        label_name = f"{f}(少)"
                    else:
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
            
            fig_pitch_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 1.1])), legend_font_color="#111111", font=dict(color="#111111"), height=420, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pitch_radar, use_container_width=True, config={'displayModeBar': False})

        with cl_pitch_kings:
            st.markdown('<div style="font-weight: bold; color: #b38600; text-align: center; margin-bottom: 10px;">👑 セ・リーグ投手部門トップ</div>', unsafe_allow_html=True)
            kp_era = cl_pitch_df.sort_values(by="防御率", ascending=True).iloc[0]
            kp_so = cl_pitch_df.sort_values(by="三振", ascending=False).iloc[0]
            kp_whip = cl_pitch_df.sort_values(by="WHIP", ascending=True).iloc[0]
            kp_win = cl_pitch_df.sort_values(by="勝利", ascending=False).iloc[0]

            st.markdown(f"""
            <div class="cl-king-grid">
                <div class="cl-king-card"><div class="cl-king-title">最優秀防御率王</div><div class="cl-king-team">{kp_era['チーム']}</div><div class="cl-king-value">{kp_era['防御率']:.2f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">奪三振王</div><div class="cl-king-team">{kp_so['チーム']}</div><div class="cl-king-value">{int(kp_so['三振'])}個</div></div>
                <div class="cl-king-card"><div class="cl-king-title">鉄壁王 (WHIP)</div><div class="cl-king-team">{kp_whip['チーム']}</div><div class="cl-king-value">{kp_whip['WHIP']:.2f}</div></div>
                <div class="cl-king-card"><div class="cl-king-title">最多勝王</div><div class="cl-king-team">{kp_win['チーム']}</div><div class="cl-king-value">{int(kp_win['勝利'])}勝</div></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 GitHubに `central_league_pitching.csv` をアップロードしてください。")

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------
# 🏏 個人打撃成績セクション（安全ガード付き完全タブ化）
# --------------------------------
st.markdown('<div class="stats-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">個人打撃成績 (INDIVIDUAL BATTING TABS)</div>', unsafe_allow_html=True)

# 👑 チーム内打撃王タイル
if not batting_df.empty:
    st.markdown(f"""
    <div class="trophy-grid-compact">
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チーム打率王</div><div class="trophy-name-luxury">{batting_df.sort_values(by="打率", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{batting_df.sort_values(by="打率", ascending=False).iloc[0]['打率']:.3f}</div></div>
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チーム本塁打王</div><div class="trophy-name-luxury">{batting_df.sort_values(by="本塁打", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{int(batting_df.sort_values(by="本塁打", ascending=False).iloc[0]['本塁打'])}本</div></div>
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チーム打点王</div><div class="trophy-name-luxury">{batting_df.sort_values(by="打点", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{int(batting_df.sort_values(by="打点", ascending=False).iloc[0]['打点'])}点</div></div>
    </div>
    """, unsafe_allow_html=True)

# 🎯 検索機能
col_search_bat, _ = st.columns([2, 1])
bat_search = col_search_bat.text_input("選手名で検索・絞り込み", key="bat_search_key", placeholder="選手名を入力...")
filtered_bat_df = batting_df[batting_df["選手名"].str.contains(bat_search, na=False)] if bat_search else batting_df

# 🔥 CSVに確実に存在する指標のみタブ化（ガード付き）
all_bat_metrics = ["打率", "OPS", "ISO", "BABIP", "得点圏打率", "本塁打", "打点", "出塁率"]
available_bat_metrics = [m for m in all_bat_metrics if m in filtered_bat_df.columns and filtered_bat_df[m].abs().sum() > 0]

if available_bat_metrics:
    bat_tabs = st.tabs([f"📊 {m}" for m in available_bat_metrics])
    for tab, metric in zip(bat_tabs, available_bat_metrics):
        with tab:
            sorted_disp_df = filtered_bat_df.sort_values(by=metric, ascending=False)
            st.dataframe(sorted_disp_df, use_container_width=True, hide_index=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f'<div style="font-size: 14px; font-weight: bold; color: #031c3c; margin-bottom: 5px;">🔥 チーム内 {metric} ランキング</div>', unsafe_allow_html=True)
            chart = create_custom_chart(batting_df, metric, is_ascending=False)
            if chart: st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
else:
    st.dataframe(filtered_bat_df, use_container_width=True, hide_index=True)

# 📄 打撃指標の解説と基準
st.markdown("""
<div class="desc-grid">
    <div class="desc-card-blue">
        <div class="desc-title">📈 OPS（オプス）</div>
        <div class="desc-text">
            <b>【計算式】</b> 出塁率 ＋ 長打率<br>
            <b>【説明】</b> 打者が「塁に出る能力」と「長打を放つ能力」を足した、得点効率に直結する現代野球の最強指標。<br>
            <b>【評価基準】</b> <b>.800</b>を超えれば超一流（クリーンアップ級）、<b>.900</b>を超えるとMVP級の怪物打者と評価されます。
        </div>
    </div>
    <div class="desc-card-blue">
        <div class="desc-title">🚀 ISO（アイエスオー）</div>
        <div class="desc-text">
            <b>【計算式】</b> 長打率 － 打率<br>
            <b>【説明】</b> 単打の影響を完全に排除し、その打者が「純粋に長打（二塁打以上）を打つ力」だけを測る指標。<br>
            <b>【評価基準】</b> <b>.200</b>を超えると「本物のスラッガー（大砲）」とされ、長打力の確かな証となります。
        </div>
    </div>
    <div class="desc-card-blue">
        <div class="desc-title">🍀 BABIP（バビップ）</div>
        <div class="desc-text">
            <b>【計算式】</b> (安打 - 本塁打) / (打数 - 三振 - 本塁打 + 犠飛)<br>
            <b>【説明】</b> 本塁打と三振を除く、「フィールド内に飛んだ打球が安打になった割合」。投手の運や、打者の打球速度に影響されます。<br>
            <b>【評価基準】</b> プロ野球平均はほぼ <b>.300</b> に収束します。極端に高い選手は「現在幸運（ヒットが出やすい）」、低い選手は「運が悪い」と判断できます。
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------
# 🛑 個人投手成績セクション（6タブ完全実装）
# --------------------------------
st.markdown('<div class="stats-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">個人投手成績 (INDIVIDUAL PITCHING TABS)</div>', unsafe_allow_html=True)

# 👑 チーム内投手王タイル
if not pitching_df.empty:
    st.markdown(f"""
    <div class="trophy-grid-compact">
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チーム最優秀防御率</div><div class="trophy-name-luxury">{pitching_df.sort_values(by="防御率", ascending=True).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{pitching_df.sort_values(by="防御率", ascending=True).iloc[0]['防御率']:.2f}</div></div>
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チーム最多勝</div><div class="trophy-name-luxury">{pitching_df.sort_values(by="勝利", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{int(pitching_df.sort_values(by="勝利", ascending=False).iloc[0]['勝利'])}勝</div></div>
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チームWHIP王</div><div class="trophy-name-luxury">{pitching_df.sort_values(by="WHIP", ascending=True).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{pitching_df.sort_values(by="WHIP", ascending=True).iloc[0]['WHIP']:.2f}</div></div>
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チームK/BB王</div><div class="trophy-name-luxury">{pitching_df.sort_values(by="K/BB", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{pitching_df.sort_values(by="K/BB", ascending=False).iloc[0]['K/BB']:.2f}</div></div>
    </div>
    """, unsafe_allow_html=True)

# 🎯 検索機能
col_search_pitch, _ = st.columns([2, 1])
pitch_search = col_search_pitch.text_input("選手名で検索・絞り込み", key="pitch_search_key", placeholder="選手名を入力...")
filtered_pitch_df = pitching_df[pitching_df["選手名"].str.contains(pitch_search, na=False)] if pitch_search else pitching_df

# 🔥 6つの投手指標タブ
all_pitch_metrics = ["防御率", "勝利", "WHIP", "K/9", "BB/9", "K/BB"]
available_pitch_metrics = [m for m in all_pitch_metrics if m in filtered_pitch_df.columns]

if available_pitch_metrics:
    pitch_tabs = st.tabs([f"📊 {m}" for m in available_pitch_metrics])
    for tab, metric in zip(pitch_tabs, available_pitch_metrics):
        with tab:
            low_is_good = metric in ["防御率", "WHIP", "BB/9"]
            sorted_disp_df = filtered_pitch_df.sort_values(by=metric, ascending=low_is_good)
            st.dataframe(sorted_disp_df, use_container_width=True, hide_index=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f'<div style="font-size: 14px; font-weight: bold; color: #031c3c; margin-bottom: 5px;">👑 チーム内 {metric} ランキング</div>', unsafe_allow_html=True)
            chart = create_custom_chart(pitching_df, metric, is_ascending=low_is_good)
            if chart: st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
else:
    st.dataframe(filtered_pitch_df, use_container_width=True, hide_index=True)

# 📄 投手指標の解説と基準
st.markdown("""
<div class="desc-grid">
    <div class="desc-card-yellow">
        <div class="desc-title">🛡️ WHIP（ウィップ）</div>
        <div class="desc-text">
            <b>【計算式】</b> (安打 ＋ 四球) ÷ 投球回<br>
            <b>【説明】</b> 1イニングあたりに平均して何人のランナーを出したかを示す、投手の安定感を表す指標。<br>
            <b>【評価基準】</b> <b>1.20</b>未満ならエース級（優秀）、<b>1.00</b>を切ると球界を代表する絶対的エースの証です。
        </div>
    </div>
    <div class="desc-card-yellow">
        <div class="desc-title">⛑️ K/9（奪三振率）</div>
        <div class="desc-text">
            <b>【計算式】</b> (奪三振 × 9) ÷ 投球回<br>
            <b>【説明】</b> 1試合（9イニング）を投げた場合に、平均して何個の三振を奪えるかを示す指標。<br>
            <b>【評価基準】</b> 先発なら<b>7.50</b>が標準。<b>9.00</b>（毎イニング1三振ペース）を超えると強力なドクターKと評されます。
        </div>
    </div>
    <div class="desc-card-yellow">
        <div class="desc-title">📉 BB/9（与四球率）</div>
        <div class="desc-text">
            <b>【計算式】</b> (四球 × 9) ÷ 投球回<br>
            <b>【説明】</b> 1試合（9イニング）あたり、平均してどれだけのフォアボールを出すかという純粋なコントロールの指標。<br>
            <b>【評価基準】</b> <b>2.00</b>未満なら「抜群の制球力（精密機械）」、4.00を超えると自滅しやすい傾向と判断されます。
        </div>
    </div>
    <div class="desc-card-yellow">
        <div class="desc-title">🎯 K/BB（ケーバイビービー）</div>
        <div class="desc-text">
            <b>【計算式】</b> 奪三振 ÷ 四球<br>
            <b>【説明】</b> 1つのフォアボールを出すまでに、いくつ三振を奪ったか。投手の総合的な統率力を示す最重要指標。<br>
            <b>【評価基準】</b> <b>3.50</b>を超えると一流、<b>5.00</b>を超えると「神がかった制球と球威を持つ絶対的エース」となります。
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# フッター
st.markdown('<div style="text-align: center; color: #5c7080; font-size: 12px; margin-top: 50px; padding-bottom: 20px;">© YOKOHAMA DeNA BAYSTARS</div>', unsafe_allow_html=True)
