import streamlit as st
import openrouteservice as ors
from openrouteservice import convert
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Route Planning Agent",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input {
        border-radius: 4px;
        padding: 0.5rem;
    }
    .metric-card {
        background-color: #23272f;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.12);
        border: 1px solid #222831;
    }
    .route-details {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 1rem 0;
        color: #222;
        display: flex;
        align-items: center;
    }
    .step-badge {
        background: #4CAF50;
        color: #fff;
        border-radius: 50%;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
        font-size: 1.1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize the OpenRouteService client
ors_client = ors.Client(key=os.getenv('ORS_API_KEY'))

def geocode_location(location_name):
    """Convert location name to coordinates using Nominatim."""
    try:
        geolocator = Nominatim(user_agent="route_planning_agent", timeout=10)
        location = geolocator.geocode(location_name)
        if location:
            return [location.longitude, location.latitude]
        return None
    except GeocoderTimedOut:
        st.error("Geocoding service timed out. Please try again.")
        return None

def get_route(start_coords, end_coords):
    """Get route between two coordinates using OpenRouteService."""
    try:
        routes = ors_client.directions(
            coordinates=[start_coords, end_coords],
            profile='driving-car',
            format='geojson'
        )
        return routes
    except Exception as e:
        st.error(f"Error getting route: {str(e)}")
        return None

def create_route_map(route):
    """Create a folium map with the route."""
    coordinates = route['features'][0]['geometry']['coordinates']
    center_lat = sum(coord[1] for coord in coordinates) / len(coordinates)
    center_lon = sum(coord[0] for coord in coordinates) / len(coordinates)
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles='CartoDB positron')
    
    # Add the route to the map
    folium.GeoJson(
        route,
        name='route',
        style_function=lambda x: {'color': '#4CAF50', 'weight': 4, 'opacity': 0.8}
    ).add_to(m)
    
    # Add markers for start and end points
    start_coords = coordinates[0]
    end_coords = coordinates[-1]
    
    folium.Marker(
        [start_coords[1], start_coords[0]],
        popup='Start',
        icon=folium.Icon(color='green', icon='play', prefix='fa')
    ).add_to(m)
    
    folium.Marker(
        [end_coords[1], end_coords[0]],
        popup='End',
        icon=folium.Icon(color='red', icon='flag-checkered', prefix='fa')
    ).add_to(m)
    
    return m

def main():
    # Header
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #1E88E5; margin-bottom: 1rem;'>🗺️ Route Planning Agent</h1>
            <p style='color: #666; font-size: 1.1rem;'>Plan your journey with ease and precision</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section with a clean card-like design
    with st.container():
       
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_location = st.text_input("📍 Starting Point", "San Francisco, CA")
        with col2:
            end_location = st.text_input("🎯 Destination", "Los Angeles, CA")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚗 Get Route", use_container_width=True):
        with st.spinner("Calculating your route..."):
            # Convert locations to coordinates
            start_coords = geocode_location(start_location)
            end_coords = geocode_location(end_location)
            
            if start_coords and end_coords:
                # Get the route
                route = get_route(start_coords, end_coords)
                
                if route:
                    # Display the map
                    st.markdown("### 🗺️ Route Map")
                    route_map = create_route_map(route)
                    folium_static(route_map, width=1000, height=500)
                    
                    # Display route details in a card
                    st.markdown("### 📊 Route Details")
                    distance = route['features'][0]['properties']['segments'][0]['distance']
                    duration = route['features'][0]['properties']['segments'][0]['duration']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <h3 style='color: #e0e0e0; font-weight: 600;'>Distance</h3>
                                <h2 style='color: #4CAF50;'>{distance/1000:.2f} km</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <h3 style='color: #e0e0e0; font-weight: 600;'>Duration</h3>
                                <h2 style='color: #4CAF50;'>{duration/3600:.2f} hours</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Display turn-by-turn directions
                    st.markdown("### 🚦 Turn-by-Turn Directions")
                    steps = route['features'][0]['properties']['segments'][0]['steps']
                    
                    for i, step in enumerate(steps, 1):
                        st.markdown(f"""
                            <div class='route-details'>
                                <span class='step-badge'>{i}</span>
                                <p style='margin: 0; font-size: 1.05rem; color: #222;'><strong>{step['instruction']}</strong></p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Could not find one or both locations. Please check the addresses and try again.")

if __name__ == "__main__":
    main() 