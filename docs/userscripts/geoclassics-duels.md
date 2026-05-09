# GeoClassics Duels — Script Analysis

**Script:** GeoClassics Duels  
**Version:** 1.5.0  
**Author:** BojanR (Discord: `734114244194467990`, Greasy Fork: [GeoClassics Duels](https://update.greasyfork.org/scripts/566899/GeoClassics%20Duels.user.js))  
**License:** MIT  
**Matches:** `https://www.geoguessr.com/*`

> This document analyses the internals of the GeoClassics Duels Tampermonkey userscript. It is intended as a reference for understanding how the script hooks into GeoGuessr's frontend and the game-server API. All credit for the original work belongs to the script's author.

---

## Overview

GeoClassics Duels overlays a custom game experience on top of GeoGuessr's Parties / Duels feature. It intercepts JSON responses from the game-server, calculates its own health/score system, and injects a HUD directly into the DOM. Two distinct game modes are supported:

| Mode | Trigger | Win condition |
|------|---------|---------------|
| **CLASSICS** | `roundWinMultiplierIncrement` > 0 | Opponent's HP reaches 0 |
| **PINPOINTING** | `roundWinMultiplierIncrement` === 0 | First to reach the win threshold (rounds won) |

---

## Architecture

```
JSON.parse hook
    └─ detects duel state in every parsed response
         ├─ MODE.CLASSICS  → calculateGeoClassics()
         └─ MODE.PINPOINTING → calculatePinpointing()

Google Maps hook (injected page-script)
    └─ intercepts Map / StreetViewPanorama constructors
         ├─ stores instances in window.__GM_MAPS
         ├─ draws target circles on result maps
         └─ handles "X to jump forward" keyboard shortcut

setInterval (1 s)
    ├─ handleSummaryPage()   — summary banner on /summary routes
    └─ injectFullscreenButtons() — POV fullscreen toggle on /spectate

MutationObserver
    └─ ensureButtons() — party preset bar on /party modal
```

---

## Global State

### Mode constants
```js
const MODE = { UNKNOWN, CLASSICS, PINPOINTING }
```
`currentMode` tracks which calculation path is active. It is set each time a duel state is detected in `JSON.parse`.

### Shared identifiers
| Variable | Purpose |
|----------|---------|
| `myPlayerId` | Cached local player ID, used to orient left/right sides |
| `currentDuelId` | ID of the active game; triggers a full state reset when it changes |

### SETTINGS (GM_getValue backed)
| Key | Default | Description |
|-----|---------|-------------|
| `gc_tieDivisor` | 2 | Controls how wide the tie range is: `tieRange = floor((5000 - best) / tieDivisor)` |
| `gc_bgUrl` | imgur URL | Background image for the result screen |
| `gc_presets` | Object | Per-mode default lobby settings (health, timer, multiplier, etc.) |

### Match score state
`matchScoreLeft / matchScoreRight` persist across page loads via `GM_setValue`. `countedGames` (capped at 50 entries) prevents the same game from being counted twice.

---

## Core Functions

### `injectMapHook()`
Runs at `document-start`. Injects a `<script>` into the page context (bypassing the userscript sandbox) that:

- Wraps `google.maps.Map` and `google.maps.StreetViewPanorama` constructors so every instance is stored in `window.__GM_MAPS` / `window.__GM_PANO`.
- Exposes `window.__GM_SET_TARGET(lat, lng, outerRadius, innerRadius, color)` — called by the userscript to draw a coloured annular target on result maps.
- Exposes `window.__GM_SET_PENALTY_MARKERS(coordsArray)` — places badge markers at penalised guess locations.
- Exposes `window.__GM_JUMP_FORWARD(baseDistance)` — moves the Street View panorama forward in the direction of the current POV. Bound to the `X` key. Respects `window.__gm_forbidMoving`.
- Runs a `setInterval` at 50 ms that redraws `google.maps.Polygon` overlays on every result map instance.

### `getMyPlayerId()`
Returns the authenticated user's ID. Tries several locations in `unsafeWindow` and the `__NEXT_DATA__` script tag. Result is cached in `myPlayerId`.

### `cleanupAllUI()`
Removes every custom DOM element (HUD, game-over overlay, score boxes, match-point badges, round number, summary banner). Called whenever a new `currentDuelId` is detected.

### `hideDefaultGeoGuessrUI()`
Injects a `<style id="geoclassics-hide-style">` that hides GeoGuessr's native health bars, damage numbers, round multipliers, and spectator sidebars. Also applies the custom background image and all animation keyframes. Idempotent — only injected once.

### `setMapState(target, penalties)`
Bridges the userscript sandbox into the page context by calling `unsafeWindow.__GM_SET_TARGET` and `unsafeWindow.__GM_SET_PENALTY_MARKERS`.

### `formatDistance(meters)`
Formats a raw metre value to a human-readable string (`"1.2 km"` or `"450 m"`).

### `updateRoundScoresUI(lScore, rScore, lDist, rDist, isGamemaster, lPenalized, rPenal)`
Spectator-only. Renders per-round score and distance labels at fixed positions within `spectate-header_variableContent`. Calls `animateRoundScore` for the count-up animation.

### `injectFullscreenButtons()`
Adds a fullscreen toggle button to every `player-pov_root__` element on the spectate page. Clicking toggles the `.geoclassics-pov-fullscreen` class which uses CSS `position:fixed; inset:0` to expand the POV.

### `updateMatchScoreUI()`
Spectator-only. Renders a persistent `MATCH SCORE L - R` label above the centre of the spectate header.

### `updateRoundNumberUI(roundNum)`
Spectator-only. Renders `ROUND N` at the top-centre of the spectate header.

---

## Mode 1: CLASSICS

### `calculateGeoClassics(data)`
The main calculation loop for the health-based mode.

**Algorithm per round:**

1. Look up each team's `roundResults[i].score`.
2. Compute `tieRange = floor((5000 - best) / tieDivisor)`. If the score gap is within `tieRange`, the round is a tie (no multiplier change, no damage).
3. `damage = |scoreLeft - scoreRight| * winnerMultiplier`. Subtracted from the loser's health.
4. Winner's multiplier increases by `multiIncrement`.

**Side assignment:** In player mode the local player is always placed on the left. In spectator mode team index 0 is left.

**Animations:** When a new finished round is detected (`lastFinishedRoundNum > gc_lastAnimatedRound`), the function schedules:
- `triggerPlayerMultiAnimation` — CSS `animate-multi-bump` on the winner's multiplier box.
- `triggerPlayerDamageAnimation` — CSS `animate-damage-pop` showing the damage number.
- `countDownValue` — animated HP countdown.

**Target circle:** Calculates `outerRadius` and `innerRadius` from the score using the inverse of GeoGuessr's scoring formula: `r = -(maxErr/10) * ln(score/5000)`. The circle is green for a decisive win, gold for a tie.

**Win detection:** When either health reaches 0, `showGeoClassicsGameOver` is called after a delay.

### `renderGeoClassicsHUD(lH, rH, lM, rM, leftColor, rightColor, useDelay, maxH)`
Builds the HUD DOM on first call and updates it on subsequent calls. Two layouts exist:

- **Spectator layout** — multiplier boxes centred above each player, health bars in the column grid cells.
- **Player layout** — compact side panels beside the native HUD area, including a round score counter below each health bar.

The health bar width is a CSS transition driven by `width: ${(hp/maxH)*100}%`. Transition delay is set to `useDelay ? VISUAL_DELAY_MS : 0` to synchronise with the GeoGuessr result reveal.

### `showGeoClassicsGameOver(winnerSide, lH, rH, ...)`
Renders a full-screen overlay with "GAME OVER" and the winner's name (looked up from `userNameMap`). A "Close" button sets `gc_gameOverDismissed = true` and removes the overlay.

### `triggerPlayerMultiAnimation(side)` / `triggerPlayerDamageAnimation(side, damage)`
Force-reflow pattern (`void el.offsetWidth`) to restart CSS animations on the multiplier and damage elements.

### `countDownValue(id, start, end, dur)`
`requestAnimationFrame` loop that interpolates a DOM element's `textContent` from `start` to `end` over `dur` milliseconds.

### `animateRoundScore(el, endScore, delayMs)`
Count-up animation using `setInterval` at 30 fps. Clears any previous animation targeting the same element. If `endScore` is `null`, the element is blanked immediately.

---

## Mode 2: PINPOINTING

### `calculatePinpointing(data)`
Score-based mode where each round awards 1 or 2 points (no HP).

**Point rules per round:**

| Situation | Points awarded |
|-----------|---------------|
| Both 5000, team 0 faster | team 0 +1 |
| Both 5000, team 1 faster | team 1 +1 |
| One team scores 5000, other does not | winner +2 |
| Normal win outside tie range | winner +1 |
| Tie (within tie range) | neither |

**Penalty rule:** If a player guesses before the penalty time (`roundStart + maxRoundTime - roundTime`) and their score is not 5000, their score is set to 0.

**Tie range** uses the same formula as CLASSICS: `floor((5000 - best) / tieDivisor)`.

When scores change, the function locks the score boxes (`dataset.locked = 'true'`), waits 4 seconds for the GeoGuessr animation, then updates and flashes the box.

### `renderPinpointingHUD(winThreshold)`
Creates or updates two absolute-positioned score boxes (`#leftScore`, `#rightScore`). On player view it also manages match-point badges (`#leftMatchpoint`, `#rightMatchpoint`) when a team is within 2 points of the threshold. On spectator view, match-point badges are attached directly to the `player-pov_root__` elements.

### `flashScore(scoreElement)`
Alternates the score box background/border between the flash colour (`rgba(90,219,149,0.4)`) and the original 6 times at 300 ms intervals.

### `showPinpointingEndScreen(winThreshold, lTeam, rTeam)`
Same pattern as `showGeoClassicsGameOver` — full-screen overlay with winner name and final score, dismissible.

---

## Summary Page

### `handleSummaryPage()`
Polls on a 1 s interval when the path includes `/summary`. Fetches the completed game from `game-server.geoguessr.com/api/duels/{id}` and chooses the correct summary renderer based on `roundWinMultiplierIncrement`.

### `calculateClassicsSummary(data)` / `calculatePinpointingSummary(data)`
Re-run the respective calculation loops against the complete round history and return a final state object (`{blueHealth, redHealth, blueMulti, redMulti}` or `{leftScore, rightScore}`).

### `renderClassicsDuelsSummary(state, container)` / `renderPinpointingSummary(state, container)`
Prepend a styled banner to `game-summary_innerContainer` showing the winner and final HP / score.

---

## JSON.parse Hook

```js
const originalParse = JSON.parse;
JSON.parse = function(...args) { ... }
```

Every JSON payload parsed by GeoGuessr passes through this wrapper. The hook:

1. Extracts `user.id` to populate `myPlayerId`.
2. Detects `forbidMoving` in any of several possible locations and sets `unsafeWindow.__gm_forbidMoving`.
3. Reads `map.maxErrorDistance` for the target-circle formula.
4. Identifies a duel state object (by the presence of `gameId`, `teams`, `rounds`).
5. On a new `gameId`, calls `cleanupAllUI()` and resets all state.
6. Routes to `calculateGeoClassics` or `calculatePinpointing`.

---

## Party Preset System

When the user is on `/party` and the Settings modal is open, a floating button bar is injected.

### `applyPreset(key)`
Orchestrates a sequence of DOM interactions to configure the lobby:

| Helper | What it drives |
|--------|---------------|
| `setGameMode(label)` | Clicks the correct mode label (Moving / No Move / NMPZ) |
| `setSliderValue(labelText, val)` | Finds the slider wrapper by label, sets value via `setReactInputValue` |
| `setNumericToValue(labelText, target)` | Clicks +/- buttons until the value matches (up to 150 iterations) |
| `setInitialHealth(value)` | Direct input manipulation on the health field |
| `setToggle(labelText, state)` | Clicks a checkbox label if its current state differs |

### `setReactInputValue(input, value)`
Uses the native `HTMLInputElement.prototype.value` setter descriptor (bypassing React's synthetic event system) then dispatches `input` and `change` events to trigger React's reconciliation.

### `clickOnceAndVerify(btn, wrap, expectedStepSign)`
Clicks a +/- button and waits up to 350 ms for the value to change. Retries once if the value did not change. Returns the new value.

### `updateButtonStyles()`
Reads the current lobby settings and highlights the matching preset button with a green border/background. Also relabels the "Rounds Without Multipliers" numeric row to "First to (how many points)" when the Pinpointing preset is active.

### Match Score Panel
Visible to non-guest hosts only. Provides +/- adjusters for `matchScoreLeft` / `matchScoreRight`, a reset button, and an enable/disable toggle. All values persist via `GM_setValue`.

---

## Timing Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| `ANIMATION_DELAY_MS` | 2650 ms | Delay before multiplier animation (synced to GeoGuessr reveal) |
| `VISUAL_DELAY_MS` | 2650 ms | Delay before HP bar transition and damage pop |
| `TRANSITION_MS` | 2300 ms | Duration of the HP count-down animation |
| GM offset (player) | 0 ms | No extra delay in player mode |
| GM offset (spectator) | +3000 ms (multi) / +2000 ms (health) | Spectator sees results later |

---

## External API Usage

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `game-server.geoguessr.com/api/duels/{id}` | GET (fetch, credentials: include) | Summary page — fetch completed game state |
| `www.geoguessr.com/api/v3/users/{playerId}` | GET (fetch, credentials: include) | Resolve player nicknames not included in the duel payload |
