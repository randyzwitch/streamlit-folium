const earthRadius = 6378137; // equatorial Earth radius in m

function toRadians(angleInDegrees: number) {
    return (angleInDegrees * Math.PI) / 180;
}

function toDegrees(angleInRadians: number) {
    return (angleInRadians * 180) / Math.PI;
}

function offset(
    c1: [number, number],
    distance: number,
    earthRadius: number,
    bearing: number): [number, number] {
    var lat1 = toRadians(c1[1]);
    var lon1 = toRadians(c1[0]);
    var dByR = distance / earthRadius;
    var lat = Math.asin(
        Math.sin(lat1) * Math.cos(dByR) + Math.cos(lat1) * Math.sin(dByR) * Math.cos(bearing)
    );
    var lon =
        lon1 +
        Math.atan2(
            Math.sin(bearing) * Math.sin(dByR) * Math.cos(lat1),
            Math.cos(dByR) - Math.sin(lat1) * Math.sin(lat)
        );
    return [toDegrees(lon), toDegrees(lat)];
}

export function circleToPolygon(center: [number, number], radius: number, sides: number = 32) {
    var coordinates = [];
    for (var i = 0; i < sides; ++i) {
        coordinates.push(
            offset(
                center, radius, earthRadius, (2 * Math.PI * i) / sides
            )
        );
    }
    coordinates.push(coordinates[0]);

    return {
        type: "Polygon",
        coordinates: [coordinates],
    };
};