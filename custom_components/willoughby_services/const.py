DOMAIN = "willoughby_services"

PLATFORMS: list[str] = ["sensor"]

CONF_ADDRESS = "address"
CONF_GEOLOCATION_ID = "geolocationid"

API_BASE_URL = "https://www.willoughby.nsw.gov.au/ocapi/Public/myarea/wasteservices"
API_LANG = "en-AU"
API_PAGE_LINK = "/$b9015858-988c-48a4-9473-7c193df083e4$/Residents/Waste-and-street-sweeping-services"

SENSOR_KEYS = {
    "red_bin": "next_red_bin_collection",
    "yellow_bin": "next_yellow_bin_collection",
    "green_bin": "next_green_bin_collection",
    "street_sweep": "next_street_sweep_date",
    "autumn_bulky": "next_autumn_bulky_collection",
    "winter_bulky": "next_winter_bulky_collection",
    "summer_bulky": "next_summer_bulky_collection",
}

