"""Simple demonstration rules for irrigation recommendations."""

def irrigation_recommendation(soil_moisture, rainfall):
    """Return a basic recommendation using sample thresholds.

    These demo thresholds are not agronomic advice. Real settings must be
    calibrated for crop, soil, growth stage, weather, and local conditions.
    """
    if soil_moisture < 30 and rainfall < 5:
        return "Irrigation Required"
    if soil_moisture < 50 and rainfall < 5:
        return "Moderate Irrigation"
    return "No Irrigation Required"
