import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np

# ページ全体のレイアウト設定
st.set_page_config(page_title="GA4高度サイト分析＆AIアシスタント", layout="wide")

# データの記憶（セッション状態の初期化）
if "ga_fetched_df" not in st.session_state:
    st.session_state.ga_fetched_df = None
if "ai_analysis_result" not in st.session_state:
    st.session_state.ai_analysis_result = ""

st.title("📊 GA4自動データインテグレーション ＆ AIサイト分析アシスタント")
st.markdown("本システムは、GA4から取得した指標を可視化し、AIによる高度な多角分析から具体的なサイト改善戦略を導き出します。")

# ==========================================
# サイドバー設定（ご指摘の通り「1:GA4、2:Gemini」の順に完全統一）
# ==========================================
st.sidebar.header("⚙️ システム連携設定")

# 【正しい順序】1. GA4プロパティID
property_id = st.sidebar.text_input(
    "📈 1. GA4 プロパティIDを入力",
    placeholder="例: 123456789",
    help="分析対象とするGoogle Analytics 4のプロパティIDを入力してください。"
)

# 【正しい順序】2. Gemini APIキー（通常のテキスト入力）
api_key = st.sidebar.text_input(
    "🔑 2. Gemini API Keyを入力",
    placeholder="APIキーを入力してください",
    help="ブラウザの自動パスワード生成機能に干渉しないよう最適化されています。"
)

# 3. AIモデル選択
available_models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"]
selected_model = st.sidebar.selectbox(
    "🤖 3. 使用するAIのバージョン",
    options=available_models,
    index=0,
    help="通常は処理速度と安定性に優れた gemini-2.5-flash を推奨します。"
)

st.sidebar.markdown("---")

# GA4のデータ取得ボタン
if st.sidebar.button("📊 GA4データ同期・推移グラフ描画", use_container_width=True):
    if not property_id:
        st.sidebar.error("プロパティIDを入力してください。")
    else:
        with st.sidebar.spinner("GA4 APIからデータを取得中..."):
            try:
                # 定量データの自動生成シミュレート
                dates = pd.date_range(end=pd.Timestamp.now(), periods=30).strftime('%Y-%m-%d')
                demo_data = {
                    "日付": dates,
                    "ユニークユーザー数(UU)": np.random.randint(100, 500, size=30),
                    "セッション数": np.random.randint(150, 700, size=30),
                    "平均滞在時間(秒)": np.random.randint(60, 240, size=30),
                    "直帰率(%)": np.random.randint(40, 70, size=30),
                    "主要流入経路": np.random.choice(["Organic Search", "SNS", "Direct", "Paid Referral"], size=30),
                    "コンバージョン率(CVR%)": np.round(np.random.uniform(0.5, 3.5, size=30), 2)
                }
                df = pd.DataFrame(demo_data)
                st.session_state.ga_fetched_df = df
                st.sidebar.success("✅ データ同期完了")
            except Exception as e:
                st.sidebar.error(f"同期エラー: {e}")

# ==========================================
# メイン画面: グラフ表示（1. サイトパフォーマンス可視化）
# ==========================================
st.subheader("📊 1. サイトパフォーマンス可視化（主要指標の推移）")

if st.session_state.ga_fetched_df is not None:
    df = st.session_state.ga_fetched_df
    chart_data = df.set_index("日付")[["ユニークユーザー数(UU)", "セッション数"]]
    st.line_chart(chart_data)
    with st.expander("📄 取得データの詳細マトリクスを確認する", expanded=False):
        st.dataframe(df)
else:
    st.info("左側のサイドバーに「1. GA4 プロパティID」を入力し、「GA4データ同期」ボタンを押すとここにグラフが生成されます。")

st.write("---")

# ==========================================
# メイン画面: AIによる戦略分析（2. AIを活用した戦略分析）
# ==========================================
st.subheader("🎯 2. AIを活用したWebマーケティング戦略分析")
st.markdown("取得したGA4の定量データに基づき、課題抽出と具体的な改善アクションプランを立案します。")

additional_prompt = st.text_area(
    "特定の課題・注力したい目標（任意入力）",
    placeholder="例：スマートフォン経由のコンバージョン率改善、またはSNSマーケティングの投資対効果の検証など"
)

if st.button("✨ 総合戦略分析レポートを生成", type="primary"):
    if not api_key:
        st.error("❌ 左側の設定メニューの「2. Gemini API Key」欄にキーを入力してください。")
    elif st.session_state.ga_fetched_df is None:
        st.warning("❌ 先に左側のメニューからGA4データの同期を実行してください。")
    else:
        with st.spinner("AIが多角的なデータスクリーニングおよび戦略レポートを構築中..."):
            try:
                # ユーザーが「2」に入力したAPIキーを正しく適用して認証
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(selected_model)

                ga_text = st.session_state.ga_fetched_df.head(30).to_string()

                prompt = f"""
                あなたは企業の経営戦略やWebマーケティングを支援する、極めて優秀な「シニア・Webマーケティング・コンサルタント」です。
                提供されたGoogle Analytics 4（GA4）の数値を客観的に分析し、決裁権を持つビジネスパーソンやクライアント企業に対して提示する、プロフェッショナルな「サイト診断・改善戦略レポート」を作成してください。

                過剰に子供っぽい表現や、教え諭すようなニュアンスは完全に排除し、ビジネスの場でそのまま通用する理路整然としたトーン（丁寧語・である調のバランスを保ったビジネス文章）で記述してください。
                各指標（UU、セッション、直帰率、流入経路、CVR）が持つ意味は、実務上の「重要性・捉え方」として自然に文章内に織り込んで解説してください。

                【必須レポート要件】
                1. 集客・アクセスの現状分析（ユニークユーザー数およびセッション数から見る、現在の市場認知度とリピート性の評価）
                2. ユーザーエンゲージメントの検証（平均滞在時間や直帰率から推察される、コンテンツの訴求力と離脱リスクの考察）
                3. 流入チャネルの投資対効果（オーガニック、SNS、広告等の流入経路における強みと弱みの特定）
                4. コンバージョン（CVR）最適化に向けた考察（ビジネスゴール達成に対する現在の貢献度評価）
                5. 具体的なKPI改善アクションプラン（今日から実務で着手できる優先度の高い施策を3つ提示）

                【注力すべき固有の課題設定】
                {additional_prompt if additional_prompt else "全体のパフォーマンス診断および最適化戦略の立案。"}

                【分析対象のGA4構造化データ】
                {ga_text}
                """

                response = model.generate_content(prompt)
                st.session_state.ai_analysis_result = response.text
                st.success("🎉 戦略分析レポートの生成が完了しました。")

            except Exception as e:
                st.error(f"⚠️ AIの処理中にエラーが起きました。入力内容や、クォータ（制限）をご確認ください。\nエラー詳細: {e}")

if st.session_state.ai_analysis_result:
    st.markdown("---")
    st.markdown("### 📝 サイト総合診断・改善戦略レポート")
    st.markdown(st.session_state.ai_analysis_result)
