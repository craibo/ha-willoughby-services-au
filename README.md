# Willoughby Waste and Street Sweeping Services

[![GitHub Release](https://img.shields.io/github/v/release/craibo/ha-willoughby-services-au?style=flat)](https://github.com/craibo/ha-willoughby-services-au/releases)
[![GitHub Activity](https://img.shields.io/github/commit-activity/m/craibo/ha-willoughby-services-au?style=flat)](https://github.com/craibo/ha-willoughby-services-au/commits/main)
[![License](https://img.shields.io/github/license/craibo/ha-willoughby-services-au?style=flat)](LICENSE)
[![hacs_default](https://img.shields.io/badge/HACS-Default%20candidate-blue.svg?style=flat)](https://hacs.xyz/)
[![Integration](https://img.shields.io/badge/Home%20Assistant-2024.1+-41BDF5.svg?style=flat)](https://www.home-assistant.io/)

A Home Assistant **integration** for [Willoughby City Council](https://www.willoughby.nsw.gov.au/) that provides waste collection and street sweeping date sensors for properties within the council area, NSW Australia. This integration is designed for inclusion in the HACS default repository list and is currently installable as a custom HACS repository.

---

## Support this project

[![Sponsor me on GitHub](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?style=flat&logo=github)](https://github.com/sponsors/craibo)
[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue?style=flat&logo=paypal)](https://paypal.me/craibo?country.x=AU&locale.x=en_AU)

---

## Features

- **Waste Collection Tracking**: Next collection dates for red, yellow, and green bins
- **Street Sweeping Dates**: Next scheduled street sweep for your configured address
- **Bulk Waste Schedules**: Upcoming autumn, winter, and summer bulk waste collection dates
- **Daily Polling**: Automatic daily refresh from the official Willoughby City Council waste services endpoint
- **Simple Setup**: UI-based configuration through Home Assistant with address or geolocation ID

## Quick Start

### Installation via HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) following the instructions [here](https://hacs.xyz/docs/use/)
2. In HACS, add this repository as a **Custom repository** with category `Integration`
3. Search for and install **Willoughby Waste and Street Sweeping Services**
4. Restart Home Assistant

### Manual Installation

1. Download the `willoughby_services` folder from the `custom_components` directory
2. Copy it to your Home Assistant `custom_components` directory
3. Restart Home Assistant

### Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** and search for "Willoughby Waste and Street Sweeping Services"
3. Provide one or both of:
   - **Street address**: Your Willoughby Council street address. The integration will call the official Willoughby “My Area” search API to resolve the correct property and geolocation ID.
   - **Geolocation ID**: The Willoughby Council geolocation identifier used by the waste services API (advanced/manual option).
4. If your street search matches multiple properties, you will be asked to pick the exact address.
5. After setup, seven date sensors will be created for your configured location

## Sensors Created

For each configured address, the following date sensors are created:

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Next Red bin collection | `sensor.*_next_red_bin_collection` | Next red (general waste) bin collection date |
| Next Yellow bin collection | `sensor.*_next_yellow_bin_collection` | Next yellow (recycling) bin collection date |
| Next Green bin collection | `sensor.*_next_green_bin_collection` | Next green (garden) bin collection date |
| Next Street sweep | `sensor.*_next_street_sweep_date` | Next scheduled street sweeping date |
| Next Autumn bulk waste | `sensor.*_next_autumn_bulky_collection` | Next autumn bulk waste collection date |
| Next Winter bulk waste | `sensor.*_next_winter_bulky_collection` | Next winter bulk waste collection date |
| Next Summer bulk waste | `sensor.*_next_summer_bulky_collection` | Next summer bulk waste collection date |

## Troubleshooting

### Common Issues

**Sensors showing "unavailable"**

- Check your internet connection
- Verify your street address or geolocation ID is valid for Willoughby City Council
- Check the integration logs for specific errors

**No sensors created after setup**

- Confirm the address falls within the Willoughby City Council area
- Restart Home Assistant and check the integration is loaded

### Debug Logging

Add to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.willoughby_services: debug
```

## Support

- **Issues**: Report bugs or feature requests via [GitHub Issues](https://github.com/craibo/ha-willoughby-services-au/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
