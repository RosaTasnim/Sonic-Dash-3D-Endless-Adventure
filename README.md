# Sonic Dash - 3D Endless Adventure

## Overview
`Project.py` implements a 3D endless runner built with `PyOpenGL` and `GLUT`. The player controls a Sonic-inspired runner on a three-lane track, avoids or destroys hazards, collects rings and special orbs, and survives as long as possible while speed and pattern complexity increase over distance.

The runtime is organized around a real-time update loop that handles:

- game state transitions (`menu`, `countdown`, `playing`, `paused`, `gameover`)
- continuous forward progression and difficulty scaling
- player movement, action timers, and collision resolution
- obstacle and collectible spawning
- environment animation, particles, HUD rendering, and camera updates

The primary goal is to maximize distance and score while managing health, charge count, dash meter, and temporary power-up effects.

### Control Summary
| Input | Action |
| --- | --- |
| `A` / `D` | Move left or right between lanes |
| `W` / Mouse Wheel Up | Jump |
| `S` / Mouse Wheel Down | Slide |
| `F` / Left Mouse Button | Charge attack |
| `SPACE` / Right Mouse Button | Dash boost |
| `C` | Toggle Cheat Mode |
| `G` | Toggle God Mode |
| `V` | Toggle first-person / third-person camera |
| `R` | Pause / resume |
| `ESC` | Open exit confirmation |

## Features

All implemented gameplay, interface, view, feedback, and state-management systems in `Project.py` are mapped into the 9 core features below.

### 1. Endless Run Progression
Core feature: The game is structured as an endless survival run with no final level. Difficulty rises over time, and the run ends only when the player loses all health outside special modes.

Subfeatures:

- **Run State Flow**  
  The game moves through `menu`, `countdown`, `playing`, `paused`, and `gameover`. A run starts from the menu, uses a `3` second countdown, can be paused and resumed with `R`, can be restarted after defeat, and can be interrupted by an exit confirmation overlay with `Y/N` input.

- **Distance And Score Tracking**  
  Total distance increases continuously from forward speed, while score grows from both traveled distance and interaction rewards such as obstacle destruction and collectible pickups. These values are the main progression outputs of a run.

- **Difficulty Scaling Curve**  
  Difficulty rises automatically as distance grows. Speed tier increases every `250` meters, base speed climbs from `50` toward a cap of `100`, and live speed is interpolated each frame so progression feels smooth rather than abrupt.

- **Spawn And Pattern Progression**  
  Obstacle and collectible spawn intervals shrink as the run advances, and new obstacle patterns unlock at specific distance milestones. Barrier and spike patterns appear first, branch patterns unlock later, and badnik combinations unlock in deeper progression.

- **Camera Angle System**  
  The run supports both third-person and first-person camera angles, toggled with `V`. The camera system includes chase-view framing, first-person perspective, run bob, hit shake, form-sensitive height changes, and state-wide availability across menu, countdown, pause, gameplay, and game over.

- **HUD And Screen Feedback**  
  Endless run progression is communicated through the HUD and overlays. The interface shows distance, score, health, rings, charges, speed tier, speed, dash meter, status bars, mode labels, hit warnings, dash-ready prompts, menu guidance, countdown prompts, pause overlay, game-over summary, and exit confirmation.

- **World Streaming And Run Reset**  
  The environment is continuously recycled with hills, palms, and arches to preserve the illusion of an endless track. Starting a new run resets player state, timers, score, particles, obstacles, collectibles, and world objects in one coordinated initialization pass.

### 2. Three Lane Movement
Core feature: Horizontal navigation is lane based, not free roaming. The player occupies one of three track lanes and continuously shifts among them to find safe paths and pickup lines.

Subfeatures:

- **Lane Topology**  
  The track is divided into three discrete lanes: left, center, and right. Both player motion and world placement depend on the same lane-to-position mapping, making navigation and hazard reading spatially consistent.

- **Smooth Lane Switching**  
  Lane changes are interpolated rather than teleported. The player slides toward the selected lane over time, which makes transitions readable and keeps collisions tied to motion timing instead of instant snaps.

- **Boundary And Start Rules**  
  Movement is clamped to the outer lanes, so the player cannot move beyond the leftmost or rightmost track edge. Every new run begins in the center lane, providing a balanced starting position.

- **Hazard Avoidance Routing**  
  Lane switching is the primary response to barriers and many mixed obstacle layouts. As patterns become denser, selecting the safest lane becomes one of the central survival skills in the run.

