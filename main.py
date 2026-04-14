import streamlit as st
import yfinance as st_yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import textwrap
import streamlit.components.v1 as components
import time

# --- Configuration & UI Setup ---
def is_mobile_device():
    try:
        user_agent = st.context.headers.get("User-Agent", "").lower()
        mobile_kw = ["mobi", "android", "iphone", "ipad", "ipod"]
        return any(kw in user_agent for kw in mobile_kw)
    except:
        return False

is_mobile = is_mobile_device()
init_state = "expanded" if is_mobile else "expanded"

st.set_page_config(page_title="رامي السهم", page_icon="📈", layout="wide", initial_sidebar_state=init_state)
# Injecting Custom CSS for a Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Tajawal', sans-serif;
    }

    /* Arabic-first layout: keep main content RTL and right-aligned */
    section.main {
        direction: rtl;
        text-align: right;
    }
    section.main h1, section.main h2, section.main h3, section.main h4, section.main h5, section.main h6,
    section.main p, section.main label, section.main li, section.main span, section.main div {
        text-align: right;
    }

    /* Center the app title + subtitle only (Streamlit-safe selectors) */
    div[data-testid="stAppViewContainer"] h1,
    div[data-testid="stAppViewContainer"] h1 * {
        text-align: center !important;
        width: 100%;
    }
    div[data-testid="stAppViewContainer"] .app-subtitle,
    div[data-testid="stAppViewContainer"] .app-subtitle * {
        text-align: center !important;
        width: 100%;
        direction: rtl;
    }
    
    /* Main Layout Tweaks */
    .stApp {
        background-color: #f8f9fa;
    }
    
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #eaeaea;
    }
    
    /* Typography */
    h1 {
        font-weight: 800;
        color: #111827;
        letter-spacing: -1px;
    }
    
    /* Recommendation Card Styling */
    .recommendation-card {
        padding: 40px 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
    }
    .recommendation-card:hover {
        transform: translateY(-2px);
    }
    
    .strong-buy { background-color: #16a34a !important; color: white !important; padding: 15px; border-radius: 10px; }
    .speed-trap { background-color: #ffd700 !important; color: black !important; padding: 15px; border-radius: 10px; }
    .buy { background-color: #16a34a !important; color: white !important; padding: 15px; border-radius: 10px; }
    .strong-sell { background-color: #dc2626 !important; color: white !important; padding: 15px; border-radius: 10px; }
    .watch { background-color: #ffd700 !important; color: black !important; padding: 15px; border-radius: 10px; }
    .neutral { background-color: #f3f4f6 !important; color: #111827 !important; padding: 15px; border-radius: 10px; }
    .hold { background-color: #2563eb !important; color: white !important; padding: 15px; border-radius: 10px; }
    .rec-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 15px;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 0px;
    }
    
    .rec-text {
        font-size: 1.35rem;
        font-weight: 600; /* Bold for clarity */
        opacity: 0.95;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Watchlist Sidebar items */
    .stButton > button {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.2s;
        display: block;
        width: 100%;
        margin-bottom: 8px;
        color: #1f2937;
    }
    .stButton > button:hover {
        background-color: #f9fafb;
        border-color: #d1d5db;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Target the text inside the button to ensure it formats properly with newlines */
    .stButton > button > div > p {
        margin-bottom: 0px;
        line-height: 1.5;
    }
    .stock-title-row {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 10px;
        flex-direction: column;
        align-items: flex-end;
        gap: 6px;
    }
    .dividend-tag {
        display: inline-block;
        background-color: #ecfdf3;
        color: #047857;
        border: 1px solid #a7f3d0;
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.95rem;
        font-weight: 700;
        line-height: 1.3;
    }
    
</style>
""", unsafe_allow_html=True)
st.title("🏹📈 رامي السهم")
st.markdown("<p class='app-subtitle' style='font-size: 1.2rem; color: #4b5563; margin-top:-15px'> تحليل الارتداد و متوسط السعر لأسهم تداول للاستثمار طويل المدى.</p>", unsafe_allow_html=True)

# --- Helper Functions ---
@st.cache_data(ttl=86400)
def fetch_data(ticker_symbol: str, years=1):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years*365)
    
    for attempt in range(3):
        try:
            data = st_yf.download(ticker_symbol, start=start_date, end=end_date, progress=False, actions=True)
            if data is not None and not data.empty:
                return data
        except Exception as e:
            if "Rate limited" in str(e) or "429" in str(e):
                time.sleep(5 * (attempt + 1))
            else:
                st.warning(f"Fetch error: {e}")
                break
    return None
def calculate_indicators(df):
    if df is None or len(df) < 20:
        return None
    
    # Yearly Average (252 trading days)
    df['Yearly_SMA'] = df['Close'].rolling(window=252, min_periods=100).mean()
    
    # Bollinger Bands (30-day SMA, 2.0 Std Dev)
    df['BB_SMA'] = df['Close'].rolling(window=30).mean()
    df['BB_STD'] = df['Close'].rolling(window=30).std()
    df['BB_Upper'] = df['BB_SMA'] + (2.0 * df['BB_STD'])
    df['BB_Lower'] = df['BB_SMA'] - (2.0 * df['BB_STD'])
    
    return df
def get_buy_recommendation(current_price, yearly_sma, bb_lower, bb_middle, bb_upper, tasi_stable):
    # Default: Not a buy zone
    rec_class = "neutral"
    rec_title = "خلك متفرج"
    rec_text = "السعر أعلى من المعدل السنوي؛ السهم حالياً يعتبر 'غالي' فنياً. انتظر تصحيح تحت المعدل السنوي."
    emoji = "⏳"

    # NaN Check
    if pd.isna(current_price) or any(pd.isna([yearly_sma, bb_lower, bb_middle, bb_upper])):
        return "data_error", "نقص بيانات", "لا توجد بيانات كافية", "⚠️"

    # --- فلتر القيمة: لا نشتري إلا إذا كان السعر تحت المعدل السنوي ---
    if current_price < yearly_sma:
        
        # 1. صيدة القاع (ارتداد من الحد السفلي)
        if current_price <= bb_lower:
            rec_class = "strong-buy"
            rec_title = "شراء (قاع القناة) 🟢🟢"
            rec_text = "السعر تحت المعدل السنوي وضرب قاع بولنجر. هذي منطقة ارتداد تاريخية وقوية."
            emoji = "💎"

        # 2. بداية انطلاق (اختراق خط المنتصف)
        elif bb_lower < current_price <= bb_middle:
            # نتحقق إذا كان السعر قريب من المنتصف للاختراق
            if (bb_middle - current_price) / (bb_middle - bb_lower) < 0.15:
                rec_class = "buy"
                rec_title = "شراء (تأكيد ارتداد) 🟢"
                rec_text = "السعر بدأ يرتد من القاع وقرب يخترق منتصف القناة. دخول آمن بتأكيد العزم."
                emoji = "🚀"
            else:
                rec_class = "buy"
                rec_title = "تجميع هادئ 🟢"
                rec_text = "السعر في مناطق رخيصة تحت المعدل السنوي وبدأ يستقر فوق قاع بولنجر."
                emoji = "🔋"

        # 3. اقتراب من السقف (رغم أنه تحت السنوي)
        elif bb_middle < current_price <= bb_upper:
            rec_class = "hold"
            rec_title = "تريّث (قرب سقف فرعي) 🔵"
            rec_text = "رغم أن السعر رخيص سنوياً، إلا أنه وصل لسقف قناة بولنجر القصيرة. انتظر تهدئة بسيطة للدخول."
            emoji = "✋"

    # --- فلتر استثنائي: إذا السوق (تاسي) غير مستقر ---
    if not tasi_stable and rec_class in ["buy", "strong-buy"]:
        rec_title += " (حذر - تاسي)"
        rec_text = "المؤشرات الفنية للسهم ممتازة، لكن وضع السوق العام (تاسي) غير مستقر. ادخل بدفعات."
        emoji = "⚠️"

    return rec_class, rec_title, rec_text, emoji
# --- Info Modal (How we analyze) ---
@st.dialog("ℹ️ كيف نحلل لك السهم؟", width="large")
def show_analysis_method_modal():
    modal_html = textwrap.dedent(
        """
        <style>
          .analysis-modal {
            direction: rtl;
            text-align: right;
            font-family: 'Inter','Tajawal',sans-serif;
          }
          .analysis-hero {
            padding: 14px 16px;
            border-radius: 14px;
            border: 1px solid rgba(229,231,235,1);
            background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(248,250,252,1) 100%);
            margin-bottom: 14px;
          }
          .analysis-hero h3{
            margin: 0 0 6px 0;
            font-weight: 800;
            color: #111827;
            letter-spacing: -0.3px;
          }
          .analysis-hero p{
            margin: 0;
            color: #374151;
            line-height: 1.8;
            font-size: 1.05rem;
          }
          .analysis-grid{
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
          }
          .analysis-card{
            padding: 14px 16px;
            border-radius: 14px;
            border: 1px solid rgba(229,231,235,1);
            background: rgba(255,255,255,1);
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
          }
          .analysis-card h4{
            margin: 0 0 8px 0;
            font-weight: 800;
            color: #111827;
          }
          .analysis-card p{
            margin: 0 0 10px 0;
            color: #374151;
            line-height: 1.8;
          }
          .analysis-card ul{
            margin: 0;
            padding-right: 18px;
            color: #374151;
            line-height: 1.9;
          }
          .analysis-note{
            display: inline-block;
            margin-top: 8px;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid rgba(191,219,254,1);
            background: rgba(239,246,255,1);
            color: #1d4ed8;
            font-weight: 700;
            font-size: 0.95rem;
          }
          .analysis-callout{
            margin-top: 12px;
            padding: 12px 14px;
            border-radius: 14px;
            border: 1px solid rgba(167,243,208,1);
            background: rgba(236,253,245,1);
            color: #064e3b;
            line-height: 1.9;
            font-weight: 700;
          }
        </style>

        <div class="analysis-modal">
          <div class="analysis-hero">
            <h3>ℹ️ كيف نحلل لك السهم؟</h3>
            <p>
              الفكرة ببساطة إننا نراقب "زحمة السير" لسعر السهم ونحدد لك إذا هو في مساره الطبيعي أو "شطح" بزيادة.
              نعتمد على أداتين أساسية:
            </p>
          </div>

          <div class="analysis-grid">
            <div class="analysis-card">
              <h4>1️⃣ ميزان السعر (المتوسط المتحرك)</h4>
              <p>
                هذا هو "المنطقة الدافئة" للسهم، وهو متوسط سعره لآخر <b>30 يوم</b>.
              </p>
              <ul>
                <li><b>فوق الميزان</b>: السهم في حالة نشاط وعزمه قوي (مسار صاعد).</li>
                <li><b>تحت الميزان</b>: السهم يمر بفترة خمول أو ضغط بيع (مسار هابط).</li>
                <li><b>قرب الميزان</b>: السهم قاعد يختبر قوته؛ إما يرتد منه ويواصل، أو يكسره ويغير اتجاهه.</li>
              </ul>
            </div>

            <div class="analysis-card">
              <h4>2️⃣ قناة الارتداد (Bollinger Bands)</h4>
              <p>
                تخيلها مثل "الجدران" اللي يتحرك بينها السهم. إذا ضرب في واحد منها، غالباً يرجع للثاني:
                <br/>
                <span class="analysis-note">في هذا التطبيق: متوسط 30 يوم، وانحراف معياري 2.0</span>
              </p>
              <ul>
                <li><b>عند الجدار السفلي (القاع)</b>: السهم صار "منضغط" ورخيص بزيادة، وغالباً يرتد للأعلى. (فرصة صيد).</li>
                <li><b>عند الجدار العلوي (السقف)</b>: السهم "طمره" أعلى من اللزوم، ومن الطبيعي يهدي أو يرجع يصحح. (منطقة جني أرباح).</li>
                <li><b>خارج القناة</b>: هنا السهم دخل منطقة "غير طبيعية"؛ يا إنه انفجار سعري قوي، أو إنه بدايه هبوط حاد.</li>
              </ul>
            </div>
          </div>

          <div class="analysis-callout">
            💡 الخلاصة اللي تهمك:<br/>
            نحن ندمج "الميزان" مع "الجدار"؛ فإذا كان السهم فوق الميزان (قوي) ووصل للجدار السفلي (رخيص)،
            فهذي هي "اللقطة" اللي يبحث عنها المحترفين.
          </div>
        </div>
        """
    ).strip()

    # Render the full explanation without internal scrolling
    components.html(modal_html, height=760, scrolling=False)

    # Mini example chart (synthetic "price correction" scenario)
    dates = pd.date_range(end=datetime.now().date(), periods=80, freq="B")
    # A simple synthetic series: uptrend then correction then recovery
    base = pd.Series(range(len(dates)), index=dates).astype(float)
    price = 100 + (base * 0.35)
    price.iloc[45:60] = price.iloc[45] - (pd.Series(range(15), index=dates[45:60]) * 1.1)  # correction down
    price.iloc[60:] = price.iloc[59] + (pd.Series(range(len(dates[60:])), index=dates[60:]) * 0.55)  # recovery
    price = price.rolling(2, min_periods=1).mean()

    mid = price.rolling(30, min_periods=30).mean()
    std = price.rolling(30, min_periods=30).std()
    upper = mid + (2 * std)
    lower = mid - (2 * std)

    example_fig = go.Figure()
    example_fig.add_trace(go.Scatter(x=dates, y=price, mode="lines", name="السعر (مثال)", line=dict(color="#2563eb", width=2.5)))
    example_fig.add_trace(go.Scatter(x=dates, y=mid, mode="lines", name="المتوسط (30)", line=dict(color="#f59e0b", width=2, dash="dash")))
    example_fig.add_trace(go.Scatter(x=dates, y=upper, mode="lines", name="بولنجر علوي", line=dict(color="rgba(37,99,235,0.35)", width=1)))
    example_fig.add_trace(go.Scatter(x=dates, y=lower, mode="lines", name="بولنجر سفلي", line=dict(color="rgba(37,99,235,0.35)", width=1), fill="tonexty", fillcolor="rgba(37, 99, 235, 0.10)"))
    example_fig.update_layout(
        title="مثال توضيحي: تصحيح سعري داخل/قرب قنوات بولنجر (30 يوم، 2.0 انحراف معياري)",
        margin=dict(l=10, r=10, t=50, b=10),
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248, 249, 250, 0.5)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="",
        yaxis_title="السعر",
    )
    example_fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,0,0,0.05)")
    example_fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(0,0,0,0.05)")

    st.plotly_chart(example_fig, use_container_width=True)
# --- Stock Dictionary ---
SAUDI_STOCKS = {
    "1120": "Al Rajhi Bank (1120)", "2222": "Saudi Aramco (2222)", "2010": "SABIC (2010)",
    "1180": "Saudi National Bank - SNB (1180)", "7010": "Saudi Telecom Company - STC (7010)",
    "1150": "Alinma Bank (1150)", "1211": "Ma'aden (1211)", "1010": "Riyad Bank (1010)",
    "1050": "Banque Saudi Fransi (1050)", "1060": "Saudi Awwal Bank - SAB (1060)",
    "1080": "Arab National Bank - ANB (1080)", "1140": "Bank Albilad (1140)",
    "1020": "Bank AlJazira (1020)", "1030": "Saudi Investment Bank (1030)",
    "5110": "Saudi Electricity (5110)", "2281": "ACWA Power (2281)",
    "2020": "SABIC Agri-Nutrients (2020)", "2060": "TASNEE (2060)",
    "2250": "SIIG (2250)", "2350": "Saudi Kayan (2350)",
    "2380": "Petro Rabigh (2380)", "2280": "Almarai (2280)",
    "4190": "Jarir (4190)", "4003": "eXtra (4003)",
    "4002": "Mouwasat (4002)", "2270": "SADAFCO (2270)",
    "4030": "Bahri (4030)", "4280": "Kingdom Holding (4280)",
    "4321": "Cenomi Centers (4321)", "7020": "Etihad Etisalat - Mobily (7020)",
    "7030": "Zain KSA (7030)",
    "2281": "ACWA Power (2281)",
    "2250": "SIIG (2250)",
    "2270": "SADAFCO (2270)",
    "4280": "Kingdom Holding (4280)",
    "7020": "Etihad Etisalat - Mobily (7020)",
    "7030": "Zain KSA (7030)",
    "4002": "Mouwasat (4002)",
}
# --- State Management ---
if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = "1120.SR"
    st.session_state.previous_ticker = "1120.SR"
# Sidebar search state
if "sidebar_search_query" not in st.session_state:
    st.session_state.sidebar_search_query = ""
if "sidebar_search_applied" not in st.session_state:
    st.session_state.sidebar_search_applied = False
if "sidebar_filtered_codes" not in st.session_state:
    st.session_state.sidebar_filtered_codes = None
# --- Sidebar Watchlist ---
with st.sidebar:
    # Temporarily disable search UI + filtering
    # st.header("🔍 البحث عن سهم")
    # search_query = st.text_input(
    #     "ابحث بالاسم أو الرقم:",
    #     placeholder="مثال: Riyad أو 1010",
    #     value=st.session_state.sidebar_search_query,
    # ).strip()
    # search_cols = st.columns([1, 1])
    # with search_cols[0]:
    #     do_search = st.button("بحث", use_container_width=True)
    # with search_cols[1]:
    #     clear_search = st.button("مسح", use_container_width=True)
    # ...
    st.session_state.sidebar_search_query = ""
    st.session_state.sidebar_search_applied = False
    st.session_state.sidebar_filtered_codes = None
    
    # Search affects only the clickable cards list below (not the watchlist selectbox)
    # Watchlist selectbox should always show all stocks.
    options = list(SAUDI_STOCKS.values())
    
    # Pre-select based on session state
    current_idx = 0
    code = st.session_state.selected_ticker.replace('.SR', '')
    for i, opt in enumerate(options):
        if f"({code})" in opt:
            current_idx = i
            break
            
    st.write("---")
    st.header("📋 قائمة الاسهم")
    selected_option = st.selectbox("اختر سهماً من تداول:", options, index=current_idx)
    # Extract the 4 digit code inside the parentheses
    sel_code = selected_option.split('(')[-1].strip(')')
    ticker = f"{sel_code}.SR"
        
    st.session_state.selected_ticker = ticker
    
    # We batch download to prevent many separate API calls.
    # Keep the cards in a fixed order (dictionary insertion order).
    selected_code_for_sidebar = st.session_state.selected_ticker.replace(".SR", "")
    sidebar_codes_to_show = list(SAUDI_STOCKS.keys())
    all_tickers = [f"{k}.SR" for k in sidebar_codes_to_show]

    # Highlight the selected card in the sidebar list
    st.markdown(
        f"""
        <style>
          .st-key-btn_{selected_code_for_sidebar} button {{
            border: 2px solid #2563eb !important;
            background: rgba(37, 99, 235, 0.08) !important;
            box-shadow: 0 8px 16px -12px rgba(37, 99, 235, 0.55) !important;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    with st.spinner("جاري تحميل قائمة المراقبة..."):
        # Fetch TASI first for market stability
        tasi_data = fetch_data("^TASI.SR")
        tasi_stable = "unstable"
        if tasi_data is not None and not tasi_data.empty:
            tasi_data['TASI_50_SMA'] = tasi_data['Close'].rolling(window=50).mean()
            tasi_data['TASI_200_SMA'] = tasi_data['Close'].rolling(window=200).mean()
            tasi_current = float(tasi_data['Close'].iloc[-1].item() if isinstance(tasi_data['Close'].iloc[-1], pd.Series) else tasi_data['Close'].iloc[-1])
            tasi_50_sma = float(tasi_data['TASI_50_SMA'].iloc[-1].item() if isinstance(tasi_data['TASI_50_SMA'].iloc[-1], pd.Series) else tasi_data['TASI_50_SMA'].iloc[-1])
            
            # Less restrictive TASI stability
            if tasi_current >= tasi_50_sma:
                tasi_stable = "stable"
            elif tasi_current >= (tasi_50_sma * 0.95): # Within 5% of 50-day average
                tasi_stable = "cautious"
        # Download all stocks
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        # yfinance caching wrapper for the batch download
        @st.cache_data(ttl=86400)
        def fetch_batch(tickers):
            for attempt in range(3):
                try:
                    # yfinance will now automatically use curl_cffi internally
                    data = st_yf.download(
                        tickers, 
                        start=start_date, 
                        end=end_date, 
                        progress=False, 
                        group_by='ticker', 
                        actions=True,
                        threads=True
                    )
                    if data is not None and not data.empty:
                        return data
                except Exception as e:
                    if "Rate limited" in str(e) or "429" in str(e):
                        time.sleep(5 * (attempt + 1))
                    else:
                        st.warning(f"Fetch batch error: {e}")
                        break
            return None
        
        batch_data = fetch_batch(all_tickers)
        
        if batch_data is not None and not batch_data.empty:
            for dcode in sidebar_codes_to_show:
                dname = SAUDI_STOCKS.get(dcode, dcode)
                list_ticker = f"{dcode}.SR"
                try:
                    # yfinance returns a MultiIndex when downloading multiple tickers
                    if len(all_tickers) > 1:
                         df = batch_data[list_ticker].dropna(how='all')
                    else:
                         df = batch_data.dropna(how='all')
                    
                    if not df.empty and len(df) > 20:
                        df = calculate_indicators(df)
                        current_price = float(df['Close'].iloc[-1].item() if isinstance(df['Close'].iloc[-1], pd.Series) else df['Close'].iloc[-1])
                        yearly_sma = float(df['Yearly_SMA'].iloc[-1].item() if isinstance(df['Yearly_SMA'].iloc[-1], pd.Series) else df['Yearly_SMA'].iloc[-1])
                        bb_lower = float(df['BB_Lower'].iloc[-1].item() if isinstance(df['BB_Lower'].iloc[-1], pd.Series) else df['BB_Lower'].iloc[-1])
                        bb_middle = float(df['BB_SMA'].iloc[-1].item() if isinstance(df['BB_SMA'].iloc[-1], pd.Series) else df['BB_SMA'].iloc[-1])
                        bb_upper = float(df['BB_Upper'].iloc[-1].item() if isinstance(df['BB_Upper'].iloc[-1], pd.Series) else df['BB_Upper'].iloc[-1])
                        
                        rec_class, rec_title, _, emoji = get_recommendation(current_price, yearly_sma, bb_lower, bb_middle, bb_upper, tasi_stable)
                        
                        pays_dividends = 'Dividends' in df.columns and bool((df['Dividends'] > 0).values.any())
                        div_flag = " 💰" if pays_dividends else ""
                        
                        tag = " (فرصة جيدة للبيع)" if rec_class == "strong-sell" else ""
                        st.markdown("""
    <style>
    div.stButton > button p {
        white-space: pre-line;      /* Respects the \\n in your string */
        text-align: center;         /* Center multi-line label text */
        display: block;             /* Ensures the paragraph fills the button width */
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)
                        btn_label = f"{emoji} {dname.split(' (')[0]}{tag}{div_flag}\n(السعر: {current_price:.2f})\n(المتوسط: {yearly_sma:.2f})"


                        if st.button(btn_label, key=f"btn_{dcode}", use_container_width=True):
                            st.session_state.selected_ticker = list_ticker
                            st.rerun()
                            
                except Exception as e:
                    pass
        else:
            st.info("عفواً، مزود البيانات مشغول حالياً (تم تجاوز الحد المسموح).نعرض البيانات المخبأة أو يرجى المحاولة بعد قليل.")
# --- Main Logic ---
if st.session_state.get("previous_ticker") != st.session_state.selected_ticker:
    if is_mobile:
        st.session_state.close_mobile_sidebar = True
    st.session_state.previous_ticker = st.session_state.selected_ticker

col1, col2 = st.columns([1, 4]) # Adjusted columns slightly since sidebar does all the navigation now
with col2:
    ticker = st.session_state.selected_ticker
    stock_data = None
    tasi_data = None
    if ticker:
        # Extract stock name for main display
        stock_name_display = "سهم غير معروف"
        code_only = ticker.replace('.SR', '')
        for k, v in SAUDI_STOCKS.items():
            if k == code_only:
                stock_name_display = v
                break
                
        with st.spinner('جاري جلب البيانات...'):
            stock_data = fetch_data(ticker)
            tasi_data = fetch_data("^TASI.SR")
            
        has_dividends = False
        if stock_data is not None and not stock_data.empty and 'Dividends' in stock_data.columns:
            if bool((stock_data['Dividends'] > 0).values.any()):
                has_dividends = True
        
        stock_header_html = f"<div class='stock-title-row'><h2 style='margin:0'>تحليل سهم: {stock_name_display}</h2>"
        if has_dividends:
            stock_header_html += "<span class='dividend-tag'>💰 يوزع أرباح</span>"
        stock_header_html += "</div>"
        st.markdown(stock_header_html, unsafe_allow_html=True)
        
    if stock_data is not None and tasi_data is not None:
        stock_data = calculate_indicators(stock_data)
        
        # Calculate TASI health (50-day SMA vs Current)
        tasi_data['TASI_50_SMA'] = tasi_data['Close'].rolling(window=50).mean()
        
        if stock_data is not None and len(stock_data) > 0 and len(tasi_data) > 0:
            current_price = float(stock_data['Close'].iloc[-1].item() if isinstance(stock_data['Close'].iloc[-1], pd.Series) else stock_data['Close'].iloc[-1])
            yearly_sma = float(stock_data['Yearly_SMA'].iloc[-1].item() if isinstance(stock_data['Yearly_SMA'].iloc[-1], pd.Series) else stock_data['Yearly_SMA'].iloc[-1])
            bb_lower = float(stock_data['BB_Lower'].iloc[-1].item() if isinstance(stock_data['BB_Lower'].iloc[-1], pd.Series) else stock_data['BB_Lower'].iloc[-1])
            bb_middle = float(stock_data['BB_SMA'].iloc[-1].item() if isinstance(stock_data['BB_SMA'].iloc[-1], pd.Series) else stock_data['BB_SMA'].iloc[-1])
            bb_upper = float(stock_data['BB_Upper'].iloc[-1].item() if isinstance(stock_data['BB_Upper'].iloc[-1], pd.Series) else stock_data['BB_Upper'].iloc[-1])
            
            tasi_current = float(tasi_data['Close'].iloc[-1].item() if isinstance(tasi_data['Close'].iloc[-1], pd.Series) else tasi_data['Close'].iloc[-1])
            tasi_50_sma = float(tasi_data['TASI_50_SMA'].iloc[-1].item() if isinstance(tasi_data['TASI_50_SMA'].iloc[-1], pd.Series) else tasi_data['TASI_50_SMA'].iloc[-1])
            tasi_stable = "unstable"
            if tasi_current >= tasi_50_sma:
                tasi_stable = "stable"
            elif tasi_current >= (tasi_50_sma * 0.95):
                tasi_stable = "cautious"
            # --- Recommendation Engine ---
            rec_class = "neutral"
            rec_title = "مراقبة"
            rec_text = ""
            emoji = "⚪"
            if pd.notna(yearly_sma) and pd.notna(bb_lower) and pd.notna(bb_upper) and pd.notna(bb_middle):
                rec_class, rec_title, rec_text, emoji = get_recommendation(current_price, yearly_sma, bb_lower, bb_middle, bb_upper, tasi_stable)

            avg_delta_pct = None
            if pd.notna(yearly_sma) and yearly_sma != 0:
                avg_delta_pct = ((current_price - yearly_sma) / yearly_sma) * 100.0
            avg_delta_pct_text = "—" if avg_delta_pct is None or pd.isna(avg_delta_pct) else f"{avg_delta_pct:+.2f}%"
            # Display Recommendation Card
            st.markdown(f"""
            <div class="recommendation-card {rec_class}">
                <div class="rec-title">{rec_title}</div>
                <div class="rec-text">{rec_text}</div>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); display: flex; justify-content: center; gap: 30px; font-weight: 600;">
                    <div>السعر الحالي<br><span style="font-size: 1.3em;">SAR {current_price:.2f}</span></div>
                    <div>المتوسط السنوي<br><span style="font-size: 1.3em;">SAR {yearly_sma:.2f}</span></div>
                    <div>التغير عن المتوسط<br><span style="font-size: 1.3em;">{avg_delta_pct_text}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("⚠️  تنبيه: هذا المحتوى مجرد توقع بناء على تحليلات بسيطة، وليس توصية استثمارية رسمية أو دعوة للبيع/الشراء.")
            # --- Plotly Chart ---
            st.subheader(f"سجل الأسعار والمؤشرات - {ticker}")
            fig = go.Figure()
            # Price Line
            # Handling 1D column access carefully because yfinance .download can return nested DataFrames
            close_prices = stock_data['Close'].squeeze()
            yearly_sma_series = stock_data['Yearly_SMA'].squeeze()
            upper_bb = stock_data['BB_Upper'].squeeze()
            lower_bb = stock_data['BB_Lower'].squeeze()
            fig.add_trace(go.Scatter(
                x=stock_data.index, y=close_prices,
                mode='lines', name='السعر الحالي',
                line=dict(color='#2563eb', width=2.5) # Sleek blue
            ))
            # Yearly SMA
            fig.add_trace(go.Scatter(
                x=stock_data.index, y=yearly_sma_series,
                mode='lines', name='المتوسط السنوي (الفلتر الأساسي)',
                line=dict(color='#f59e0b', width=2, dash='dash') # Amber
            ))
            # Bollinger Bands (Shaded area)
            fig.add_trace(go.Scatter(
                x=stock_data.index, y=upper_bb,
                line=dict(width=0), name='الحد العلوي  لقناة الارتداد',
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=stock_data.index, y=lower_bb,
                fill='tonexty', fillcolor='rgba(37, 99, 235, 0.1)', # Very light transparent blue
                line=dict(width=0), name='الحد السفلي  لقناة الارتداد',
                hoverinfo='skip'
            ))
            fig.update_layout(
                xaxis_title="",
                yaxis_title="السعر (ريال)",
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248, 249, 250, 0.5)', # Match stApp background mostly
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor="rgba(255, 255, 255, 0.8)"
                )
            )
            
            # Minor Grid tweaks
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)')
            
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("الملخص الفني"):
                if st.button("ℹ️ كيف تم التحليل؟", help="فتح شرح طريقة التحليل", key="analysis_info_btn"):
                    show_analysis_method_modal()
                st.write(f"استقرار تاسي: {'نعم (أعلى من متوسط 50 يوماً)' if tasi_stable else 'لا (أقل من متوسط 50 يوماً)'}")
                st.write(f"السعر الحالي: {current_price:.2f}")
                st.write(f"المتوسط السنوي: {yearly_sma:.2f}")
                st.write(f"التغير عن المتوسط السنوي: {avg_delta_pct_text}")
                st.write(f"نطاق  قناة الارتداد السفلي: {bb_lower:.2f}")
                st.write(f"نطاق قناة الارتداد العلوي: {bb_upper:.2f}")
        else:
             st.error("بيانات غير كافية لحساب المؤشرات. يرجى تجربة سهم آخر.")       
    else:
        st.error("خطأ في جلب البيانات. يرجى التأكد من صحة رمز السهم (مثال: 2222 لشركة أرامكو السعودية).")

# --- Mobile Sidebar Auto-Close Injection ---
if st.session_state.get("close_mobile_sidebar", False):
    st.session_state.close_mobile_sidebar = False
    import uuid
    run_id = uuid.uuid4().hex
    components.html(
        f"""
        <script>
        // Force Streamlit to re-execute this script by making the string unique: {run_id}
        setTimeout(function() {{
            var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {{
                var closeBtn = sidebar.querySelector('button');
                if (closeBtn) closeBtn.click();
            }}
        }}, 300);
        </script>
        """,
        height=0, width=0
    )
