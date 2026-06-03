import folium
from config import roadColors, cityLabelColor, mapTiles, zoomStart
from dane import points


def getRoadType(roadName):
    parts = roadName.replace("+", " ").replace(",", " ").split()

    if "Lokalne" in roadName:
        return "LOCAL"

    for part in parts:
        if part.startswith("A") and part[1:].isdigit():
            return "A"

    for part in parts:
        if part.startswith("S") and part[1:].isdigit():
            return "S"

    for part in parts:
        if part.startswith("DK"):
            return "DK"

    for part in parts:
        if part.startswith("DW"):
            return "DW"

    return "OTHER"


def getRoadColor(roadName):
    roadType = getRoadType(roadName)
    return roadColors.get(roadType, roadColors["OTHER"])


def createMap(G):
    centerLat = sum(point["lat"] for point in points) / len(points)
    centerLon = sum(point["lon"] for point in points) / len(points)

    m = folium.Map(
        location=[centerLat, centerLon],
        zoom_start=zoomStart,
        tiles=mapTiles
    )

    for nodeId, data in G.nodes(data=True):
        folium.CircleMarker(
            location=[data["lat"], data["lon"]],
            radius=5,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=1,
            tooltip=f"{nodeId} - {data['name']}"
        ).add_to(m)

        folium.Marker(
            location=[data["lat"], data["lon"]],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 13px;
                    font-weight: bold;
                    color: {cityLabelColor};
                    background-color: white;
                    border: 1px solid {cityLabelColor};
                    border-radius: 4px;
                    padding: 2px 5px;
                    white-space: nowrap;
                    transform: translate(10px, -10px);
                ">
                    {data['name']}
                </div>
                """
            )
        ).add_to(m)

    

    for nodeA, nodeB, key, data in G.edges(keys=True, data=True):

        color = getRoadColor(data["droga"])

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

        color = getRoadColor(data["droga"])

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