- **Collectible Path Routing**  
  Rings and orbs are lane aligned, so movement is also a scoring and resource-management system. Efficient lane choices let the player avoid threats while staying on profitable pickup lines.

- **Mode Based Control Ownership**  
  In standard play and Cheat Mode, lane changes are fully manual. In God Mode, lane ownership shifts to the autopilot system, which chooses and steers toward target lanes automatically.

### 3. Jump Slide Mechanics
Core feature: Vertical evasion is handled through jump and slide actions. These mechanics let the player clear low hazards, overhead hazards, and selected enemy interactions.

Subfeatures:

- **Base Locomotion State**  
  The player normally remains in a running state, which drives the animation cycle, camera bob, and baseline collision posture. Other movement forms temporarily replace this state and then return to run when their timers or physics resolve.

- **Jump Physics Model**  
  Jumping applies upward force `25` against gravity `-50`, producing a full airborne arc. Jump can only begin from the ground, and it remains active until the player lands back at `y = 0`.

- **Slide State Model**  
  Sliding lasts `1.0s` and compresses the player profile into a low roll-like state. This is the primary answer to overhead obstacles such as branches.

- **Buffered Recovery Timing**  
  If slide is pressed during a jump, the game stores a buffered slide for `0.25s`. On landing, the player clears jump velocity, spawns a landing effect, and immediately enters slide if the buffered input is still valid.

- **Clearance And Collision Profiles**  
  Jump and slide are tied to obstacle-specific clearance rules. Spikes are cleared by sufficient height, branches are cleared by staying low, and the player’s collision and pickup bounds change dynamically across run, jump, slide, charge, and dash forms.

- **State Interaction And Inputs**  
  Jump and slide interact with charge and dash rather than existing independently. Dash and charge cancel slide on entry, and jump/slide support both keyboard and mouse-wheel input paths during active play.

### 4. Charge Attack System
Core feature: Charge is a short offensive action used to break through hazards, especially badnik enemies, while consuming a limited charge resource.

Subfeatures:

- **Activation And Input Mapping**  
  Charge is triggered manually with `F` or the left mouse button during active play. The action is a deliberate player-controlled attack state rather than an automatic response in normal modes.

- **Charge Resource Economy**  
  The player starts with `5` charges, and each activation consumes one use. Charge cannot begin if the count has already dropped to zero, so offensive play is limited by resource management.

- **Timed Speed State**  
  Charge lasts `1.0s` and applies a `1.25x` forward speed multiplier during its active window. This gives the move both offensive utility and a temporary pace increase.

- **State Entry Constraints**  
  Charge cannot start while dash is active, cannot stack with another charge, and cancels slide on activation. These restrictions prevent conflicting high-priority movement states from overlapping.

- **Combat And Recovery Loop**  
  Charge can destroy breakable hazards on contact and is especially useful against badniks. Charge orb pickups fully refill the charge stock, and charging through a badnik can restore one spent charge if the meter is not already full.

- **Visual And HUD Feedback**  
  Starting charge creates a particle burst and flash effect, while the HUD shows both the remaining charge count and a live charge timer bar during active use.

### 5. Dash Boost System
Core feature: Dash is a high-speed burst state that increases movement speed, generates an offensive trail effect, and can smash through hazards.

Subfeatures:

- **Meter Acquisition System**  
  Dash is gated by a `0-100%` meter. Rings add `+1%` and dash orbs add `+5%`, so normal collection routes directly support boost readiness.

- **Activation Requirements**  
  Dash can begin only when the meter reaches `100%`, and it is triggered with `SPACE` or the right mouse button. This makes dash a stored burst resource rather than a constant movement mode.

- **Timed Speed Burst**  
  Dash lasts `3.0s` and applies a `1.5x` speed multiplier over base speed, making it the fastest manual movement state in the game.

- **Offensive Collision Power**  
  While dash is active, the player can smash breakable hazards on contact rather than taking damage. Dash also grants a small recovery buffer on activation to reduce edge-case startup collisions.

- **Meter Drain And State Cleanup**  
  During dash, the meter visually drains based on the remaining dash timer. When the state ends, the timer is cleared, the dash state is removed, and the meter returns to zero.

- **Visual And HUD Feedback**  
  Dash is reinforced with startup particles, continuous trail effects, a dedicated HUD meter bar, and a `DASH READY - PRESS SPACE` prompt when the resource is fully charged.

### 6. Obstacle Enemy System
Core feature: The game uses lane-based hazards and enemies to force reaction choices, lane planning, and attack usage.

