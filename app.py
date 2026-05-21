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
# ベイスターズ風CSS（高級感溢れるデザイン）
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

/* 👑 タイル用 */
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
}

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

/* 🧭 指標解説 */
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

[data-testid="stSidebar"] { background-color: #031c3c !important; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #ffffff !important; }
[data-testid="stSidebar"] div[data-baseweb="select"] span { color: #111111 !important; }

.sim-result-box-blacktext {
    background-color: #e6f2ff;
    border-left: 6px solid #005bac;
    padding: 15px;
    border-radius: 0 12px 12px 0;
    margin-top: 15px;
}
.sim-result-box-blacktext span { color: #111111 !important; font-weight: bold !important; }

[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
.stTabs [data-baseweb="tab"] { font-size: 15px !important; font-weight: bold !important; color: #005bac !important; }
</style>
""", unsafe_allow_html=True)

# --------------------------------
# タイトル
# --------------------------------
st.markdown('<div class="main-title">横浜DeNAベイスターズ 成績アプリ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026 SEASON STATS</div>', unsafe_allow_html=True)

# --------------------------------
# ファイル読み込み＆マニアック指標の自動計算
# --------------------------------
batting_csv_path = "baystars_batting.csv"
pitching_csv_path = "baystars_pitching.csv"
cl_batting_csv_path = "central_league_stats.csv"
cl_pitching_csv_path = "central_league_pitching.csv"

try:
    batting_df = pd.read_csv(batting_csv_path)
    pitching_df = pd.read_csv(pitching_csv_path)
    
    # 💥 個人打撃のアドバンスド指標計算
    if "出塁率" in batting_df.columns and "長打率" in batting_df.columns:
        batting_df["OPS"] = batting_df["出塁率"] + batting_df["長打率"]
    if "長打率" in batting_df.columns and "打率" in batting_df.columns:
        batting_df["ISO"] = batting_df["長打率"] - batting_df["打率"]
    if all(x in batting_df.columns for x in ["安打", "本塁打", "打数", "三振", "犠飛"]):
        # 簡易BABIP計算式: (安打 - 本塁打) / (打数 - 三振 - 本塁打 + 犠飛)
        batting_df["BABIP"] = (batting_df["安打"] - batting_df["本塁打"]) / (batting_df["打数"] - batting_df["三振"] - batting_df["本塁打"] + batting_df["犠飛"])
        batting_df["BABIP"] = batting_df["BABIP"].round(3).fillna(0.000)

    # 💥 個人投手のアドバンスド指標計算
    if "投球回" in pitching_df.columns and pitching_df["投球回"].max() > 0:
        if "奪三振" in pitching_df.columns:
            pitching_df["K/9"] = round((pitching_df["奪三振"] * 9) / pitching_df["投球回"], 2)
        if "四球" in pitching_df.columns:
            pitching_df["BB/9"] = round((pitching_df["四球"] * 9) / pitching_df["投球回"], 2)
    if "奪三振" in pitching_df.columns and "四球" in pitching_df.columns:
        pitching_df["K/BB"] = pitching_df.apply(lambda r: round(r["奪三振"] / r["四球"], 2) if r["四球"] > 0 else r["奪三振"], axis=1)

    # チーム比較データ
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
# 📊 Plotly用共通関数
# --------------------------------
def create_custom_chart(df, y_column, is_ascending=False):
    if y_column not in df.columns: return None
    df_sorted = df.sort_values(by=y_column, ascending=is_ascending)
    text_fmt = ".3f" if any(x in y_column for x in ["打率", "OPS", "出塁", "長打", "ISO", "BABIP", "得点圏"]) else None
    fig = px.bar(df_sorted, x="選手名", y=y_column, text=y_column)
    fig.update_traces(marker_color="#005bac")
    fig.update_layout(xaxis_title=None, yaxis_title=None, font=dict(color="#111111"), margin=dict(l=10, r=10, t=25, b=40), height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    if text_fmt: fig.update_traces(texttemplate='%{text:' + text_fmt + '}', textposition='outside', textfont=dict(color="#111111", weight="bold"))
    return fig


# --------------------------------
# 🏟️ チーム成績セクション（省略なし）
# --------------------------------
st.markdown('<div class="stats-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">セ・リーグ チームスタッツ比較 (CENTRAL LEAGUE)</div>', unsafe_allow_html=True)
team_colors = {"横浜DeNAベイスターズ": "#005bac", "阪神タイガース": "#ffc107", "読売ジャイアンツ": "#ff6600", "東京ヤクルトスワローズ": "#228b22", "広島東洋カープ": "#ff0000", "中日ドラゴンズ": "#002f6c"}
t_tabs = st.tabs(["🏏 チーム打撃成績比較", "🛑 チーム投球成績比較"])

with t_tabs[0]:
    if not cl_bat_df.empty:
        st.dataframe(cl_bat_df, use_container_width=True, hide_index=True)
with t_tabs[1]:
    if not cl_pitch_df.empty:
        st.dataframe(cl_pitch_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------
# 🏏 個人打撃成績セクション（完全タブ化機能＋マニアック解説付き）
# --------------------------------
st.markdown('<div class="stats-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">個人打撃成績 (INDIVIDUAL BATTING TABS)</div>', unsafe_allow_html=True)

# 👑 チーム内打撃王タイル
if not batting_df.empty:
    st.markdown(f"""
    <div class="trophy-grid-compact">
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チーム打率王</div><div class="trophy-name-luxury">{batting_df.sort_values(by="打率", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{batting_df.sort_values(by="打率", ascending=False).iloc[0]['打率']:.3f}</div></div>
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チーム本塁打王</div><div class="trophy-name-luxury">{batting_df.sort_values(by="本塁打", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{int(batting_df.sort_values(by="本塁打", ascending=False).iloc[0]['本塁打'])}本</div></div>
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チームOPS王</div><div class="trophy-name-luxury">{batting_df.sort_values(by="OPS", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{batting_df.sort_values(by="OPS", ascending=False).iloc[0]['OPS']:.3f}</div></div>
        <div class="trophy-card-luxury"><div class="trophy-title-luxury">チームISO王</div><div class="trophy-name-luxury">{batting_df.sort_values(by="ISO", ascending=False).iloc[0]['選手名']}</div><div class="trophy-value-luxury">{batting_df.sort_values(by="ISO", ascending=False).iloc[0]['ISO']:.3f}</div></div>
    </div>
    """, unsafe_allow_html=True)

# 🎯 検索機能
col_search_bat, _ = st.columns([2, 1])
bat_search = col_search_bat.text_input("選手名で検索・絞り込み", key="bat_search_key", placeholder="選手名を入力...")
filtered_bat_df = batting_df[batting_df["選手名"].str.contains(bat_search, na=False)] if bat_search else batting_df

# 🔥 8つの指標タブ
bat_metrics = ["打率", "OPS", "ISO", "BABIP", "得点圏打率", "本塁打", "打点", "出塁率"]
bat_tabs = st.tabs([f"📊 {m}" for m in bat_metrics])

for tab, metric in zip(bat_tabs, bat_metrics):
    with tab:
        # 表の表示（選択された指標でソート）
        sorted_disp_df = filtered_bat_df.sort_values(by=metric, ascending=False)
        st.dataframe(sorted_disp_df, use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)
        # グラフの表示
        st.markdown(f'<div style="font-size: 14px; font-weight: bold; color: #031c3c; margin-bottom: 5px;">🔥 チーム内 {metric} ランキング</div>', unsafe_allow_html=True)
        chart = create_custom_chart(batting_df, metric, is_ascending=False)
        if chart: st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

# 📄 打撃指標の解説と基準
st.markdown("""
<div class="desc-grid">
    <div class="desc-card-blue">
        <div class="desc-title">📈 OPS（オプス）</div>
        <div class="desc-text">
            <b>【計算式】</b> 出塁率 ＋ 長打率<br>
            <b>【説明】</b> 打者が「塁に出る能力」と「長打を放つ能力」を足した、得点効率に直結する現代野球の最強指標。<br>
            <b>【評価基準】</b> <b>.800</b>を超えれば超一流（クリーンアップ級）、<b>.900</b>を超えるとMVP級（リーグ支配者）の怪物打者と評価されます。
        </div>
    </div>
    <div class="desc-card-blue">
        <div class="desc-title">🚀 ISO（アイエスオー）</div>
        <div class="desc-text">
            <b>【計算式】</b> 長打率 － 打率<br>
            <b>【説明】</b> 単打（ヒット）による影響を完全に排除し、その打者が「純粋に長打（二塁打以上）を打つ力」だけを測る指標。<br>
            <b>【評価基準】</b> <b>.200</b>を超えると「本物のスラッガー（大砲）」とされ、.250超えはリーグ最高峰の長打力を持つ証です。
        </div>
    </div>
    <div class="desc-card-blue">
        <div class="desc-title">🍀 BABIP（バビップ）</div>
        <div class="desc-text">
            <b>【計算式】</b> (安打 - 本塁打) / (打数 - 三振 - 本塁打 + 犠飛)<br>
            <b>【説明】</b> 本塁打と三振を除く、「フィールド内に飛んだ打球が安打になった割合」。投手の運や、打者の俊足・打球速度に影響されます。<br>
            <b>【評価基準】</b> プロ野球平均はほぼ <b>.300</b> に収束します。これが.360など極端に高い選手は「現在幸運（ヒットが出やすい状態）」、逆に.240など低い選手は「運が悪いか、打球の質が極端に悪い」と判断できます。
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------
# 🛑 個人投手成績セクション（完全タブ化機能＋マニアック解説付き）
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

# 🔥 6つの指標タブ
pitch_metrics = ["防御率", "勝利", "WHIP", "K/9", "BB/9", "K/BB"]
pitch_tabs = st.tabs([f"📊 {m}" for m in pitch_metrics])

for tab, metric in zip(pitch_tabs, pitch_metrics):
    with tab:
        # 防御率, WHIP, BB/9 は低いほうが優秀なので昇順ソート（ascending=True）
        low_is_good = metric in ["防御率", "WHIP", "BB/9"]
        sorted_disp_df = filtered_pitch_df.sort_values(by=metric, ascending=low_is_good)
        st.dataframe(sorted_disp_df, use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # グラフの表示
        st.markdown(f'<div style="font-size: 14px; font-weight: bold; color: #031c3c; margin-bottom: 5px;">👑 チーム内 {metric} ランキング</div>', unsafe_allow_html=True)
        chart = create_custom_chart(pitching_df, metric, is_ascending=low_is_good)
        if chart: st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

# 📄 投手指標の解説と基準
st.markdown("""
<div class="desc-grid">
    <div class="desc-card-yellow">
        <div class="desc-title">🛡️ WHIP（ウィップ）</div>
        <div class="desc-text">
            <b>【計算式】</b> (安打 ＋ 四球) ÷ 投球回<br>
            <b>【説明】</b> 1イニングあたりに平均して何人のランナーを出したかを示す、投手の安定感を表す指標（死球やエラーは含まない）。<br>
            <b>【評価基準】</b> <b>1.20</b>未満ならエース級（優秀）、<b>1.00</b>を切ると球界を代表する圧倒的守護神や超一流先発の証です。
        </div>
    </div>
    <div class="desc-card-yellow">
        <div class="desc-title">⛑️ K/9（奪三振率）</div>
        <div class="desc-text">
            <b>【計算式】</b> (奪三振 × 9) ÷ 投球回<br>
            <b>【説明】</b> 1試合（9イニング）を投げた場合に、平均して何個の三振を奪えるかを示す、投手のパワーやねじ伏せる力を示す指標。<br>
            <b>【評価基準】</b> <b>7.50</b>が先発の標準。<b>9.00</b>（毎イニング1三振ペース）を超えると三振の山を築く強力なドクターKと評されます。
        </div>
    </div>
    <div class="desc-card-yellow">
        <div class="desc-title">📉 BB/9（与四球率）</div>
        <div class="desc-text">
            <b>【計算式】</b> (四球 × 9) ÷ 投球回<br>
            <b>【説明】</b> 1試合（9イニング）あたり、平均してどれだけのフォアボールを出すかという、純粋なコントロールの指標。<br>
            <b>【評価基準】</b> <b>2.00</b>未満なら「抜群の制球力（精密機械）」、逆に4.00を超えると四球から自滅しやすい荒れ球投手と判断されます。
        </div>
    </div>
    <div class="desc-card-yellow">
        <div class="desc-title">🎯 K/BB（ケーバイビービー）</div>
        <div class="desc-text">
            <b>【計算式】</b> 奪三振 ÷ 四球<br>
            <b>【説明】</b> 1つのフォアボールを出すまでに、いくつ三振を奪ったか。投手の総合的な支配力と大人のピッチングを最も正確に表す指標。<br>
            <b>【評価基準】</b> <b>3.50</b>を超えると一流、<b>5.00</b>を超えると「神がかった制球と球威を持つ絶対的なエース」となります。
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# フッター
st.markdown('<div style="text-align: center; color: #5c7080; font-size: 12px; margin-top: 50px; padding-bottom: 20px;">© YOKOHAMA DeNA BAYSTARS</div>', unsafe_allow_html=True)
