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
    /* Background dengan gradient subtle */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
    }
    
    /* Styling untuk metric cards */
    .stMetric {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.06);
        border: 1px solid rgba(59, 130, 246, 0.1);
        transition: transform 0.2s;
    }
    
    /* Kecilkan font value di metric */
    [data-testid="stMetricValue"] {
        font-size: 20px !important;
        font-weight: 600 !important;
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
    
    /* Decorative elements */
    .decoration-bar {
        height: 4px;
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        border-radius: 2px;
        margin: 10px 0 20px 0;
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
st.markdown("# Dashboard Pasar BMW: Analisis Harga & Prediksi Harga")
st.markdown('<div class="decoration-bar"></div>', unsafe_allow_html=True)

# ========================================
# LAYOUT: FILTERS DI KANAN ATAS
# ========================================
col_left, col_right = st.columns([3, 1])

with col_right:
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    
    # Filter Jenis Transmisi (dengan tombol)
    st.markdown("**Jenis Transmisi**")
    transmission_cols = st.columns(2)
    
    # Hitung jumlah data per transmisi
    auto_count = len(df[df['Transmission'] == 'Automatic'])
    manual_count = len(df[df['Transmission'] == 'Manual'])
    
    with transmission_cols[0]:
        auto_selected = st.checkbox(f"Automatic\n{auto_count}", value=True, key="auto")
    with transmission_cols[1]:
        manual_selected = st.checkbox(f"Manual\n{manual_count}", value=True, key="manual")
    
    st.markdown("---")
    
    # Filter Mata Uang
    st.markdown("**Mata uang**")
    currency_options = ['Euro', 'Rupiah', 'US Dollar']
    selected_currency = st.radio(
        "",
        currency_options,
        index=2,  # Default US Dollar
        key="currency",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Filter Tahun
    st.markdown("**Tahun**")
    year_options = ['All'] + sorted(df['Year'].unique().tolist(), reverse=True)
    selected_year = st.selectbox(
        "",
        year_options,
        index=0,
        key="year",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Filter Model (Multiselect)
    st.markdown("**Model**")
    all_models = sorted(df['Model'].unique().tolist())
    selected_models = st.multiselect(
        "",
        all_models,
        default=all_models,  # Default: semua model dipilih
        key="model",
        label_visibility="collapsed",
        placeholder="Pilih model..."
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

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
# BAGIAN 1: KPI METRICS
# ========================================
with col_left:
    # Hitung metrics
    min_price = filtered_df['Price_USD'].min()
    max_price = filtered_df['Price_USD'].max()
    avg_price = filtered_df['Price_USD'].mean()
    
    # Hitung prediksi harga (rata-rata dari data forecast)
    forecast_data = filtered_df[filtered_df['Type'] == 'Forecast']
    if not forecast_data.empty:
        predicted_price = forecast_data['Price_USD'].mean()
    else:
        predicted_price = avg_price
    
    # Konversi ke mata uang yang dipilih
    min_price_converted = convert_currency(min_price, selected_currency)
    max_price_converted = convert_currency(max_price, selected_currency)
    avg_price_converted = convert_currency(avg_price, selected_currency)
    predicted_price_converted = convert_currency(predicted_price, selected_currency)
    
    # Tampilkan 4 KPI Cards
    kpi_cols = st.columns(4)
    
    with kpi_cols[0]:
        st.metric(
            label="Harga Minimal",
            value=format_currency(min_price_converted, selected_currency)
        )
    
    with kpi_cols[1]:
        st.metric(
            label="Harga Maksimal",
            value=format_currency(max_price_converted, selected_currency)
        )
    
    with kpi_cols[2]:
        st.metric(
            label="Harga Rata-rata",
            value=format_currency(avg_price_converted, selected_currency)
        )
    
    with kpi_cols[3]:
        st.metric(
            label="Prediksi Harga",
            value=format_currency(predicted_price_converted, selected_currency)
        )
    
    
    # ========================================
    # BAGIAN 2: LINE CHART - RATA-RATA HARGA PER TAHUN
    # ========================================
    st.markdown("**Rata-rata harga mobil per tahun**")
    
    # Hitung rata-rata harga per tahun per model
    trend_data = filtered_df.groupby(['Year', 'Model'])['Price_USD'].mean().reset_index()
    
    # Konversi ke mata uang yang dipilih
    trend_data['Price_Converted'] = trend_data['Price_USD'].apply(
        lambda x: convert_currency(x, selected_currency)
    )
    
    # Buat line chart
    fig_line = px.line(
        trend_data,
        x='Year',
        y='Price_Converted',
        color='Model',
        markers=True,
        labels={'Price_Converted': 'Harga Rata-rata', 'Year': 'Tahun'},
        template='plotly_white'
    )
    
    fig_line.update_traces(line=dict(width=2), marker=dict(size=6))
    fig_line.update_layout(
        hovermode='x unified',
        height=350,
        font=dict(size=11),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=50, t=30, b=80),
        showlegend=True
    )
    
    st.plotly_chart(fig_line, use_container_width=True)

# ========================================
# BAGIAN 3: STORYTELLING & ANALISIS
# ========================================
st.markdown("---")
st.markdown('<div class="decoration-bar"></div>', unsafe_allow_html=True)
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
        
        # Layout 2 kolom untuk insight cards
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            # Card 1: Model Terbaik
            if best_model['trend_pct'] > 5:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                            padding: 25px; border-radius: 15px; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            border-left: 5px solid #22c55e; margin-bottom: 20px;'>
                    <h3 style='color: #15803d; margin-top: 0;'>📈 Model Terbaik</h3>
                    <h2 style='color: #166534; margin: 10px 0;'>{best_model['model']}</h2>
                    <p style='font-size: 16px; color: #166534; line-height: 1.6;'>
                        Performa luar biasa dengan kenaikan <strong>{best_model['trend_pct']:.1f}%</strong> 
                        dalam beberapa tahun terakhir.
                    </p>
                    <p style='font-size: 18px; font-weight: 600; color: #15803d; margin: 15px 0;'>
                        Harga saat ini: {format_currency(convert_currency(best_model['current_avg'], selected_currency), selected_currency)}
                    </p>
                    <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-top: 15px;'>
                        <p style='margin: 0; color: #166534; font-weight: 500;'>
                            ✅ <strong>Rekomendasi:</strong> Sangat bagus untuk investasi jangka panjang. 
                            Tren menunjukkan permintaan tinggi dan nilai yang terus meningkat.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif best_model['trend_pct'] > 0:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                            padding: 25px; border-radius: 15px; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            border-left: 5px solid #3b82f6; margin-bottom: 20px;'>
                    <h3 style='color: #1e40af; margin-top: 0;'>📊 Model Stabil</h3>
                    <h2 style='color: #1e3a8a; margin: 10px 0;'>{best_model['model']}</h2>
                    <p style='font-size: 16px; color: #1e3a8a; line-height: 1.6;'>
                        Pertumbuhan stabil dengan kenaikan <strong>{best_model['trend_pct']:.1f}%</strong>.
                    </p>
                    <p style='font-size: 18px; font-weight: 600; color: #1e40af; margin: 15px 0;'>
                        Harga saat ini: {format_currency(convert_currency(best_model['current_avg'], selected_currency), selected_currency)}
                    </p>
                    <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-top: 15px;'>
                        <p style='margin: 0; color: #1e3a8a; font-weight: 500;'>
                            ✅ <strong>Rekomendasi:</strong> Cocok untuk investasi yang aman dengan risiko rendah.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Card 3: Model Paling Stabil
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                        padding: 25px; border-radius: 15px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        border-left: 5px solid #f59e0b; margin-bottom: 20px;'>
                <h3 style='color: #92400e; margin-top: 0;'>🛡️ Model Paling Stabil</h3>
                <h2 style='color: #78350f; margin: 10px 0;'>{most_stable_model['model']}</h2>
                <p style='font-size: 16px; color: #78350f; line-height: 1.6;'>
                    Volatilitas harga terendah - harga lebih konsisten dan dapat diprediksi.
                </p>
                <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-top: 15px;'>
                    <p style='margin: 0; color: #78350f; font-weight: 500;'>
                        ✅ <strong>Keuntungan:</strong> Jika Anda membeli dan menjual kembali, 
                        harga tidak akan turun terlalu jauh karena permintaan pasar yang stabil.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col2:
            # Card 2: Prediksi Masa Depan
            if best_future_model['future_trend_pct'] > 3:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                            padding: 25px; border-radius: 15px; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            border-left: 5px solid #6366f1; margin-bottom: 20px;'>
                    <h3 style='color: #3730a3; margin-top: 0;'>🔮 Prediksi Terbaik</h3>
                    <h2 style='color: #312e81; margin: 10px 0;'>{best_future_model['model']}</h2>
                    <p style='font-size: 16px; color: #312e81; line-height: 1.6;'>
                        Diprediksi mengalami kenaikan harga sebesar <strong>{best_future_model['future_trend_pct']:.1f}%</strong> 
                        di masa depan.
                    </p>
                    <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-top: 15px;'>
                        <p style='margin: 0; color: #312e81; font-weight: 500;'>
                            💡 <strong>Strategi:</strong> Waktu yang <strong>TEPAT UNTUK MEMBELI</strong>! 
                            Jika Anda membeli sekarang dan menjual kembali dalam 2-3 tahun, 
                            potensi keuntungan sangat tinggi dengan risiko penurunan harga yang minimal.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif best_future_model['future_trend_pct'] < -3:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                            padding: 25px; border-radius: 15px; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            border-left: 5px solid #ef4444; margin-bottom: 20px;'>
                    <h3 style='color: #991b1b; margin-top: 0;'>⚠️ Perhatian</h3>
                    <h2 style='color: #7f1d1d; margin: 10px 0;'>{best_future_model['model']}</h2>
                    <p style='font-size: 16px; color: #7f1d1d; line-height: 1.6;'>
                        Diprediksi mengalami penurunan harga sekitar <strong>{abs(best_future_model['future_trend_pct']):.1f}%</strong> 
                        di masa depan.
                    </p>
                    <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-top: 15px;'>
                        <p style='margin: 0; color: #7f1d1d; font-weight: 500;'>
                            💡 <strong>Strategi:</strong> Jika Anda memiliki model ini, 
                            pertimbangkan untuk <strong>MENJUAL SEKARANG</strong> sebelum harga turun lebih jauh.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); 
                            padding: 25px; border-radius: 15px; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            border-left: 5px solid #6366f1; margin-bottom: 20px;'>
                    <h3 style='color: #3730a3; margin-top: 0;'>📊 Stabilitas Harga</h3>
                    <h2 style='color: #312e81; margin: 10px 0;'>{best_future_model['model']}</h2>
                    <p style='font-size: 16px; color: #312e81; line-height: 1.6;'>
                        Diprediksi akan mempertahankan harga yang relatif stabil 
                        (perubahan: <strong>{best_future_model['future_trend_pct']:+.1f}%</strong>).
                    </p>
                    <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-top: 15px;'>
                        <p style='margin: 0; color: #312e81; font-weight: 500;'>
                            💡 <strong>Strategi:</strong> Model ini cocok untuk <strong>HOLD</strong> (tahan). 
                            Tidak ada urgensi untuk membeli atau menjual.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Card 4: Perbandingan Performa
            if len(model_analysis) > 1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); 
                            padding: 25px; border-radius: 15px; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            border-left: 5px solid #ec4899; margin-bottom: 20px;'>
                    <h3 style='color: #831843; margin-top: 0;'>⚖️ Perbandingan Performa</h3>
                    <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-top: 15px;'>
                        <p style='margin: 5px 0; color: #831843; font-size: 15px;'>
                            <strong>🏆 Terbaik:</strong> {best_model['model']} 
                            <span style='color: #15803d; font-weight: 600;'>({best_model['trend_pct']:+.1f}%)</span>
                        </p>
                        <p style='margin: 5px 0; color: #831843; font-size: 15px;'>
                            <strong>📉 Terlemah:</strong> {worst_model['model']} 
                            <span style='color: #991b1b; font-weight: 600;'>({worst_model['trend_pct']:+.1f}%)</span>
                        </p>
                        <p style='margin: 5px 0; color: #831843; font-size: 15px;'>
                            <strong>📊 Selisih:</strong> {abs(best_model['trend_pct'] - worst_model['trend_pct']):.1f}%
                        </p>
                    </div>
                    <div style='background-color: rgba(255,255,255,0.7); padding: 15px; border-radius: 10px; margin-top: 15px;'>
                        <p style='margin: 0; color: #831843; font-weight: 500;'>
                            💡 <strong>Kesimpulan:</strong> Ada perbedaan signifikan dalam performa antar model. 
                            Pilih model dengan cermat berdasarkan tujuan investasi Anda.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📊 Tidak cukup data untuk analisis mendalam. Pilih lebih banyak model atau tahun.")
else:
    st.info("📊 Tidak ada data aktual untuk analisis. Silakan sesuaikan filter.")

# ========================================
# BAGIAN 4: BAR CHART & TABLE
# ========================================
st.markdown("---")

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

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>📊 Dashboard BMW Price Analysis | Dibuat dengan Streamlit & Plotly</p>
        <p>🎓 Proyek Sains Data - Teknik Informatika Semester 7</p>
    </div>
""", unsafe_allow_html=True)