Subfeatures:

- **Obstacle And Enemy Roster**  
  The system contains four main threat types: barriers, spikes, branches, and badniks. Each type occupies a different part of the lane space and demands a different response, such as switching, jumping, sliding, or charging.

- **Object Data And Breakability**  
  Every obstacle stores lane, position, size, animation phase, and score value, and the objects are treated as breakable hazards. This allows dash, charge, invincibility, shield logic, and mode overrides to interact with them consistently.

- **Pattern Based Spawning**  
  Obstacles are spawned as predefined lane patterns instead of purely isolated random placements. This creates deliberate challenge layouts and supports distance-based escalation.

- **Spawn Safety Rules**  
  Same-lane spacing rules prevent impossible stacks, especially for repeated spikes and mixed branch-plus-barrier combinations. Collectible placement also checks obstacle occupancy so reward lines are not blindly blocked.

- **Collision And Damage Resolution**  
  On contact, the game resolves collisions through a layered pipeline: power invincibility, active attack state, shield protection, Cheat Mode logic, God Mode intervention, and finally normal damage. Standard hazards deal `1` damage, while badniks deal `2`.

- **Rewards, Feedback, And Failure**  
  Destroying obstacles grants score, with badniks rewarding the most. Hazard destruction produces particle bursts, successful clears and shield breaks use distinct feedback, and health reaching zero in standard play triggers crash feedback and game over.

### 7. Collectible Powerups
Core feature: Rings and orb pickups create the game’s resource economy by feeding dash usage, charge recovery, defense, healing, and temporary utility effects.

Subfeatures:

- **Ring Economy**  
  Rings appear in straight chains and jump-friendly arcs. Each ring adds `1` to the ring counter, grants `10` score, and increases the dash meter by `1%` outside Cheat Mode.

- **Orb Distribution System**  
  Special orbs are spawned through a weighted random system, with dash orbs appearing most often and stronger defensive or recovery pickups appearing less frequently. The menu also documents the collectible roster before the run begins.

- **Mobility And Attack Powerups**  
  Dash orbs add `5%` dash meter and charge orbs refill all charges. These pickups feed the two major offensive movement systems directly.

- **Defense And Survival Powerups**  
  Shield orbs provide a single-hit protection layer for `5s`, invincibility orbs grant `5s` of obstacle-smashing immunity, and health orbs restore `2` health up to the maximum of `5`.

- **Magnet And Pickup Handling**  
  Magnet orbs enable a `5s` ring-attraction effect with a wider collection radius. More broadly, pickups use their own collision profile, letting rings and orbs remain collectible across multiple player movement forms.

- **Visual And HUD Feedback**  
  Collectibles rotate, pulse, and bob in space, each pickup type produces its own particle feedback, shield adds a visible aura, and temporary effects such as magnet, shield, charge, and invincibility are represented through labeled HUD timer bars.

### 8. Cheat Mode
Core feature: Cheat Mode is a player-assisted survival mode that reduces resource pressure and softens punishment without fully automating the game.

Subfeatures:

- **Toggle And Exclusivity Rules**  
  Cheat Mode is toggled with `C`, and enabling it automatically disables God Mode. The two special modes are mutually exclusive at all times.

- **State Reset On Entry**  
  Switching Cheat Mode resets dash and charge action state, clears mode-specific timers, restores health to maximum, and clears recent hit-feedback state so the mode begins from a clean baseline.

- **Automatic Resource Recovery**  
  While Cheat Mode is active, dash refills automatically when the player is not dashing, and charges regenerate over time until they return to maximum.

- **Health Regeneration Model**  
  Cheat Mode still allows temporary health loss, but health recovers after a short delay and then returns in timed steps rather than remaining permanently depleted.

- **Reduced Consequence Collisions**  
  Obstacle contact destroys the obstacle and applies softer health loss instead of the normal fatal damage path. Badnik collisions remain heavier than standard hazard collisions.

- **Manual Play And Presentation**  
  Cheat Mode keeps manual control over lanes, jump, slide, charge, and dash while changing the player color and showing a `CHEAT MODE` HUD label so the altered rules remain visible.

### 9. God Mode
Core feature: God Mode is a fully assisted autopilot mode that automatically reads hazards, changes lanes, and executes the correct action before collision.

Subfeatures:

- **Toggle And Setup Rules**  
  God Mode is toggled with `G`, automatically disables Cheat Mode, clears conflicting dash and charge state, resets autopilot focus data, restores charge stock to maximum, and starts from a clean automation baseline.

