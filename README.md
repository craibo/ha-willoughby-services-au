## ha-willoughby-services-au
Provides waste and street sweeping dates for areas in Willoughby Council, NSW.

This repository contains a Home Assistant custom integration, **Willoughby Waste and Street Sweeping Services**, which exposes the following date sensors for a configured Willoughby Council address:

- **Next Red bin collection**
- **Next Yellow bin collection**
- **Next Green bin collection**
- **Next Street Sweep date**
- **Next Autumn bulk waste collection**
- **Next Winter bulk waste collection**
- **Next Summer bulk waste collection**

The integration polls the official Willoughby City Council waste services endpoint once per day to keep dates up to date.

### Installation

- Add this repository as a custom repository in HACS, category `Integration`.
- Install **Willoughby Waste and Street Sweeping Services** from HACS.
- Restart Home Assistant.

### Configuration

- In Home Assistant, go to **Settings → Devices & services → Add integration**.
- Search for **Willoughby Waste and Street Sweeping Services**.
- Provide either:
  - Your **street address** (for display), and/or
  - The Willoughby **geolocation ID** used by the council waste services.
- After setup, seven date sensors will be created for your configured location.


