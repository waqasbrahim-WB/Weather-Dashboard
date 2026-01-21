import streamlit as st
from datetime import datetime, timedelta
import random

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header */
    .weather-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .weather-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .weather-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-size: 1.2rem;
    }
    
    /* Current weather card */
    .current-weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        padding: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        margin-bottom: 1.5rem;
    }
    
    .temp-display {
        font-size: 5rem;
        font-weight: 700;
        line-height: 1;
        margin: 1rem 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    
    .weather-emoji {
        font-size: 6rem;
        text-align: center;
        margin: 1rem 0;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }
    
    .weather-desc {
        font-size: 1.5rem;
        text-transform: capitalize;
        opacity: 0.95;
        margin-bottom: 1rem;
    }
    
    .weather-detail {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .weather-detail-label {
        font-size: 0.9rem;
        opacity: 0.85;
        margin-bottom: 0.25rem;
    }
    
    .weather-detail-value {
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* City card */
    .city-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        cursor: pointer;
        height: 100%;
    }
    
    .city-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .city-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }
    
    .city-name {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .city-temp {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .city-condition {
        color: #6b7280;
        font-size: 1rem;
    }
    
    /* Forecast card */
    .forecast-card {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .forecast-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        border-color: #667eea;
    }
    
    .forecast-day {
        font-size: 1.1rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    
    .forecast-emoji {
        font-size: 3rem;
        margin: 0.5rem 0;
    }
    
    .forecast-temp {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .forecast-minmax {
        font-size: 0.9rem;
        color: #6b7280;
    }
    
    /* Alert card */
    .alert-card {
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .alert-warning {
        background: #fef3c7;
        border-color: #f59e0b;
        color: #92400e;
    }
    
    .alert-danger {
        background: #fee2e2;
        border-color: #ef4444;
        color: #991b1b;
    }
    
    .alert-info {
        background: #dbeafe;
        border-color: #3b82f6;
        color: #1e40af;
    }
    
    .alert-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .alert-message {
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Stats card */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.25rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Hourly forecast */
    .hourly-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        min-width: 100px;
    }
    
    .hourly-time {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .hourly-emoji {
        font-size: 2rem;
        margin: 0.5rem 0;
    }
    
    .hourly-temp {
        font-size: 1.3rem;
        font-weight: 600;
        color: #374151;
    }
    
    /* Search box */
    .search-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f3f4f6;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# WEATHER DATA & UTILITIES
# ============================================================================

# Weather conditions mapping
WEATHER_CONDITIONS = {
    "Clear": {"emoji": "☀️", "desc": "Clear Sky"},
    "Clouds": {"emoji": "☁️", "desc": "Cloudy"},
    "Rain": {"emoji": "🌧️", "desc": "Rainy"},
    "Drizzle": {"emoji": "🌦️", "desc": "Light Rain"},
    "Thunderstorm": {"emoji": "⛈️", "desc": "Thunderstorm"},
    "Snow": {"emoji": "❄️", "desc": "Snowy"},
    "Mist": {"emoji": "🌫️", "desc": "Misty"},
    "Fog": {"emoji": "🌫️", "desc": "Foggy"},
    "Haze": {"emoji": "🌫️", "desc": "Hazy"},
}

# Major cities with coordinates
CITIES = {
    "Karachi": {"country": "Pakistan", "lat": 24.8607, "lon": 67.0011},
    "Lahore": {"country": "Pakistan", "lat": 31.5204, "lon": 74.3587},
    "Islamabad": {"country": "Pakistan", "lat": 33.6844, "lon": 73.0479},
    "New York": {"country": "USA", "lat": 40.7128, "lon": -74.0060},
    "London": {"country": "UK", "lat": 51.5074, "lon": -0.1278},
    "Tokyo": {"country": "Japan", "lat": 35.6762, "lon": 139.6503},
    "Dubai": {"country": "UAE", "lat": 25.2048, "lon": 55.2708},
    "Paris": {"country": "France", "lat": 48.8566, "lon": 2.3522},
    "Sydney": {"country": "Australia", "lat": -33.8688, "lon": 151.2093},
    "Mumbai": {"country": "India", "lat": 19.0760, "lon": 72.8777},
}

def generate_mock_weather(city_name):
    """Generate realistic mock weather data"""
    base_temps = {
        "Karachi": 28, "Lahore": 25, "Islamabad": 22,
        "New York": 15, "London": 12, "Tokyo": 18,
        "Dubai": 32, "Paris": 14, "Sydney": 22, "Mumbai": 29
    }
    
    base_temp = base_temps.get(city_name, 20)
    temp_variation = random.uniform(-3, 3)
    temp = round(base_temp + temp_variation, 1)
    
    conditions = list(WEATHER_CONDITIONS.keys())
    weights = [0.35, 0.25, 0.15, 0.08, 0.05, 0.05, 0.04, 0.02, 0.01]
    condition = random.choices(conditions, weights=weights)[0]
    
    return {
        "city": city_name,
        "country": CITIES[city_name]["country"],
        "temp": temp,
        "feels_like": round(temp + random.uniform(-2, 2), 1),
        "temp_min": round(temp - random.uniform(3, 5), 1),
        "temp_max": round(temp + random.uniform(3, 5), 1),
        "condition": condition,
        "description": WEATHER_CONDITIONS[condition]["desc"],
        "emoji": WEATHER_CONDITIONS[condition]["emoji"],
        "humidity": random.randint(40, 90),
        "wind_speed": round(random.uniform(5, 25), 1),
        "pressure": random.randint(1005, 1025),
        "visibility": round(random.uniform(5, 10), 1),
        "clouds": random.randint(0, 100),
        "sunrise": "06:30 AM",
        "sunset": "06:45 PM",
        "uv_index": random.randint(1, 11),
        "air_quality": random.choice(["Good", "Moderate", "Unhealthy"]),
    }

def generate_forecast(city_name, days=5):
    """Generate multi-day forecast"""
    forecast = []
    base_weather = generate_mock_weather(city_name)
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i+1)
        day_name = date.strftime("%A")
        
        temp_variation = random.uniform(-4, 4)
        temp = round(base_weather["temp"] + temp_variation, 1)
        
        condition = random.choice(list(WEATHER_CONDITIONS.keys()))
        
        forecast.append({
            "day": day_name,
            "date": date.strftime("%b %d"),
            "temp": temp,
            "temp_min": round(temp - random.uniform(3, 6), 1),
            "temp_max": round(temp + random.uniform(3, 6), 1),
            "condition": condition,
            "emoji": WEATHER_CONDITIONS[condition]["emoji"],
            "description": WEATHER_CONDITIONS[condition]["desc"],
            "precipitation": random.randint(0, 80),
            "wind_speed": round(random.uniform(5, 20), 1),
        })
    
    return forecast

def generate_hourly_forecast(city_name):
    """Generate hourly forecast for next 12 hours"""
    hourly = []
    base_weather = generate_mock_weather(city_name)
    current_hour = datetime.now().hour
    
    for i in range(12):
        hour = (current_hour + i) % 24
        hour_str = f"{hour:02d}:00"
        
        temp_variation = random.uniform(-2, 2)
        temp = round(base_weather["temp"] + temp_variation, 1)
        
        condition = random.choice(list(WEATHER_CONDITIONS.keys()))
        
        hourly.append({
            "time": hour_str,
            "temp": temp,
            "emoji": WEATHER_CONDITIONS[condition]["emoji"],
            "condition": condition,
        })
    
    return hourly

def generate_weather_alerts(city_name):
    """Generate weather alerts"""
    alerts = []
    
    weather = generate_mock_weather(city_name)
    
    # Temperature alerts
    if weather["temp"] > 35:
        alerts.append({
            "type": "danger",
            "icon": "🔥",
            "title": "Heat Wave Warning",
            "message": f"Extreme heat expected. Temperature may reach {weather['temp_max']}°C. Stay hydrated and avoid outdoor activities."
        })
    elif weather["temp"] < 5:
        alerts.append({
            "type": "warning",
            "icon": "🥶",
            "title": "Cold Weather Advisory",
            "message": f"Very cold temperatures expected. Dress warmly and protect against frostbite."
        })
    
    # Condition alerts
    if weather["condition"] == "Thunderstorm":
        alerts.append({
            "type": "danger",
            "icon": "⛈️",
            "title": "Severe Thunderstorm Warning",
            "message": "Strong thunderstorms expected. Seek shelter immediately. Avoid outdoor activities."
        })
    elif weather["condition"] == "Rain":
        alerts.append({
            "type": "warning",
            "icon": "🌧️",
            "title": "Heavy Rain Alert",
            "message": "Heavy rainfall expected. Possible flooding in low-lying areas. Drive carefully."
        })
    
    # Wind alerts
    if weather["wind_speed"] > 40:
        alerts.append({
            "type": "warning",
            "icon": "💨",
            "title": "High Wind Warning",
            "message": f"Strong winds expected up to {weather['wind_speed']} km/h. Secure outdoor objects."
        })
    
    # UV alerts
    if weather["uv_index"] >= 8:
        alerts.append({
            "type": "info",
            "icon": "☀️",
            "title": "High UV Index",
            "message": f"UV Index: {weather['uv_index']}. Wear sunscreen and protective clothing."
        })
    
    # Air quality alerts
    if weather["air_quality"] == "Unhealthy":
        alerts.append({
            "type": "warning",
            "icon": "😷",
            "title": "Air Quality Alert",
            "message": "Air quality is unhealthy. People with respiratory issues should stay indoors."
        })
    
    return alerts

# ============================================================================
# SESSION STATE
# ============================================================================
def init_session_state():
    if 'selected_city' not in st.session_state:
        st.session_state.selected_city = "Karachi"
    if 'favorite_cities' not in st.session_state:
        st.session_state.favorite_cities = ["Karachi", "Lahore", "Islamabad"]
    if 'temp_unit' not in st.session_state:
        st.session_state.temp_unit = "Celsius"

def celsius_to_fahrenheit(celsius):
    return round((celsius * 9/5) + 32, 1)

def get_display_temp(temp):
    if st.session_state.temp_unit == "Fahrenheit":
        return f"{celsius_to_fahrenheit(temp)}°F"
    return f"{temp}°C"

# ============================================================================
# UI COMPONENTS
# ============================================================================
def render_header():
    current_time = datetime.now().strftime("%A, %B %d, %Y • %I:%M %p")
    st.markdown(f"""
    <div class="weather-header">
        <h1>🌦️ Weather Dashboard</h1>
        <p>{current_time}</p>
    </div>
    """, unsafe_allow_html=True)

def render_current_weather(weather):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="current-weather-card">
            <h2 style="margin: 0; font-size: 2rem;">📍 {weather['city']}, {weather['country']}</h2>
            <div class="weather-desc">{weather['description']}</div>
            <div class="temp-display">{get_display_temp(weather['temp'])}</div>
            <p style="font-size: 1.1rem; margin: 0; opacity: 0.9;">Feels like {get_display_temp(weather['feels_like'])}</p>
            <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.85;">
                H: {get_display_temp(weather['temp_max'])} • L: {get_display_temp(weather['temp_min'])}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="current-weather-card" style="display: flex; align-items: center; justify-content: center;">
            <div class="weather-emoji">{weather['emoji']}</div>
        </div>
        """, unsafe_allow_html=True)

def render_weather_details(weather):
    st.markdown("### 📊 Weather Details")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">💧</div>
            <div class="stat-value">{weather['humidity']}%</div>
            <div class="stat-label">Humidity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">💨</div>
            <div class="stat-value">{weather['wind_speed']}</div>
            <div class="stat-label">Wind (km/h)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🌡️</div>
            <div class="stat-value">{weather['pressure']}</div>
            <div class="stat-label">Pressure (hPa)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">👁️</div>
            <div class="stat-value">{weather['visibility']}</div>
            <div class="stat-label">Visibility (km)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">☁️</div>
            <div class="stat-value">{weather['clouds']}%</div>
            <div class="stat-label">Cloudiness</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🌅</div>
            <div class="stat-value">{weather['sunrise']}</div>
            <div class="stat-label">Sunrise</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🌇</div>
            <div class="stat-value">{weather['sunset']}</div>
            <div class="stat-label">Sunset</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        uv_color = "#10b981" if weather['uv_index'] < 3 else "#f59e0b" if weather['uv_index'] < 8 else "#ef4444"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">☀️</div>
            <div class="stat-value" style="color: {uv_color};">{weather['uv_index']}</div>
            <div class="stat-label">UV Index</div>
        </div>
        """, unsafe_allow_html=True)

def render_hourly_forecast(city_name):
    st.markdown("### ⏰ Hourly Forecast")
    hourly = generate_hourly_forecast(city_name)
    
    cols = st.columns(6)
    for idx, hour_data in enumerate(hourly[:6]):
        with cols[idx]:
            st.markdown(f"""
            <div class="hourly-card">
                <div class="hourly-time">{hour_data['time']}</div>
                <div class="hourly-emoji">{hour_data['emoji']}</div>
                <div class="hourly-temp">{get_display_temp(hour_data['temp'])}</div>
            </div>
            """, unsafe_allow_html=True)

def render_forecast(city_name):
    st.markdown("### 📅 5-Day Forecast")
    forecast = generate_forecast(city_name)
    
    cols = st.columns(5)
    for idx, day_data in enumerate(forecast):
        with cols[idx]:
            st.markdown(f"""
            <div class="forecast-card">
                <div class="forecast-day">{day_data['day']}</div>
                <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem;">{day_data['date']}</div>
                <div class="forecast-emoji">{day_data['emoji']}</div>
                <div class="forecast-temp">{get_display_temp(day_data['temp'])}</div>
                <div class="forecast-minmax">
                    ↑ {get_display_temp(day_data['temp_max'])} ↓ {get_display_temp(day_data['temp_min'])}
                </div>
                <div style="font-size: 0.85rem; color: #6b7280; margin-top: 0.5rem;">
                    💧 {day_data['precipitation']}%
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_weather_alerts(city_name):
    alerts = generate_weather_alerts(city_name)
    
    if alerts:
        st.markdown("### ⚠️ Weather Alerts")
        for alert in alerts:
            st.markdown(f"""
            <div class="alert-card alert-{alert['type']}">
                <div class="alert-title">
                    <span>{alert['icon']}</span>
                    <span>{alert['title']}</span>
                </div>
                <div class="alert-message">{alert['message']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No weather alerts for this location")

def render_city_comparison():
    st.markdown("### 🌍 Multi-City Comparison")
    
    cities_to_compare = st.session_state.favorite_cities
    
    cols = st.columns(len(cities_to_compare))
    for idx, city in enumerate(cities_to_compare):
        with cols[idx]:
            weather = generate_mock_weather(city)
            is_selected = city == st.session_state.selected_city
            
            st.markdown(f"""
            <div class="city-card {'selected' if is_selected else ''}">
                <div class="city-name">📍 {city}</div>
                <div style="font-size: 3rem; text-align: center; margin: 0.5rem 0;">
                    {weather['emoji']}
                </div>
                <div class="city-temp">{get_display_temp(weather['temp'])}</div>
                <div class="city-condition">{weather['description']}</div>
                <div style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">
                    H: {get_display_temp(weather['temp_max'])} • L: {get_display_temp(weather['temp_min'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("View Details", key=f"view_{city}", use_container_width=True):
                st.session_state.selected_city = city
                st.rerun()

def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # Temperature unit
        st.session_state.temp_unit = st.radio(
            "Temperature Unit",
            ["Celsius", "Fahrenheit"],
            index=0 if st.session_state.temp_unit == "Celsius" else 1
        )
        
        st.markdown("---")
        
        # City selector
        st.markdown("## 🌍 Select City")
        selected = st.selectbox(
            "Choose a city",
            list(CITIES.keys()),
            index=list(CITIES.keys()).index(st.session_state.selected_city)
        )
        
        if selected != st.session_state.selected_city:
            st.session_state.selected_city = selected
            st.rerun()
        
        st.markdown("---")
        
        # Favorite cities
        st.markdown("## ⭐ Favorite Cities")
        st.markdown("*Manage your favorite cities for quick access*")
        
        for city in st.session_state.favorite_cities:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📍 {city}")
            with col2:
                if st.button("❌", key=f"remove_{city}", help="Remove"):
                    st.session_state.favorite_cities.remove(city)
                    st.rerun()
        
        # Add city
        st.markdown("**Add New City**")
        available_cities = [c for c in CITIES.keys() if c not in st.session_state.favorite_cities]
        if available_cities:
            new_city = st.selectbox("Select city to add", available_cities, key="add_city_select")
            if st.button("➕ Add to Favorites", use_container_width=True):
                st.session_state.favorite_cities.append(new_city)
                st.toast(f"✅ {new_city} added to favorites!")
                st.rerun()
        else:
            st.info("All cities are already in favorites!")
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("## 📊 Quick Stats")
        weather = generate_mock_weather(st.session_state.selected_city)
        
        st.metric("Current Temperature", get_display_temp(weather['temp']), 
                 f"{weather['temp'] - weather['temp_min']:.1f}° from low")
        st.metric("Humidity", f"{weather['humidity']}%")
        st.metric("Wind Speed", f"{weather['wind_speed']} km/h")
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
            st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    init_session_state()
    
    render_header()
    render_sidebar()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Current Weather", "📅 Forecast", "⚠️ Alerts", "🌍 Compare Cities"])
    
    with tab1:
        weather = generate_mock_weather(st.session_state.selected_city)
        
        render_current_weather(weather)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_weather_details(weather)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_hourly_forecast(st.session_state.selected_city)
    
    with tab2:
        render_forecast(st.session_state.selected_city)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Additional forecast details
        st.markdown("### 📈 Detailed Forecast Analysis")
        forecast_data = generate_forecast(st.session_state.selected_city)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌡️ Temperature Trend**")
            for day in forecast_data:
                st.write(f"**{day['day']}**: {get_display_temp(day['temp'])} ({day['description']})")
        
        with col2:
            st.markdown("**💧 Precipitation Chance**")
            for day in forecast_data:
                st.progress(day['precipitation'] / 100)
                st.write(f"{day['day']}: {day['precipitation']}% chance")
    
    with tab3:
        render_weather_alerts(st.session_state.selected_city)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Safety tips
        st.markdown("### 💡 Weather Safety Tips")
        
        weather = generate_mock_weather(st.session_state.selected_city)
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.info("""
            **General Safety:**
            - Check weather before outdoor activities
            - Keep emergency kit ready
            - Stay informed about weather changes
            - Have backup plans for severe weather
            """)
        
        with tips_col2:
            if weather['temp'] > 30:
                st.warning("""
                **Heat Safety:**
                - Stay hydrated
                - Avoid midday sun
                - Wear light clothing
                - Check on elderly neighbors
                """)
            elif weather['temp'] < 10:
                st.warning("""
                **Cold Safety:**
                - Dress in layers
                - Protect extremities
                - Limit outdoor exposure
                - Check heating systems
                """)
            else:
                st.success("""
                **Comfortable Weather:**
                - Perfect for outdoor activities
                - Enjoy the pleasant conditions
                - Stay active and healthy
                - Make the most of good weather
                """)
    
    with tab4:
        render_city_comparison()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # World weather highlights
        st.markdown("### 🌏 Global Weather Highlights")
        
        all_cities_weather = {city: generate_mock_weather(city) for city in CITIES.keys()}
        
        # Find extremes
        hottest_city = max(all_cities_weather.items(), key=lambda x: x[1]['temp'])
        coldest_city = min(all_cities_weather.items(), key=lambda x: x[1]['temp'])
        windiest_city = max(all_cities_weather.items(), key=lambda x: x[1]['wind_speed'])
        most_humid = max(all_cities_weather.items(), key=lambda x: x[1]['humidity'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">Hottest</div>
                <div style="font-size: 1rem; color: #6b7280;">{hottest_city[0]}</div>
                <div class="stat-value">{get_display_temp(hottest_city[1]['temp'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🥶</div>
                <div style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">Coldest</div>
                <div style="font-size: 1rem; color: #6b7280;">{coldest_city[0]}</div>
                <div class="stat-value">{get_display_temp(coldest_city[1]['temp'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">💨</div>
                <div style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">Windiest</div>
                <div style="font-size: 1rem; color: #6b7280;">{windiest_city[0]}</div>
                <div class="stat-value">{windiest_city[1]['wind_speed']} km/h</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">💧</div>
                <div style="font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">Most Humid</div>
                <div style="font-size: 1rem; color: #6b7280;">{most_humid[0]}</div>
                <div class="stat-value">{most_humid[1]['humidity']}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 1rem;">
        <p style="margin: 0;">🌦️ Weather Dashboard • Real-time weather information at your fingertips</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Data refreshes automatically • Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%I:%M %p")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
