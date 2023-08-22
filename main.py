import osmnx as ox
import folium

def find_large_parking_lots(city_name, top_n=10):
    graph = ox.graph_from_place(city_name, network_type='drive')
    center = ox.geocode(city_name)
    
    m = folium.Map(location=center, zoom_start=13)

    parking_lots = ox.geometries_from_place(city_name, tags={'amenity': 'parking'})

    parking_lots['area'] = parking_lots.geometry.area
    large_parking_lots = parking_lots.nlargest(top_n, 'area')

    for _, row in large_parking_lots.iterrows():
        location = (row['geometry'].centroid.y, row['geometry'].centroid.x)
        google_maps_link = f"https://www.google.com/maps?q={location[0]},{location[1]}"
        
        folium.Marker(
            location=location,
            popup=f"<a href='{google_maps_link}' target='_blank'>Open in Google Maps</a>",
            icon=folium.Icon(color='blue')
        ).add_to(m)

    return m

city_name = input("Enter the city name: ")
m = find_large_parking_lots(city_name)
m.save("Parking_Lot_Maps/" + city_name.replace(" ", "_") + "_parking_lots_map.html") 