- **Autonomous Lane Controller**  
  The autopilot owns lane movement while active. It keeps a target lane, continuously steers the player toward that lane, and replaces manual lane choice entirely.

- **Obstacle Analysis Pipeline**  
  God Mode tracks a current focus obstacle, scans ahead for the nearest relevant threat in-lane, evaluates distance-based triggers, checks candidate lane safety, and can temporarily lock lane choice to avoid unstable switching.

- **Automated Action Responses**  
  The system chooses the correct action per obstacle type: switching away from barriers, jumping over spikes, sliding under branches, and charging into badniks when needed.

- **Auto Dash And Failsafe Protection**  
  When dash meter reaches `100%`, God Mode activates dash automatically. If a collision is about to happen, the autopilot can force an emergency lane or action correction to avoid normal damage resolution.

- **Input Suppression And Presentation**  
  Manual movement and attack inputs are ignored while God Mode is active, and the mode announces itself through distinct player coloration and a `GOD MODE` label in the HUD.

## Gameplay Rules

### Objective
- Survive for as long as possible.
- Increase total distance and score.
- Collect rings and power-ups to strengthen mobility, offense, and defense.

### Starting A Run
- The game starts in the menu state.
- Press `SPACE` to begin a new run.
- A `3` second countdown plays before live gameplay starts.

### Player Resources
- Maximum health: `5`
- Maximum charge count: `5`
- Dash meter range: `0%` to `100%`
- Ring counter: increases as rings are collected

### Scoring Rules
- Score increases continuously from forward distance.
- Score also increases from collecting rings, collecting special orbs, and destroying obstacles.

### Movement Rules
- The player can occupy only one of three lanes at a time.
- `A` moves left and `D` moves right within lane bounds.
- `W` jumps, `S` slides, `F` charges, and `SPACE` activates dash when the meter is full.
- In God Mode, manual movement and attack inputs are bypassed by autopilot decisions.

### View Rules
- Press `V` to switch between first-person and third-person camera modes.
- Camera switching is available in menu, countdown, active play, paused state, and game-over state.
- Third-person gives a wider tactical view of the track.
- First-person uses form-sensitive camera height, bob, and hit shake for a more immersive perspective.

### HUD And Screen Rules
- The menu screen shows the title, controls, collectible reference, and start prompt.
- The countdown screen shows the remaining start timer and a `GO!` transition.
- The gameplay HUD shows distance, score, health, rings, charges, speed tier, speed, and dash percentage.
- The HUD also shows active effect timers, dash-ready prompts, mode labels, and hit warnings.
- The pause screen overlays the live view and instructs the player to press `R` to resume.
- The game-over screen displays final distance and final score, then waits for a restart command.
- The exit confirmation screen blocks normal play until `Y` confirms quit or `N` cancels.

### Obstacle Interaction Rules
- Barrier: safest answer is lane switching; attack states can also destroy it.
- Spike: must be jumped over.
- Branch: must be slid under.
- Badnik: best handled with charge attack or a clean jump-over; direct collision is costly.

### Damage And Survival Rules
- Normal obstacle hits deal `1` damage.
- Badnik hits deal `2` damage.
- After a normal hit, the player receives `3s` of recovery invincibility.
- If health reaches `0` in standard play, the run enters `gameover`.

### Power-Up Rules
- Rings increase score and charge the dash meter.
- Dash orb accelerates dash readiness.
- Charge orb fully restores charges.
- Magnet orb attracts rings for `5s`.
- Shield orb blocks one obstacle for `5s` or until consumed.
- Invincibility orb destroys touched obstacles for `5s`.
- Health orb restores `2` health up to the maximum limit.

### Dash Rules
- Dash requires a full `100%` meter.
- Dash lasts `3s`.
- Dash increases speed and can destroy breakable obstacles on contact.

### Charge Rules
- Charge consumes one charge use.
- Charge lasts `1s`.
- Charge cannot start during dash or when charge count is `0`.

### Mode Rules
- Cheat Mode and God Mode cannot be active at the same time.
- Cheat Mode keeps manual play intact but adds regeneration and softer collision punishment.
- God Mode automates hazard handling and prevents standard collision damage through autopilot responses.

### Pause, Restart, And Exit Rules
- Press `R` to pause or resume.
- Press `SPACE` on the game-over screen to restart with a fresh run.
- Press `ESC` to open exit confirmation, then `Y` to quit or `N` to cancel.
