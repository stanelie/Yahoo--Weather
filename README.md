# YWeather for Pebble

Originally by dabdemon. Forked and maintained by stanelie.

---

## What it does

A Pebble watchface that displays the current time, date, weather conditions, and a 3-day forecast. Weather data is fetched from OpenWeatherMap using your own free API key.

## Requirements

- A Pebble, Pebble Time, or Pebble Time Round watch running Rebble
- An [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) account (free tier is sufficient)
- The Rebble companion app on Android or iOS

## Building

Requires the Rebble/Pebble SDK with waf.

```
pebble build
pebble install --phone <your-phone-ip>
```

## Settings

Open the Pebble app on your phone, go to My Watchfaces, and tap the gear icon next to YWeather. The settings page is hosted at:

```
https://stanelie.github.io/Yahoo--Weather/ywsettings36.html
```

Enter your OpenWeatherMap API key in the Custom API Key field and adjust preferences, then tap Submit.

---

## Changes from the original (stanelie fork)

### Build system
- Rewrote `wscript` to use the current Rebble SDK API (`pbl_build` / `pbl_bundle` with per-platform loop), fixing a `TypeError` crash that prevented the app from compiling at all.

### Bug fixes
- Fixed a copy-paste bug in `unloadInitialTuples()` in `appMessage.c` where 13 out of 15 `memset` calls used the wrong destination buffer, causing a `-Werror=array-bounds` compiler error.

### Weather
- Switched all OpenWeatherMap requests from HTTP to HTTPS.
- Switched forecast endpoint from `/data/2.5/forecast/daily` (paid) to `/data/2.5/forecast` (free 3-hour intervals), with daily aggregation of min/max temperatures.
- Rewrote `openweatherByLatLong()` from synchronous to asynchronous XHR. The Pebble JS runtime silently intercepts and drops synchronous XHR (`XHR intercepting! returning from open`), so the weather never loaded with the original code.
- Removed all dead weather provider code (Yahoo! Weather, The Weather Underground, forecast.io). All weather now routes directly to OpenWeatherMap.
- Fixed `getWeatherFromLocation()` (GPS-off path) to use OpenWeatherMap instead of falling through to the dead Yahoo default.

### Settings
- Fixed the settings button doing nothing: `CheckUserKey()` was called in the `showConfiguration` handler but was never defined, causing a `ReferenceError` that silently prevented `Pebble.openURL()` from firing.
- Added `sendSettingsToWatch()`, called immediately on `webviewclosed` before the weather fetch, so display settings (seconds, theme, etc.) apply even when weather is unavailable.
- Added a cache-busting timestamp to the settings URL so the phone's WebView always fetches a fresh copy.
- Fixed default `weatherprovider` from `"0"` (Yahoo) to `"3"` (OpenWeatherMap).

### Appearance
- Time is now always white on all Pebble models (was `GColorChromeYellow` on color Pebbles).
- Battery ring is now always white at all charge levels (was red/orange/yellow/green based on charge percentage).

### Menu icon
- Replaced the non-standard 24×28 placeholder icon with a 25×25 screenshot of the actual watchface (required size for the Pebble SDK).

### Settings page (GitHub Pages)
- Replaced broken CDN links with stable cdnjs alternatives.
- Removed the dead license/PayPal system entirely (User Key, License Type, PayPal button, all LT1/LT2/LT3 badge labels on settings controls).
- Unlocked all settings that were previously gated behind the dead license server.
- Removed dead weather provider options; shows "OpenWeatherMap" as a static label.
- Removed the Support and Cancel buttons.
- Submit button is now fixed to the top of the screen so it is always reachable while scrolling.
- Improved toggle button contrast: unselected buttons are dark/muted, selected buttons are bright green with a checkmark prefix.
- Removed the collapsible accordion sections — all settings are always visible.
- Merged the Common Settings and Extra Features tabs into one continuous scrollable page.
- Removed the top jumbotron instructions block and the Extra Features warning banner.
