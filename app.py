import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ========================================
# KONFIGURASI HALAMAN
# ========================================
st.set_page_config(
    page_title="Dashboard Pasar BMW",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# CUSTOM CSS UNTUK STYLING
# ========================================
st.markdown("""
    <style>
    /* Background putih (default) */
    .stApp {
        background: #ffffff !important;
    }
    
    /* Force White Background for Filter Container */
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stBorderWrapper"],
    div[class*="stVerticalBlockBorderWrapper"],
    div[class*="stBorderWrapper"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }
    
    /* Container untuk setiap section - efek mengambang (Legacy/Manual) */
    .section-container {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Styling untuk metric cards */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.06);
        border: 1px solid rgba(59, 130, 246, 0.1);
        border-top: 4px solid #1C69D4;  /* Garis biru BMW di atas card */
        transition: transform 0.2s;
    }
    
    /* Hover effect untuk metric cards */
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.08);
    }
    
    /* Font value di metric - Bold, Modern, Biru */
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #1C69D4 !important;  /* Biru BMW */
        font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif !important;
    }
    
    /* Styling label metric */
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #64748b !important;
    }
    
    /* Header dengan gradient */
    h1 {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        text-align: center;
        padding: 15px 0;
        font-size: 32px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Filter container dengan styling lebih cantik */
    .filter-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.06);
        border: 1px solid rgba(59, 130, 246, 0.1);
    }
    
    /* Styling untuk checkbox dan radio */
    .stCheckbox, .stRadio {
        padding: 5px 0;
    }
    
    /* Divider styling */
    hr {
        margin: 20px 0;
        border: none;
        border-top: 2px solid rgba(59, 130, 246, 0.1);
    }
    
    /* Multiselect styling */
    .stMultiSelect {
        font-size: 14px;
    }
    
    /* Multiselect tag styling - ubah merah ke biru */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #1C69D4 !important;
    }
    
    /* Selectbox styling - ubah merah ke biru */
    .stSelectbox [data-baseweb="select"] {
        border-color: #1C69D4 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# FUNGSI UNTUK LOAD DATA
# ========================================
@st.cache_data
def load_data():
    """Load data dari CSV"""
    try:
        df = pd.read_csv('bmw_pricing_data.csv')
        df['Year'] = df['Year'].astype(int)
        df['Price_USD'] = df['Price_USD'].astype(float)
        return df
    except FileNotFoundError:
        st.error("❌ File 'bmw_pricing_data.csv' tidak ditemukan!")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error saat membaca file: {str(e)}")
        st.stop()

# ========================================
# FUNGSI KONVERSI MATA UANG
# ========================================
def convert_currency(amount, currency):
    """Konversi dari USD ke mata uang lain"""
    rates = {
        'US Dollar': 1.0,
        'Euro': 0.92,
        'Rupiah': 15800.0
    }
    return amount * rates[currency]

def format_currency(amount, currency):
    """Format angka sesuai mata uang"""
    if currency == 'US Dollar':
        return f"${amount:,.0f}"
    elif currency == 'Euro':
        return f"€{amount:,.0f}"
    elif currency == 'Rupiah':
        return f"Rp {amount:,.0f}"

# ========================================
# LOAD DATA
# ========================================
df = load_data()

# ========================================
# HEADER
# ========================================
st.markdown("""
    <div style='margin-bottom: 20px; padding-top: 20px;'>
        <h1 style='text-align: center; color: #1e40af;'>Dashboard Pasar BMW: Analisis Harga & Prediksi Harga</h1>
        <p style='text-align: center; color: #64748b; font-size: 14px; margin-top: -10px; margin-bottom: 0px;'>
            Dashboard interaktif untuk menganalisis tren harga mobil BMW, membandingkan performa antar model, 
            dan memprediksi harga masa depan berdasarkan data historis
        </p>
    </div>
""", unsafe_allow_html=True)

# ========================================
# BARIS 1: KPI METRICS DENGAN PERSENTASE (akan dihitung setelah filter)
# ========================================
# Placeholder - akan diisi setelah filter diterapkan
kpi_placeholder = st.empty()

# ========================================
# BARIS 2: FILTERS HORIZONTAL
# ========================================
# Inisialisasi currency default
if 'selected_currency' not in st.session_state:
    st.session_state.selected_currency = 'US Dollar'

with st.container(border=True):
    st.markdown("### 🔍 Filter Data")

    filter_cols = st.columns([2, 2, 2, 3])

    with filter_cols[0]:
        st.markdown("**Jenis Transmisi**")
        trans_btn_cols = st.columns(2)
        
        with trans_btn_cols[0]:
            auto_selected = st.checkbox("Automatic", value=True, key="auto")
        with trans_btn_cols[1]:
            manual_selected = st.checkbox("Manual", value=True, key="manual")

    with filter_cols[1]:
        st.markdown("**Mata Uang**")
        currency_btn_cols = st.columns(3)
        
        with currency_btn_cols[0]:
            usd_selected = st.button("USD", key="usd", use_container_width=True)
        with currency_btn_cols[1]:
            eur_selected = st.button("EUR", key="eur", use_container_width=True)
        with currency_btn_cols[2]:
            idr_selected = st.button("IDR", key="idr", use_container_width=True)
        
        # Update selected currency
        if usd_selected:
            st.session_state.selected_currency = 'US Dollar'
        elif eur_selected:
            st.session_state.selected_currency = 'Euro'
        elif idr_selected:
            st.session_state.selected_currency = 'Rupiah'
        
        selected_currency = st.session_state.selected_currency

    with filter_cols[2]:
        st.markdown("**Tahun**")
        year_options = ['All'] + sorted(df['Year'].unique().tolist(), reverse=True)
        selected_year = st.selectbox(
            "",
            year_options,
            index=0,
            key="year",
            label_visibility="collapsed"
        )

    with filter_cols[3]:
        st.markdown("**Model**")
        all_models = sorted(df['Model'].unique().tolist())
        selected_models = st.multiselect(
            "",
            all_models,
            default=all_models,
            key="model",
            label_visibility="collapsed",
            placeholder="Pilih model..."
        )

# ========================================
# FILTER DATA BERDASARKAN PILIHAN USER
# ========================================
# Filter transmisi
transmission_filter = []
if auto_selected:
    transmission_filter.append('Automatic')
if manual_selected:
    transmission_filter.append('Manual')

# Jika tidak ada transmisi yang dipilih, tampilkan semua
if not transmission_filter:
    transmission_filter = df['Transmission'].unique().tolist()

# Apply filters
filtered_df = df[df['Transmission'].isin(transmission_filter)]

# Filter tahun (jika bukan "All")
if selected_year != 'All':
    filtered_df = filtered_df[filtered_df['Year'] == int(selected_year)]

# Filter model (jika ada yang dipilih)
if selected_models:
    filtered_df = filtered_df[filtered_df['Model'].isin(selected_models)]

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

# ========================================
# HITUNG KPI METRICS BERDASARKAN FILTERED DATA
# ========================================
# Pisahkan data actual dan forecast dari filtered data
actual_filtered = filtered_df[filtered_df['Type'] == 'Actual']
forecast_filtered = filtered_df[filtered_df['Type'] == 'Forecast']

if not actual_filtered.empty:
    # Jika memilih tahun spesifik, bandingkan dengan tahun sebelumnya
    if selected_year != 'All':
        current_year = int(selected_year)
        prev_year = current_year - 1
        
        # Data tahun yang dipilih (sudah terfilter)
        current_year_data = actual_filtered[actual_filtered['Year'] == current_year]
        
        # Data tahun sebelumnya dari dataset asli (dengan filter model & transmisi yang sama)
        prev_year_base = df[df['Type'] == 'Actual']
        prev_year_base = prev_year_base[prev_year_base['Year'] == prev_year]
        
        # Apply filter transmisi dan model yang sama
        transmission_filter_list = []
        if auto_selected:
            transmission_filter_list.append('Automatic')
        if manual_selected:
            transmission_filter_list.append('Manual')
        if not transmission_filter_list:
            transmission_filter_list = df['Transmission'].unique().tolist()
        
        prev_year_data = prev_year_base[prev_year_base['Transmission'].isin(transmission_filter_list)]
        if selected_models:
            prev_year_data = prev_year_data[prev_year_data['Model'].isin(selected_models)]
    else:
        # Jika "All", ambil tahun terbaru dan sebelumnya
        available_years = sorted(actual_filtered['Year'].unique())
        
        if len(available_years) >= 2:
            current_year = available_years[-1]
            prev_year = available_years[-2]
        else:
            current_year = available_years[-1] if available_years else actual_filtered['Year'].max()
            prev_year = current_year - 1
        
        current_year_data = actual_filtered[actual_filtered['Year'] == current_year]
        prev_year_data = actual_filtered[actual_filtered['Year'] == prev_year]
    
    # Hitung metrics tahun sekarang
    min_price = current_year_data['Price_USD'].min() if not current_year_data.empty else 0
    max_price = current_year_data['Price_USD'].max() if not current_year_data.empty else 0
    avg_price = current_year_data['Price_USD'].mean() if not current_year_data.empty else 0
    
    # Hitung metrics tahun lalu
    min_price_prev = prev_year_data['Price_USD'].min() if not prev_year_data.empty else min_price
    max_price_prev = prev_year_data['Price_USD'].max() if not prev_year_data.empty else max_price
    avg_price_prev = prev_year_data['Price_USD'].mean() if not prev_year_data.empty else avg_price
    
    # Hitung persentase perubahan
    min_pct = ((min_price - min_price_prev) / min_price_prev * 100) if min_price_prev > 0 else 0
    max_pct = ((max_price - max_price_prev) / max_price_prev * 100) if max_price_prev > 0 else 0
    avg_pct = ((avg_price - avg_price_prev) / avg_price_prev * 100) if avg_price_prev > 0 else 0
    
    # Hitung prediksi harga dari data forecast yang sudah difilter
    if not forecast_filtered.empty:
        predicted_price = forecast_filtered['Price_USD'].mean()
        pred_pct = ((predicted_price - avg_price) / avg_price * 100) if avg_price > 0 else 0
    else:
        predicted_price = avg_price
        pred_pct = 0
else:
    # Fallback jika tidak ada data actual
    min_price = filtered_df['Price_USD'].min()
    max_price = filtered_df['Price_USD'].max()
    avg_price = filtered_df['Price_USD'].mean()
    predicted_price = avg_price
    min_pct = max_pct = avg_pct = pred_pct = 0

# Konversi ke mata uang yang dipilih
min_price_converted = convert_currency(min_price, selected_currency)
max_price_converted = convert_currency(max_price, selected_currency)
avg_price_converted = convert_currency(avg_price, selected_currency)
predicted_price_converted = convert_currency(predicted_price, selected_currency)

# Tentukan apakah persentase ditampilkan (hanya jika memilih tahun spesifik, bukan "All")
show_delta = (selected_year != 'All')

# Tampilkan KPI Cards di placeholder (tanpa container tambahan)
with kpi_placeholder.container():
    kpi_cols = st.columns(4)
    
    with kpi_cols[0]:
        if show_delta:
            st.metric(
                label="Harga Minimal",
                value=format_currency(min_price_converted, selected_currency),
                delta=f"{min_pct:+.1f}% vs tahun sebelumnya"
            )
        else:
            st.metric(
                label="Harga Minimal",
                value=format_currency(min_price_converted, selected_currency)
            )
    
    with kpi_cols[1]:
        if show_delta:
            st.metric(
                label="Harga Maksimal",
                value=format_currency(max_price_converted, selected_currency),
                delta=f"{max_pct:+.1f}% vs tahun sebelumnya"
            )
        else:
            st.metric(
                label="Harga Maksimal",
                value=format_currency(max_price_converted, selected_currency)
            )
    
    with kpi_cols[2]:
        if show_delta:
            st.metric(
                label="Harga Rata-rata",
                value=format_currency(avg_price_converted, selected_currency),
                delta=f"{avg_pct:+.1f}% vs tahun sebelumnya"
            )
        else:
            st.metric(
                label="Harga Rata-rata",
                value=format_currency(avg_price_converted, selected_currency)
            )
    
    with kpi_cols[3]:
        if show_delta:
            st.metric(
                label="Prediksi Harga",
                value=format_currency(predicted_price_converted, selected_currency),
                delta=f"{pred_pct:+.1f}% vs harga saat ini"
            )
        else:
            st.metric(
                label="Prediksi Harga",
                value=format_currency(predicted_price_converted, selected_currency)
            )

# ========================================
# BARIS 3: LINE CHART - RATA-RATA HARGA PER TAHUN
# ========================================
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown("### 📈 Tren Harga Mobil Per Tahun")

# Hitung rata-rata harga per tahun per model
trend_data = filtered_df.groupby(['Year', 'Model'])['Price_USD'].mean().reset_index()

# Konversi ke mata uang yang dipilih
trend_data['Price_Converted'] = trend_data['Price_USD'].apply(
    lambda x: convert_currency(x, selected_currency)
)

# Buat line chart dengan warna BMW blue
# Palet warna BMW: biru, abu-abu gelap, putih
bmw_colors = ['#1C69D4', '#0E4C92', '#00A1E4', '#6C757D', '#2C5F9E', '#4A90E2']

fig_line = px.line(
    trend_data,
    x='Year',
    y='Price_Converted',
    color='Model',
    markers=True,
    labels={'Price_Converted': 'Harga Rata-rata', 'Year': 'Tahun'},
    template='plotly_white',
    color_discrete_sequence=bmw_colors  # Warna BMW
)

# Update traces dengan garis tajam (linear)
fig_line.update_traces(
    line=dict(width=3),  # Garis lurus dengan lebar 3
    marker=dict(size=8),
    fill='tonexty',  # Fill area di bawah garis
    fillcolor='rgba(28, 105, 212, 0.1)'  # Warna biru BMW dengan transparansi
)

# Set fill untuk trace pertama ke 'tozeroy'
fig_line.data[0].fill = 'tozeroy'
fig_line.data[0].fillcolor = 'rgba(28, 105, 212, 0.1)'

# Jika hanya 1 model dipilih, tambahkan persentase di setiap titik (tanpa kotak dan arrow)
if len(selected_models) == 1:
    model_trend = trend_data[trend_data['Model'] == selected_models[0]].sort_values('Year')
    
    # Hitung persentase perubahan
    annotations = []
    for i in range(1, len(model_trend)):
        prev_price = model_trend.iloc[i-1]['Price_Converted']
        curr_price = model_trend.iloc[i]['Price_Converted']
        pct_change = ((curr_price - prev_price) / prev_price * 100) if prev_price > 0 else 0
        
        # Warna berdasarkan naik/turun
        color = '#22c55e' if pct_change > 0 else '#ef4444' if pct_change < 0 else '#6b7280'
        
        # Annotation tanpa kotak dan arrow - hanya text
        annotations.append(
            dict(
                x=model_trend.iloc[i]['Year'],
                y=curr_price,
                text=f"{pct_change:+.1f}%",
                showarrow=False,  # Hapus arrow
                font=dict(size=12, color=color, family="Arial Black"),
                yshift=15,  # Geser ke atas sedikit
                xanchor='center'
            )
        )
    
    fig_line.update_layout(annotations=annotations)

# Hitung range Y-axis yang optimal untuk menampilkan variasi data
y_min = trend_data['Price_Converted'].min()
y_max = trend_data['Price_Converted'].max()
y_range = y_max - y_min
# Tambahkan padding 10% di atas dan bawah agar grafik tidak terlalu mepet
y_padding = y_range * 0.1
y_axis_min = max(0, y_min - y_padding)  # Minimal 0
y_axis_max = y_max + y_padding

fig_line.update_layout(
    hovermode='x unified',
    height=400,
    font=dict(size=12),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=50, r=50, t=30, b=80),
    showlegend=True,
    plot_bgcolor='rgba(0,0,0,0)',  # Background transparan
    paper_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(
        range=[y_axis_min, y_axis_max],  # Set range Y-axis agar zoom in
        gridcolor='rgba(200, 200, 200, 0.2)'  # Grid lebih subtle
    ),
    xaxis=dict(
        gridcolor='rgba(200, 200, 200, 0.2)'
    )
)

st.plotly_chart(fig_line, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)  # Tutup container grafik

# ========================================
# BARIS 4: ANALISIS PASAR & REKOMENDASI INVESTASI
# ========================================
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown("## 📖 Analisis Pasar & Rekomendasi Investasi")
st.markdown("*Insight cerdas berdasarkan analisis data historis dan prediksi masa depan*")
st.markdown("<br>", unsafe_allow_html=True)

# Analisis data untuk storytelling
actual_data = filtered_df[filtered_df['Type'] == 'Actual']
forecast_data = filtered_df[filtered_df['Type'] == 'Forecast']

if not actual_data.empty:
    # Analisis per model
    model_analysis = []
    for model in filtered_df['Model'].unique():
        model_data = actual_data[actual_data['Model'] == model]
        model_forecast = forecast_data[forecast_data['Model'] == model]
        
        if len(model_data) >= 2:
            # Hitung tren (bandingkan 3 tahun terakhir vs 3 tahun sebelumnya)
            sorted_data = model_data.sort_values('Year')
            recent_years = sorted_data.tail(3)['Price_USD'].mean()
            older_years = sorted_data.head(max(3, len(sorted_data)-3))['Price_USD'].mean()
            
            trend_pct = ((recent_years - older_years) / older_years * 100) if older_years > 0 else 0
            
            # Prediksi masa depan
            if not model_forecast.empty:
                future_price = model_forecast['Price_USD'].mean()
                current_price = recent_years
                future_trend_pct = ((future_price - current_price) / current_price * 100) if current_price > 0 else 0
            else:
                future_trend_pct = 0
            
            # Volatilitas (standar deviasi)
            volatility = model_data['Price_USD'].std()
            
            model_analysis.append({
                'model': model,
                'current_avg': recent_years,
                'trend_pct': trend_pct,
                'future_trend_pct': future_trend_pct,
                'volatility': volatility
            })
    
    if model_analysis:
        # Urutkan berdasarkan tren terbaik
        model_analysis.sort(key=lambda x: x['trend_pct'], reverse=True)
        best_model = model_analysis[0]
        worst_model = model_analysis[-1]
        
        # Cari model dengan future trend terbaik
        model_analysis_future = sorted(model_analysis, key=lambda x: x['future_trend_pct'], reverse=True)
        best_future_model = model_analysis_future[0]
        
        # Cari model paling stabil (volatilitas terendah)
        model_analysis_stable = sorted(model_analysis, key=lambda x: x['volatility'])
        most_stable_model = model_analysis_stable[0]
        
        # Layout 4 kolom untuk insight cards - format paragraf
        insight_cols = st.columns(4)
        
        # Card 1: Model Terbaik
        with insight_cols[0]:
            if best_model['trend_pct'] > 5:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                            padding: 20px; border-radius: 12px; 
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                            border-top: 4px solid #22c55e; height: 200px;'>
                    <p style='color: #15803d; margin: 0 0 12px 0; font-size: 14px; font-weight: 600; text-align: center;'>
                        📈 Model Terbaik
                    </p>
                    <p style='color: #166534; margin: 0; font-size: 14px; line-height: 1.7; text-align: justify;'>
                        <strong style='font-size: 18px; display: block; text-align: center; margin-bottom: 8px;'>{best_model['model']}</strong>
                        menunjukkan performa luar biasa dengan kenaikan <strong>{best_model['trend_pct']:.1f}%</strong> dalam beberapa tahun terakhir. 
                        Sangat cocok untuk investasi jangka panjang dengan potensi keuntungan yang menjanjikan.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            elif best_model['trend_pct'] > 0:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                            padding: 20px; border-radius: 12px; 
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                            border-top: 4px solid #3b82f6; height: 200px;'>
                    <p style='color: #1e40af; margin: 0 0 12px 0; font-size: 14px; font-weight: 600; text-align: center;'>
                        📊 Model Stabil
                    </p>
                    <p style='color: #1e3a8a; margin: 0; font-size: 14px; line-height: 1.7; text-align: justify;'>
                        <strong style='font-size: 18px; display: block; text-align: center; margin-bottom: 8px;'>{best_model['model']}</strong>
                        menunjukkan pertumbuhan stabil dengan kenaikan <strong>{best_model['trend_pct']:.1f}%</strong>. 
                        Pilihan yang aman dengan risiko rendah untuk investor yang mengutamakan stabilitas.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Card 2: Prediksi Masa Depan
        with insight_cols[1]:
            if best_future_model['future_trend_pct'] > 3:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                            padding: 20px; border-radius: 12px; 
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                            border-top: 4px solid #6366f1; height: 200px;'>
                    <p style='color: #3730a3; margin: 0 0 12px 0; font-size: 14px; font-weight: 600; text-align: center;'>
                        🔮 Prediksi Terbaik
                    </p>
                    <p style='color: #312e81; margin: 0; font-size: 14px; line-height: 1.7; text-align: justify;'>
                        <strong style='font-size: 18px; display: block; text-align: center; margin-bottom: 8px;'>{best_future_model['model']}</strong>
                        diprediksi mengalami kenaikan harga sebesar <strong>+{best_future_model['future_trend_pct']:.1f}%</strong> di masa depan. 
                        Ini adalah waktu yang tepat untuk membeli dengan potensi keuntungan tinggi.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            elif best_future_model['future_trend_pct'] < -3:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                            padding: 20px; border-radius: 12px; 
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                            border-top: 4px solid #ef4444; height: 200px;'>
                    <p style='color: #991b1b; margin: 0 0 12px 0; font-size: 14px; font-weight: 600; text-align: center;'>
                        ⚠️ Perhatian
                    </p>
                    <p style='color: #7f1d1d; margin: 0; font-size: 14px; line-height: 1.7; text-align: justify;'>
                        <strong style='font-size: 18px; display: block; text-align: center; margin-bottom: 8px;'>{best_future_model['model']}</strong>
                        diprediksi mengalami penurunan harga sekitar <strong>{best_future_model['future_trend_pct']:.1f}%</strong>. 
                        Pertimbangkan untuk menjual sekarang sebelum harga turun lebih jauh.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                            padding: 20px; border-radius: 12px; 
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                            border-top: 4px solid #6366f1; height: 200px;'>
                    <p style='color: #3730a3; margin: 0 0 12px 0; font-size: 14px; font-weight: 600; text-align: center;'>
                        📊 Stabilitas Harga
                    </p>
                    <p style='color: #312e81; margin: 0; font-size: 14px; line-height: 1.7; text-align: justify;'>
                        <strong style='font-size: 18px; display: block; text-align: center; margin-bottom: 8px;'>{best_future_model['model']}</strong>
                        diprediksi akan mempertahankan harga yang relatif stabil dengan perubahan <strong>{best_future_model['future_trend_pct']:+.1f}%</strong>. 
                        Cocok untuk strategi HOLD tanpa urgensi untuk membeli atau menjual.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Card 3: Model Paling Stabil
        with insight_cols[2]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                        padding: 20px; border-radius: 12px; 
                        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                        border-top: 4px solid #f59e0b; height: 200px;'>
                <p style='color: #92400e; margin: 0 0 12px 0; font-size: 14px; font-weight: 600; text-align: center;'>
                    🛡️ Paling Stabil
                </p>
                <p style='color: #78350f; margin: 0; font-size: 14px; line-height: 1.7; text-align: justify;'>
                    <strong style='font-size: 18px; display: block; text-align: center; margin-bottom: 8px;'>{most_stable_model['model']}</strong>
                    memiliki volatilitas harga terendah, artinya harga lebih konsisten dan dapat diprediksi. 
                    Ideal untuk investor yang menghindari fluktuasi harga yang ekstrem.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Card 4: Perbandingan Performa
        with insight_cols[3]:
            if len(model_analysis) > 1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); 
                            padding: 20px; border-radius: 12px; 
                            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                            border-top: 4px solid #ec4899; height: 200px;'>
                    <p style='color: #831843; margin: 0 0 12px 0; font-size: 14px; font-weight: 600; text-align: center;'>
                        ⚖️ Perbandingan
                    </p>
                    <p style='color: #831843; margin: 0; font-size: 14px; line-height: 1.7; text-align: justify;'>
                        Model terbaik <strong>{best_model['model']}</strong> tumbuh <strong style='color: #15803d;'>{best_model['trend_pct']:+.1f}%</strong>, 
                        sementara <strong>{worst_model['model']}</strong> hanya <strong style='color: #991b1b;'>{worst_model['trend_pct']:+.1f}%</strong>. 
                        Perbedaan performa yang signifikan menunjukkan pentingnya pemilihan model yang tepat.
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📊 Tidak cukup data untuk analisis mendalam. Pilih lebih banyak model atau tahun.")
else:
    st.info("📊 Tidak ada data aktual untuk analisis. Silakan sesuaikan filter.")

st.markdown('</div>', unsafe_allow_html=True)  # Tutup container analisis

# ========================================
# BARIS 5: BAR CHART & TABLE
# ========================================
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown("### 📊 Perbandingan Harga Per Model")

chart_col, table_col = st.columns([1, 1])

with chart_col:
    st.markdown("**Rata Rata Harga Per Model**")
    
    # Hitung rata-rata harga per model
    model_avg = filtered_df.groupby('Model')['Price_USD'].mean().reset_index()
    model_avg = model_avg.sort_values('Price_USD', ascending=True)
    
    # Konversi ke mata uang yang dipilih
    model_avg['Price_Converted'] = model_avg['Price_USD'].apply(
        lambda x: convert_currency(x, selected_currency)
    )
    
    # Buat bar chart horizontal
    fig_bar = px.bar(
        model_avg,
        y='Model',
        x='Price_Converted',
        orientation='h',
        labels={'Price_Converted': 'Harga Rata-rata', 'Model': 'Model'},
        template='plotly_white',
        color_discrete_sequence=['#3b82f6']
    )
    
    fig_bar.update_layout(
        height=400,
        font=dict(size=11),
        margin=dict(l=50, r=50, t=30, b=50),
        showlegend=False
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

with table_col:
    st.markdown("**Model**")
    
    # Buat tabel dengan rata-rata dan prediksi per model
    table_data = []
    
    for model in sorted(filtered_df['Model'].unique()):
        model_data = filtered_df[filtered_df['Model'] == model]
        
        # Harga rata-rata
        avg = model_data['Price_USD'].mean()
        
        # Prediksi harga (dari data forecast)
        forecast = model_data[model_data['Type'] == 'Forecast']
        if not forecast.empty:
            pred = forecast['Price_USD'].mean()
        else:
            pred = avg
        
        # Konversi ke mata uang yang dipilih
        avg_converted = convert_currency(avg, selected_currency)
        pred_converted = convert_currency(pred, selected_currency)
        
        table_data.append({
            'Model': model,
            'Harga Rata-rata': format_currency(avg_converted, selected_currency),
            'Prediksi Harga': format_currency(pred_converted, selected_currency)
        })
    
    # Tampilkan sebagai dataframe
    table_df = pd.DataFrame(table_data)
    
    # Tambahkan row "Total" di akhir
    total_avg = convert_currency(filtered_df['Price_USD'].mean(), selected_currency)
    total_pred = convert_currency(
        filtered_df[filtered_df['Type'] == 'Forecast']['Price_USD'].mean() 
        if not filtered_df[filtered_df['Type'] == 'Forecast'].empty 
        else filtered_df['Price_USD'].mean(),
        selected_currency
    )
    
    total_row = pd.DataFrame([{
        'Model': 'Total',
        'Harga Rata-rata': format_currency(total_avg, selected_currency),
        'Prediksi Harga': format_currency(total_pred, selected_currency)
    }])
    
    table_df = pd.concat([table_df, total_row], ignore_index=True)
    
    # Styling untuk tabel
    st.dataframe(
        table_df,
        use_container_width=True,
        height=400,
        hide_index=True
    )

st.markdown('</div>', unsafe_allow_html=True)  # Tutup container bar chart & table

# ========================================
# FOOTER
# ========================================
st.markdown("""
    <div style='text-align: center; color: #666; padding: 30px 20px; margin-top: 20px;'>
        <p>📊 Dashboard BMW Price Analysis | Dibuat dengan Streamlit & Plotly</p>
        <p>🎓 Proyek Sains Data - Teknik Informatika Semester 7</p>
    </div>
""", unsafe_allow_html=True)
