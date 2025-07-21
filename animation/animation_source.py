def return_lat_long(coords):

    """
    Take a polyline code, decode it into a list of latitude and longitude coordinates
    """

    # TODO turn it into a dictionary of lists so we can add in total distance and day

    data = {}

    coordinates = polyline.decode(coords)

    latitudes = [coordinate[0] for coordinate in coordinates]
    longitudes = [coordinate[1] for coordinate in coordinates]

    return latitudes, longitudes
