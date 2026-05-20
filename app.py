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
# ベイスターズ風CSS（図解通りの黄金比レイアウト）
# --------------------------------
st.markdown("""
<style>
/* 背景グラデーションと全体のフォント指定 */
.stApp {
    background-color: #dff3ff;
    background-image: linear-gradient(to bottom, #dff3ff, #f7fbff);
    font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", sans-serif;
}
/* タイトルエリア */
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
/* 白背景の大きなカード */
.stats-card {
    background-color: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.05);
    margin-bottom: 30px;
}
/* セクションタイトル */
.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #031c3c;
    border-left: 6px solid #005bac;
    padding-left: 12px;
    margin-bottom: 15px;
}

/* 👑 横2列のコンパクト高級カード */
.trophy-grid-compact-2col {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* 綺麗な横2列 */
    gap: 8px;
}
.trophy-card-luxury-mini {
    background: linear-gradient(135deg, #fffef9 0%, #fffbdf 100%);
    border: 1px solid #ffe599;
    border-radius: 8px;
    padding: 8px 10px;
    box-shadow: 0px 2px 5px rgba(212, 175, 55, 0.1);
    text-align: center;
}
.trophy-title-luxury-mini {
    font-size: 11px;
    color: #b38600;
    font-weight: bold;
    margin-bottom: 2px;
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

/* 予測結果カード（完全真っ黒文字固定） */
.sim-result-box-blacktext {
    background-color: #e6f2ff;
    border-left: 6px solid #005bac;
    padding: 15px;
    border-radius: 0 12px 12px 0;
    margin-top: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
}
.sim-result-box-blacktext span, 
.sim-result-box-blacktext b, 
.sim-result-box-blacktext small {
    color: #111111 !important;
    font-weight: bold !important;
}

/* テーブル調整 */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}
.regulation-text {
    color: #5c7080;
    font-size: 14px;
    font-weight: bold;
}
/* ポップアップ */
div[data-testid="stPopover"] button {
    background-color: #e8f4ff;
    color: #005bac;
    border: 1px solid #9ed4ff;
    border-radius: 8px;
    font-weight: bold;
}
/* タブ */
.stTabs [data-baseweb="tab"] {
    background-color: #f0f7ff !important;
    border: 1px solid #cce4ff !important;
    border-radius: 6px 6px 0px 0px !important;
    padding: 6px 12px !important;
    color: #005bac !important;
    font-weight: bold !important;
    font-size: 13px;
}
.stTabs [aria-selected="true"] {
    background-color: #005bac !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# タイトル
# --------------------------------
st.markdown('<div class="main-title">横浜DeNAベイスターズ 成績アプリ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">2026 SEASON STATS</div>', unsafe_allow_html=True)

# --------------------------------
# ファイル読み込み（ネット公開用のシンプルな書き方に修正）
# --------------------------------
batting_csv_path = "baystars_batting.csv"
pitching_csv_path = "baystars_pitching.csv"

try:
    batting_df = pd.read_csv(batting_csv_path)
    pitching_df = pd.read_csv(pitching_csv_path)
except FileNotFoundError as e:
    st.error(f"⚠️ CSVファイルが見つかりません。")
    st.stop()

# --------------------------------
# 🧮 サイドバー予測（完全真っ黒文字固定）
# --------------------------------
st.sidebar.markdown("<h2>🧮 フル出場シミュレーター</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:14px;'>選手の現在のペースのままフル出場した場合の妄想成績を計算！</p>", unsafe_allow_html=True)

sim_mode = st.sidebar.radio("設定する対象", ["打者を選ぶ", "投手を選ぶ"])

if sim_mode == "打者を選ぶ":
    selected_player = st.sidebar.selectbox("選手名", batting_df["選手名"].unique())
    p_data = batting_df[batting_df["選手名"] == selected_player].iloc[0]
    
    current_pa = p_data.get("打席", p_data.get("打席数", 0))
    if current_pa > 0:
        target_pa = st.sidebar.slider("目標の年間総打席数", min_value=100, max_value=650, value=443, step=10)
        scale = target_pa / current_pa
        
        st.sidebar.markdown(f"<h3>📈 {selected_player} 選手の予測</h3>", unsafe_allow_html=True)
        st.sidebar.markdown(f"<p>現在打席: <b>{int(current_pa)}</b> → 目標: <b>{target_pa}</b></p>", unsafe_allow_html=True)
        
        pred_hr = round(p_data.get("本塁打", 0) * scale, 1)
        pred_rbi = round(p_data.get("打点", 0) * scale, 1)
        pred_hits = round(p_data.get("安打", p_data.get("安打数", 0)) * scale, 1)
        
        st.sidebar.markdown(f"""
        <div class="sim-result-box-blacktext">
            <span>🦖 <b>予測本塁打:</b></span> <span style="font-size:22px;">{pred_hr}</span> <span>本</span><br>
            <span>🔥 <b>予測打点:</b></span> <span>{pred_rbi}</span> <span>点</span><br>
            <span>⚔️ <b>予測安打:</b></span> <span>{pred_hits}</span> <span>本</span><br>
            <small style="display:inline-block; margin-top:5px;">※現在のペースを維持した計算値です</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.warning("打席データが0です。")

else:
    selected_player = st.sidebar.selectbox("選手名", pitching_df["選手名"].unique())
    p_data = pitching_df[pitching_df["選手名"] == selected_player].iloc[0]
    
    current_ip = p_data.get("投球回", p_data.get("投球回数", 0))
    if current_ip > 0:
        target_ip = st.sidebar.slider("目標の年間総投球回", min_value=10, max_value=200, value=143, step=5)
        scale = target_ip / current_ip
        
        st.sidebar.markdown(f"<h3>📈 {selected_player} 選手の予測</h3>", unsafe_allow_html=True)
        st.sidebar.markdown(f"<p>現在回数: <b>{current_ip}</b> → 目標: <b>{target_ip}</b></p>", unsafe_allow_html=True)
        
        pred_so = round(p_data.get("奪三振", 0) * scale, 1)
        pred_w = round(p_data.get("勝利", p_data.get("勝", 0)) * scale, 1)
        
        st.sidebar.markdown(f"""
        <div class="sim-result-box-blacktext">
            <span>⛑️ <b>予測奪三振:</b></span> <span style="font-size:22px;">{pred_so}</span> <span>個</span><br>
            <span>👑 <b>予測勝利数:</b></span> <span>{pred_w}</span> <span>勝</span><br>
            <span>⭐ <b>現在の防御率:</b></span> <span>{p_data.get('防御率', 0)}</span><br>
            <small style="display:inline-block; margin-top:5px;">※現在の安定感を維持した場合の計算値です</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.warning("投球回データが0です。")


# --------------------------------
# 📊 Plotlyグラフ用共通関数
# --------------------------------
def create_custom_chart(df, y_column, label_text, is_ascending=False):
    if y_column not in df.columns:
        return None
    df_sorted = df.sort_values(by=y_column, ascending=is_ascending)
    # 打率や得点圏打率などは小数点以下3桁、それ以外は通常表示にするテキストフォーマット
    text_fmt = ".3f" if "打率" in y_column or y_column == "OPS" else None
    
    fig = px.bar(df_sorted, x="選手名", y=y_column, text=y_column, color_discrete_sequence=["#005bac"])
    fig.update_layout(
        xaxis_title=None, yaxis_title=f"数値 ({label_text})",
        font=dict(size=12, color="#111111", family="sans-serif"),
        margin=dict(l=10, r=10, t=25, b=40), height=280,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_xaxes(tickangle=45, tickfont=dict(size=11, weight="bold", color="#111111"))
    fig.update_yaxes(tickfont=dict(size=11, weight="bold", color="#111111"), gridcolor="#cce4ff")
    
    if text_fmt:
        fig.update_traces(texttemplate='%{text:' + text_fmt + '}', textposition='outside', textfont_size=10, textfont_color="#111111", textfont_weight="bold")
    else:
        fig.update_traces(textposition='outside', textfont_size=10, textfont_color="#111111", textfont_weight="bold")
    return fig


# --------------------------------
# 🏏 打撃成績セクション
# --------------------------------
st.markdown('<div class="stats-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">打撃成績</div>', unsafe_allow_html=True)

col_search_bat, col_note_bat = st.columns([2, 1])
with col_search_bat:
    batting_search = st.text_input("選手名で検索（例：牧）", key="search_bat", label_visibility="collapsed", placeholder="選手名で検索（例：牧）")
with col_note_bat:
    st.markdown('<div style="text-align: right; padding-top: 5px;" class="regulation-text">※規定打席以上</div>', unsafe_allow_html=True)

disp_batting = batting_df.copy()
if batting_search:
    disp_batting = disp_batting[disp_batting["選手名"].astype(str).str.contains(batting_search, case=False, na=False)]

# 上段：表をワイドに配置
with st.popover("📊 打撃指標の見方・目安"):
    st.markdown("""
    ### 📋 主要打撃指標の解説と基準
    * **打率 (AVG)**: ヒットを打つ確率。 [.250(平均) / .280(優秀) / .300(一流)]
    * **得点圏打率**: ランナーが二塁または三塁のチャンスの時の打率。
    * **OPS**: 出塁率 ＋ 長打率。得点貢献度を表す最重要指標。 [.700(平均) / .800(優秀) / .900〜(超一流)]
    * **ISO**: 長打率 － 打率。純粋な「長打力」を測る指標。 [.140(平均) / .200(優秀・長距離砲) / .250〜(超一流)]
    * **BABIP**: 本塁打・三振を除くグラウンドに飛んだ打球が安打になる確率。 [プロ平均は常時.300前後に収束。高すぎると運が良い、低すぎると不運]
    * **RC27**: その打者1人で1試合（27アウト）戦った場合の予測総得点。 [4.0〜4.5(平均) / 6.0(優秀) / 8.0〜(リーグ最強クラス)]
    """)
st.dataframe(disp_batting, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# 下段：グラフとチーム王を左右に配置
col_graph_bat, col_kings_bat = st.columns([55, 45])

with col_graph_bat:
    st.markdown('<div style="font-weight: bold; color: #031c3c; margin-bottom: 5px; font-size: 15px;">📊 打者ランキング</div>', unsafe_allow_html=True)
    
    # ★得点圏打率とISOを追加した、新ランキングタブ
    tab_labels = ["打率", "得点圏打率", "OPS", "ISO", "本塁打", "打点"]
    bat_rank_tabs = st.tabs(tab_labels)
    
    with bat_rank_tabs[0]:
        st.plotly_chart(create_custom_chart(batting_df, "打率", "打率", False), use_container_width=True, config={'displayModeBar': False})
    with bat_rank_tabs[1]:
        col_name = "得点圏打率" if "得点圏打率" in batting_df.columns else ("得点圏" if "得点圏" in batting_df.columns else None)
        if col_name:
            st.plotly_chart(create_custom_chart(batting_df, col_name, "得点圏", False), use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("CSVに『得点圏打率』の列がありません。")
    with bat_rank_tabs[2]:
        st.plotly_chart(create_custom_chart(batting_df, "OPS", "OPS", False), use_container_width=True, config={'displayModeBar': False})
    with bat_rank_tabs[3]:
        if "ISO" in batting_df.columns:
            st.plotly_chart(create_custom_chart(batting_df, "ISO", "ISO", False), use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("CSVに『ISO』の列がありません。")
    with bat_rank_tabs[4]:
        st.plotly_chart(create_custom_chart(batting_df, "本塁打", "HR", False), use_container_width=True, config={'displayModeBar': False})
    with bat_rank_tabs[5]:
        st.plotly_chart(create_custom_chart(batting_df, "打点", "打点", False), use_container_width=True, config={'displayModeBar': False})
        
with col_kings_bat:
    st.markdown('<div style="font-weight: bold; color: #b38600; margin-bottom: 5px; font-size: 15px;">👑 チーム打撃王</div>', unsafe_allow_html=True)
    if not batting_df.empty:
        top_avg = batting_df.sort_values(by="打率", ascending=False).iloc[0]
        top_ops = batting_df.sort_values(by="OPS", ascending=False).iloc[0]
        top_hr = batting_df.sort_values(by="本塁打", ascending=False).iloc[0]
        top_rbi = batting_df.sort_values(by="打点", ascending=False).iloc[0]
        
        sb_col = "盗塁" if "盗塁" in batting_df.columns else ("盗塁数" if "盗塁数" in batting_df.columns else None)
        top_sb_name = batting_df.sort_values(by=sb_col, ascending=False).iloc[0]['選手名'] if sb_col else "データなし"
        top_sb_val = f"{int(batting_df.sort_values(by=sb_col, ascending=False).iloc[0][sb_col])}個" if sb_col else ""
        
        st.markdown('<div class="trophy-grid-compact-2col">', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">首位打者</div><div class="trophy-name-luxury-mini">{top_avg["選手名"]}</div><div class="trophy-value-luxury-mini">{top_avg["打率"]:.3f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">最高OPS</div><div class="trophy-name-luxury-mini">{top_ops["選手名"]}</div><div class="trophy-value-luxury-mini">{top_ops["OPS"]:.3f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">本塁打王</div><div class="trophy-name-luxury-mini">{top_hr["選手名"]}</div><div class="trophy-value-luxury-mini">{int(top_hr["本塁打"])}本</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">打点王</div><div class="trophy-name-luxury-mini">{top_rbi["選手名"]}</div><div class="trophy-value-luxury-mini">{int(top_rbi["打点"])}点</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">盗塁王</div><div class="trophy-name-luxury-mini">{top_sb_name}</div><div class="trophy-value-luxury-mini">{top_sb_val}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------
# 🛑 投手成績セクション（バグ修正・大復活版）
# --------------------------------
st.markdown('<div class="stats-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">投手成績</div>', unsafe_allow_html=True)

col_search_pit, col_note_pit = st.columns([2, 1])
with col_search_pit:
    pitching_search = st.text_input("選手名で検索（例：東）", key="search_pit", label_visibility="collapsed", placeholder="選手名で検索（例：東）")
with col_note_pit:
    st.markdown('<div style="text-align: right; padding-top: 5px;" class="regulation-text">※規定投球回以上</div>', unsafe_allow_html=True)

disp_pitching = pitching_df.copy()
if pitching_search:
    disp_pitching = disp_pitching[disp_pitching["選手名"].astype(str).str.contains(pitching_search, case=False, na=False)]

# 上段：データ表をワイドに配置（復活確認用の最重要エリア）
with st.popover("📊 投手指標の見方・目安"):
    st.markdown("""
    ### 📋 主要投手指標の解説と基準
    * **防御率 (ERA)**: 9回を投げた場合の平均自責点。 [3.50〜4.00(平均) / 3.00(優秀) / 2.00台〜(エース級)]
    * **K/9 (奪三振率)**: 9回あたり平均で何個の三振を奪えるか。 [7.00(平均) / 8.50〜(優秀)]
    * **WHIP**: 1イニングあたりに出した走者（安打＋四球）の数。 [1.30(平均) / 1.20(良好) / 1.10未満(超エース・守護神級)]
    * **BB/9 (与四球率)**: 9回あたり平均で何個の四球を出すか。投手の純粋な制球力。 [3.30(平均) / 2.50(優秀) / 1.50未満(精密機械)]
    """)
st.dataframe(disp_pitching, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# 下段：グラフとチーム王
col_graph_pit, col_kings_pit = st.columns([55, 45])

with col_graph_pit:
    st.markdown('<div style="font-weight: bold; color: #031c3c; margin-bottom: 5px; font-size: 15px;">📊 投手ランキング</div>', unsafe_allow_html=True)
    pit_rank_tabs = st.tabs(["防御率", "K/9", "BB/9", "WHIP"])
    with pit_rank_tabs[0]:
        st.plotly_chart(create_custom_chart(pitching_df, "防御率", "防御率", True), use_container_width=True, config={'displayModeBar': False})
    with pit_rank_tabs[1]:
        st.plotly_chart(create_custom_chart(pitching_df, "K/9", "K/9", False), use_container_width=True, config={'displayModeBar': False})
    with pit_rank_tabs[2]:
        st.plotly_chart(create_custom_chart(pitching_df, "BB/9", "BB/9", True), use_container_width=True, config={'displayModeBar': False})
    with pit_rank_tabs[3]:
        st.plotly_chart(create_custom_chart(pitching_df, "WHIP", "WHIP", True), use_container_width=True, config={'displayModeBar': False})
        
with col_kings_pit:
    st.markdown('<div style="font-weight: bold; color: #b38600; margin-bottom: 5px; font-size: 15px;">👑 チーム投手王</div>', unsafe_allow_html=True)
    if not pitching_df.empty:
        top_era = pitching_df.sort_values(by="防御率", ascending=True).iloc[0]
        top_k9 = pitching_df.sort_values(by="K/9", ascending=False).iloc[0]
        top_whip = pitching_df.sort_values(by="WHIP", ascending=True).iloc[0]
        
        # カラム名の有無を安全に判定して文字列を作成（バグの原因を根本解決）
        w_col = "勝利" if "勝利" in pitching_df.columns else ("勝" if "勝" in pitching_df.columns else None)
        if w_col:
            top_w_row = pitching_df.sort_values(by=w_col, ascending=False).iloc[0]
            top_w_str = f'{top_w_row["選手名"]}<br>{int(top_w_row[w_col])}勝'
        else:
            top_w_str = "データなし"
            
        h_col = "ホールド" if "ホールド" in pitching_df.columns else ("HP" if "HP" in pitching_df.columns else None)
        if h_col:
            top_h_row = pitching_df.sort_values(by=h_col, ascending=False).iloc[0]
            top_h_str = f'{top_h_row["選手名"]}<br>{int(top_h_row[h_col])}HP'
        else:
            top_h_str = "データなし"
            
        g_col = "登板" if "登板" in pitching_df.columns else ("試合" if "試合" in pitching_df.columns else ("試合数" if "試合数" in pitching_df.columns else None))
        if g_col:
            top_g_row = pitching_df.sort_values(by=g_col, ascending=False).iloc[0]
            top_g_str = f'{top_g_row["選手名"]}<br>{int(top_g_row[g_col])}試合'
        else:
            top_g_str = "データなし"
        
        st.markdown('<div class="trophy-grid-compact-2col">', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">最優秀防御率</div><div class="trophy-name-luxury-mini">{top_era["選手名"]}</div><div class="trophy-value-luxury-mini">{top_era["防御率"]:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">勝利王</div><div class="trophy-value-luxury-mini">{top_w_str}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">奪三振王</div><div class="trophy-name-luxury-mini">{top_k9["選手名"]}</div><div class="trophy-value-luxury-mini">{top_k9["K/9"]:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">最高安定感</div><div class="trophy-name-luxury-mini">{top_whip["選手名"]}</div><div class="trophy-value-luxury-mini">{top_whip["WHIP"]:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">ホールド王</div><div class="trophy-value-luxury-mini">{top_h_str}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trophy-card-luxury-mini"><div class="trophy-title-luxury-mini">登板王</div><div class="trophy-value-luxury-mini">{top_g_str}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------
# フッター
# --------------------------------
st.markdown('<div style="text-align: center; color: #5c7080; font-size: 12px; margin-top: 50px; margin-bottom: 20px;">© YOKOHAMA DeNA BAYSTARS</div>', unsafe_allow_html=True)
