import folium
from config import edgeColors, mapTiles, zoomStart
from dane import points


def createMap(G):
    centerLat = sum(point["lat"] for point in points) / len(points)
    centerLon = sum(point["lon"] for point in points) / len(points)

    m = folium.Map(
        location=[centerLat, centerLon],
        zoom_start=zoomStart,
        tiles=mapTiles
    )

    for nodeId, data in G.nodes(data=True):
        folium.Marker(
            location=[data["lat"], data["lon"]],
            tooltip=f"{nodeId} - {data['name']}"
        ).add_to(m)

    

    for nodeA, nodeB, key, data in G.edges(keys=True, data=True):
        

        edgeKey = tuple(sorted([nodeA, nodeB]))
        color = edgeColors.get(edgeKey, "black")

        if nodeA == nodeB:
            lat = G.nodes[nodeA]["lat"]
            lon = G.nodes[nodeA]["lon"]

            radius = data["km"] * 60

            folium.Circle(
                location=[lat, lon],
                radius=radius,
                color=color,
                fill=False,
                weight=4,
                tooltip=(
                    f"{nodeA} ↔ {nodeB}<br>"
                    f"droga = {data['droga']}<br>"
                    f"predkosc max = {data['predkoscMax']} km/h<br>"
                    f"predkosc srednia = {data['predkoscSrednia']} km/h<br>"
                    f"natężenie ruchu = {data['natezenieRuchu']}/5<br>"
                    f"jakość drogi = {data['jakoscDrogi']}/5<br>"
                    f"km lokalnie = {data['km']}<br>"
                    f"czas = {data['czas']} min"
                )
            ).add_to(m)

            continue
        pointA = G.nodes[nodeA]
        pointB = G.nodes[nodeB]

        lat1 = pointA["lat"]
        lon1 = pointA["lon"]

        lat2 = pointB["lat"]
        lon2 = pointB["lon"]

        offset = (key - 1) * 0.03

        midLat = ((lat1 + lat2) / 2) + offset
        midLon = ((lon1 + lon2) / 2) - offset

        edgeKey = tuple(sorted([nodeA, nodeB]))
        color = edgeColors.get(edgeKey, "black")

        folium.PolyLine(
            locations=[
                [lat1, lon1],
                [midLat, midLon],
                [lat2, lon2]
            ],
            color=color,
            weight=4,
            tooltip=(
                f"{nodeA} ↔ {nodeB}<br>"
                f"droga = {data['droga']}<br>"
                f"predkosc max = {data['predkoscMax']} km/h<br>"
                f"predkosc srednia = {data['predkoscSrednia']} km/h<br>"
                f"natężenie ruchu = {data['natezenieRuchu']}/5<br>"
                f"jakość drogi = {data['jakoscDrogi']}/5<br>"
                f"km = {data['km']}<br>"
                f"czas = {data['czas']} min"
            )
        ).add_to(m)

    return m