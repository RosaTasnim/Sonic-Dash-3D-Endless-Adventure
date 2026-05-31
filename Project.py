"""
Sonic Dash - 3D Endless Adventure

[CONTROLS]
  [A] / [D]       : Switch Lanes
  [W] / [MWU]     : Jump
  [S] / [MWD]     : Slide
  [F] / [LMB]     : Charge
  [SPACE] / [RMB] : Dash

[OTHERS]
  [C]     : Cheat Mode
  [G]     : God Mode
  [V]     : First / Third Person
  [R]     : Pause / Resume Game
  [SPACE] : Start / Restart Game
  [ESC]   : Quit Game
"""

import time
import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLUT import GLUT_BITMAP_TIMES_ROMAN_24
from OpenGL.GLUT import GLUT_STROKE_ROMAN


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = b"Project: Sonic Dash - 3D Endless Adventure"

TAU = math.pi * 2

TRACK_FRONT_Z = 50
TRACK_BACK_Z = -500
TRACK_HALF_WIDTH = 20
LANE_SPACING = 10

GRAVITY = -50
JUMP_FORCE = 25
SLIDE_DURATION = 1
SLIDE_BUFFER_DURATION = 0.25
INVINCIBILITY_DURATION = 3
DASH_DURATION = 3
CHARGE_DURATION = 1
MAGNET_DURATION = 5
ORB_INVINCIBILITY_DURATION = 5
SHIELD_DURATION = 5
COUNTDOWN_DURATION = 3
MODE_HEALTH_RESTORE_DELAY = 0.75
MODE_HEALTH_RESTORE_STEP = 0.55
MODE_CHARGE_RESTORE_STEP = 0.65

INITIAL_SPEED = 50
SPEED_STEP = 5
MAX_BASE_SPEED = 100
DASH_SPEED_MULTIPLIER = 1.5
CHARGE_SPEED_MULTIPLIER = 1.25
MAX_FRAME_DT = 0.1
MAX_COLLISION_STEP_DISTANCE = 2.0

OBSTACLE_SPAWN_START = 1.5
OBSTACLE_SPAWN_MIN = 0.75
COLLECTIBLE_SPAWN_START = 2
COLLECTIBLE_SPAWN_MIN = 1
OBSTACLE_CLEARANCE_STEPS = 18
SPIKE_SAME_LANE_GAP = 110
BRANCH_BARRIER_SAME_LANE_GAP = 135
COLLECTIBLE_BLOCKER_GAP = 7.5
COLLECTIBLE_CLEARANCE_STEPS = 18

STARTING_RINGS = 0
PLAYER_MAX_HEALTH = 5
PLAYER_MAX_CHARGES = 5
PLAYER_RADIUS = 1.75

GOD_AUTOPILOT_LOOKAHEAD = 220
GOD_AUTOPILOT_BARRIER_SWITCH = 110
GOD_AUTOPILOT_CHARGE_TRIGGER = 45
GOD_AUTOPILOT_JUMP_TRIGGER = 40
GOD_AUTOPILOT_SLIDE_TRIGGER = 35
GOD_AUTOPILOT_FALLBACK_TRIGGER = 25

COL_SKY_TOP = (0.20, 0.75, 0.95)
COL_SKY_MID = (0.45, 0.85, 1.0)
COL_SKY_BOTTOM = (0.90, 0.95, 1.0)
COL_TRACK = (0.20, 0.30, 0.45)
COL_TRACK_EDGE = (0.10, 0.20, 0.35)
COL_LANE_GLOW = (0.30, 0.80, 1.0)
COL_SHOULDER_A = (0.20, 0.65, 0.25)
COL_SHOULDER_B = (0.10, 0.55, 0.20)
COL_HILL_GREEN = (0.20, 0.65, 0.25)
COL_HILL_DARK = (0.10, 0.50, 0.15)
COL_PALM_TRUNK = (0.55, 0.35, 0.10)
COL_PALM_LEAF = (0.15, 0.70, 0.25)
COL_ARCH = (1.0, 0.80, 0.10)
COL_ARCH_ALT = (0.95, 0.45, 0.15)
COL_PLAYER_BLUE = (0.10, 0.40, 0.95)
COL_PLAYER_LIGHT = (0.80, 0.90, 1.0)
COL_PLAYER_SKIN = (0.95, 0.85, 0.60)
COL_PLAYER_GLOVE = (0.95, 0.95, 1.0)
COL_PLAYER_CHEAT = (1.0, 0.70, 0.20)
COL_PLAYER_GOD = (1.0, 0.35, 0.55)
COL_RING = (1.0, 0.80, 0.10)
COL_DASH_BLUE = (0.35, 0.95, 1.0)
COL_DASH_ORB = (0.20, 0.95, 0.95)
COL_CHARGE_ORB = (0.20, 0.45, 1.0)
COL_MAGNET_ORB = (0.95, 0.20, 0.20)
COL_INVINCIBILITY_ORB = (1.0, 0.60, 0.15)
COL_HEALTH_ORB = (0.20, 0.90, 0.30)
COL_SHIELD_ORB = (0.72, 0.78, 0.86)
COL_SHIELD_NET = (0.86, 0.94, 1.0)
COL_BARRIER = (0.90, 0.30, 0.20)
COL_SPIKE = (0.85, 0.85, 0.90)
COL_BRANCH = (0.60, 0.30, 0.10)
COL_BADNIK = (0.70, 0.10, 0.15)
COL_BADNIK_EYE = (1.0, 0.95, 0.80)
COL_WHITE = (1.0, 1.0, 1.0)
COL_BLACK = (0.0, 0.0, 0.0)
COL_TEXT_DARK = (0.10, 0.15, 0.20)
COL_WARNING = (1.0, 0.40, 0.20)
COL_STEEL = (0.65, 0.75, 0.80)
COL_STEEL_DARK = (0.25, 0.30, 0.40)
COL_OBS_GLOW = (1.0, 0.75, 0.20)
COL_COOL_CYAN = (0.40, 0.95, 1.0)
COL_WARNING_STRIPE = (1.0, 0.90, 0.30)


window_id = 0
window_width = WINDOW_WIDTH
window_height = WINDOW_HEIGHT

quit_requested = False
exit_confirm_active = False
exit_confirm_return_state = "menu"

last_time = 0
game_state = "menu"
countdown_timer = COUNTDOWN_DURATION

base_speed = INITIAL_SPEED
current_speed = INITIAL_SPEED
speed_tier = 1
total_distance = 0
score = 0
obstacle_timer = 0
collectible_timer = 0
world_anim_time = 0

player_x = 0
player_y = 0
player_z = 0
player_lane_index = 1
player_velocity_y = 0
player_is_jumping = False
player_is_sliding = False
player_slide_timer = 0
player_slide_buffer_timer = 0
player_run_phase = 0
player_invincible_timer = 0
player_health = PLAYER_MAX_HEALTH
player_charge_count = PLAYER_MAX_CHARGES
player_rings = STARTING_RINGS
player_dash_meter = 0
player_is_dashing = False
player_dash_timer = 0
player_trail_timer = 0
player_is_charging = False
player_charge_timer = 0
player_charge_flash = 0
player_magnet_timer = 0
player_power_invincible_timer = 0
player_shield_timer = 0
player_hit_flash_timer = 0
player_hit_message_timer = 0
player_hit_message = ""
player_health_restore_delay_timer = 0
player_health_restore_step_timer = 0
player_charge_restore_step_timer = 0
player_cheat_dash_refill_timer = 0
player_cheat_mode = False
player_god_mode = False
god_autopilot_target_lane = 1
god_autopilot_focus_obstacle = None
god_autopilot_lane_lock_timer = 0

camera_mode = "third"

obstacles = []
collectibles = []
particles = []
hills = []
palms = []
arches = []


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def lane_to_x(lane):
    return (lane - 1) * LANE_SPACING


def color_scale(color, amount):
    return tuple(clamp(channel * amount, 0.0, 1.0) for channel in color)


def color_lerp(color_a, color_b, t):
    return (
        lerp(color_a[0], color_b[0], t),
        lerp(color_a[1], color_b[1], t),
        lerp(color_a[2], color_b[2], t),
    )


def world_time():
    return world_anim_time


def current_collectible_y(collectible):
    return collectible["y"] + math.sin(world_time() * 4.5 + collectible["phase"]) * 0.25


def obstacle_center_y(obstacle):
    if obstacle["type"] == "badnik":
        return obstacle["y"] + math.sin(world_time() * 4.0 + obstacle["phase"]) * 0.5
    return obstacle["y"]


def player_collision_center_y():
    if player_is_sliding:
        return player_y + 1.4
    if (player_is_dashing or player_is_charging) and not player_is_jumping:
        return player_y + 1.45
    if player_is_dashing or player_is_jumping:
        return player_y + 1.65
    return player_y + 2.4


def player_collectible_profile():
    if player_is_sliding or player_is_attacking() or player_is_jumping:
        center_y = player_y + player_roll_radius("jump") + 0.10
        radius = player_roll_radius("jump") * 1.18
        return center_y - radius, center_y + radius, radius * 1.02

    return player_y + 0.80, player_y + 4.45, 1.28


def collectible_contact_radius(collectible_type):
    if collectible_type == "ring":
        return 1.15
    return 1.08


def player_is_attacking():
    return player_is_dashing or player_is_charging


def current_player_form():
    if player_is_dashing:
        return "DASH", COL_DASH_BLUE
    if player_is_charging:
        return "CHARGE", COL_PLAYER_LIGHT
    if player_is_sliding:
        return "ROLL", COL_RING
    if player_is_jumping:
        return "JUMP", COL_RING
    return "RUN", COL_WHITE


def clear_hit_feedback():
    global player_hit_flash_timer, player_hit_message_timer, player_hit_message

    player_hit_flash_timer = 0
    player_hit_message_timer = 0
    player_hit_message = ""


def reset_god_autopilot_state():
    global god_autopilot_target_lane, god_autopilot_focus_obstacle, god_autopilot_lane_lock_timer

    god_autopilot_target_lane = player_lane_index
    god_autopilot_focus_obstacle = None
    god_autopilot_lane_lock_timer = 0


def register_mode_health_loss(amount):
    global player_health, player_health_restore_delay_timer, player_health_restore_step_timer

    player_health = max(0, player_health - amount)
    player_health_restore_delay_timer = MODE_HEALTH_RESTORE_DELAY
    player_health_restore_step_timer = 0


def open_exit_confirmation():
    global exit_confirm_active, exit_confirm_return_state

    exit_confirm_active = True
    exit_confirm_return_state = game_state
    log_event("SYSTEM", f"Exit confirmation opened")


def close_exit_confirmation():
    global exit_confirm_active, last_time

    exit_confirm_active = False
    last_time = time.time()
    log_event("SYSTEM", "Exit confirmation canceled")


def reset_mode_dash_state():
    global player_is_dashing, player_dash_timer, player_dash_meter, player_trail_timer
    global player_is_charging, player_charge_timer, player_charge_flash
    global player_cheat_dash_refill_timer

    player_is_dashing = False
    player_dash_timer = 0
    player_dash_meter = 0
    player_trail_timer = 0
    player_cheat_dash_refill_timer = 0
    player_is_charging = False
    player_charge_timer = 0
    player_charge_flash = 0


def toggle_cheat_mode():
    global player_cheat_mode, player_god_mode, player_dash_meter, player_health
    global player_health_restore_delay_timer, player_health_restore_step_timer, player_charge_restore_step_timer
    global player_cheat_dash_refill_timer

    if player_cheat_mode:
        player_cheat_mode = False
        reset_mode_dash_state()
        reset_god_autopilot_state()
        log_event("MODE", "Cheat mode disabled")
    else:
        reset_mode_dash_state()
        player_cheat_mode = True
        player_god_mode = False
        player_dash_meter = 0
        player_cheat_dash_refill_timer = 0
        player_health = PLAYER_MAX_HEALTH
        player_health_restore_delay_timer = 0
        player_health_restore_step_timer = 0
        player_charge_restore_step_timer = 0
        clear_hit_feedback()
        reset_god_autopilot_state()
        log_event("MODE", "Cheat mode enabled")


def toggle_god_mode():
    global player_cheat_mode, player_god_mode, player_dash_meter, player_charge_count
    global player_charge_restore_step_timer, player_cheat_dash_refill_timer

    if player_god_mode:
        player_god_mode = False
        reset_mode_dash_state()
        reset_god_autopilot_state()
        log_event("MODE", "God mode disabled")
    else:
        reset_mode_dash_state()
        player_god_mode = True
        player_cheat_mode = False
        player_dash_meter = 0
        player_cheat_dash_refill_timer = 0
        player_charge_count = PLAYER_MAX_CHARGES
        player_charge_restore_step_timer = 0
        clear_hit_feedback()
        reset_god_autopilot_state()
        log_event("MODE", "God mode enabled")


def obstacle_distance_ahead(obstacle):
    return -obstacle["z"]


def nearest_lane_index_from_x(x_pos):
    best_lane = 0
    best_distance = abs(x_pos - lane_to_x(0))

    for lane in range(1, 3):
        lane_distance = abs(x_pos - lane_to_x(lane))
        if lane_distance < best_distance:
            best_lane = lane
            best_distance = lane_distance

    return best_lane


def find_nearest_lane_obstacle(lane, max_distance=GOD_AUTOPILOT_LOOKAHEAD):
    nearest_obstacle = None
    nearest_distance = max_distance + 999

    for obstacle in obstacles:
        if obstacle["lane"] != lane:
            continue
        distance = obstacle_distance_ahead(obstacle)
        if distance < -obstacle["depth"] or distance > max_distance:
            continue
        if distance < nearest_distance:
            nearest_obstacle = obstacle
            nearest_distance = distance

    return nearest_obstacle, nearest_distance


def lane_switch_is_safe(lane):
    obstacle, distance = find_nearest_lane_obstacle(lane, 90)
    if obstacle is None:
        return True
    if obstacle["type"] == "barrier":
        return distance > 70
    return distance > 20


def adjacent_lanes(base_lane):
    lanes = []
    if base_lane > 0:
        lanes.append(base_lane - 1)
    if base_lane < 2:
        lanes.append(base_lane + 1)
    return lanes


def choose_barrier_escape_lane(base_lane=None):
    if base_lane is None:
        base_lane = god_autopilot_target_lane

    best_lane = None
    best_clearance = -1

    for lane in adjacent_lanes(base_lane):
        obstacle, distance = find_nearest_lane_obstacle(lane, 95)
        clearance = 999 if obstacle is None else distance
        if obstacle is not None and obstacle["type"] == "barrier" and clearance <= 70:
            continue
        if clearance <= 20:
            continue

        if clearance > best_clearance:
            best_clearance = clearance
            best_lane = lane
        elif clearance == best_clearance and best_lane is not None:
            if abs(lane - base_lane) < abs(best_lane - base_lane):
                best_lane = lane

    return best_lane


def choose_any_barrier_escape_lane(base_lane=None):
    if base_lane is None:
        base_lane = god_autopilot_target_lane

    best_lane = None
    best_clearance = -1

    for lane in range(3):
        if lane == base_lane:
            continue

        obstacle, distance = find_nearest_lane_obstacle(lane, 120)
        clearance = 999 if obstacle is None else distance
        if clearance > best_clearance:
            best_clearance = clearance
            best_lane = lane
        elif clearance == best_clearance and best_lane is not None:
            if abs(lane - base_lane) < abs(best_lane - base_lane):
                best_lane = lane

    return best_lane


def set_god_autopilot_lane(lane, lock_time=0):
    global player_lane_index, god_autopilot_target_lane, god_autopilot_lane_lock_timer

    current_lane = nearest_lane_index_from_x(player_x)
    if lane > current_lane + 1:
        lane = current_lane + 1
    elif lane < current_lane - 1:
        lane = current_lane - 1

    god_autopilot_target_lane = lane
    player_lane_index = lane
    god_autopilot_lane_lock_timer = max(god_autopilot_lane_lock_timer, lock_time)


def focus_obstacle_is_active():
    if god_autopilot_focus_obstacle is None:
        return False
    if god_autopilot_focus_obstacle not in obstacles:
        return False

    distance = obstacle_distance_ahead(god_autopilot_focus_obstacle)
    return -god_autopilot_focus_obstacle["depth"] < distance < GOD_AUTOPILOT_LOOKAHEAD


def acquire_god_focus_obstacle():
    global god_autopilot_focus_obstacle

    if focus_obstacle_is_active():
        return god_autopilot_focus_obstacle

    god_autopilot_focus_obstacle = None
    obstacle, _ = find_nearest_lane_obstacle(god_autopilot_target_lane, GOD_AUTOPILOT_LOOKAHEAD)
    if obstacle is not None:
        god_autopilot_focus_obstacle = obstacle
    return god_autopilot_focus_obstacle


def update_god_autopilot(dt):
    global god_autopilot_focus_obstacle, god_autopilot_lane_lock_timer

    if not player_god_mode or game_state != "playing":
        return

    if not player_is_dashing and player_dash_meter >= 100:
        start_dash()
        god_autopilot_focus_obstacle = None
        return

    if player_is_dashing:
        god_autopilot_focus_obstacle = None
        return

    if god_autopilot_lane_lock_timer > 0:
        god_autopilot_lane_lock_timer = max(0, god_autopilot_lane_lock_timer - dt)

    current_lane = nearest_lane_index_from_x(player_x)
    lane_delta = abs(player_x - lane_to_x(god_autopilot_target_lane))
    player_lane_index = god_autopilot_target_lane

    if lane_delta > 0.12:
        return

    focus_obstacle = acquire_god_focus_obstacle()
    if focus_obstacle is None:
        return

    obstacle_type = focus_obstacle["type"]
    current_distance = obstacle_distance_ahead(focus_obstacle)
    speed_factor = clamp((current_speed - INITIAL_SPEED) / 50, 0, 1)
    barrier_trigger = lerp(GOD_AUTOPILOT_BARRIER_SWITCH, 140, speed_factor)
    jump_trigger = lerp(GOD_AUTOPILOT_JUMP_TRIGGER, 58, speed_factor)
    slide_trigger = lerp(GOD_AUTOPILOT_SLIDE_TRIGGER, 54, speed_factor)
    charge_trigger = lerp(GOD_AUTOPILOT_CHARGE_TRIGGER, 56, speed_factor)
    emergency_trigger = focus_obstacle["depth"] * 0.5 + PLAYER_RADIUS + 1.5

    if obstacle_type == "barrier":
        if focus_obstacle["lane"] != god_autopilot_target_lane:
            god_autopilot_focus_obstacle = None
            return

        if current_distance < barrier_trigger and god_autopilot_lane_lock_timer <= 0:
            escape_lane = choose_barrier_escape_lane(current_lane)
            if escape_lane is not None and lane_switch_is_safe(escape_lane):
                set_god_autopilot_lane(escape_lane, 1.10)
                god_autopilot_focus_obstacle = None
                return

        if current_distance < emergency_trigger:
            force_god_mode_obstacle_action(focus_obstacle)
            return

    elif obstacle_type == "spike":
        if current_distance < jump_trigger and not player_is_jumping:
            start_jump()
            return
        if current_distance < emergency_trigger:
            force_god_mode_obstacle_action(focus_obstacle)
            return

    elif obstacle_type == "branch":
        if current_distance < slide_trigger and not player_is_sliding and not player_is_jumping:
            start_slide()
            return
        if current_distance < emergency_trigger:
            force_god_mode_obstacle_action(focus_obstacle)
            return

    elif obstacle_type == "badnik":
        if current_distance < charge_trigger:
            start_charge()
            return
        if current_distance < emergency_trigger:
            if force_god_mode_obstacle_action(focus_obstacle):
                destroy_obstacle(focus_obstacle, dash_smash=True)
            return

    if current_distance < -focus_obstacle["depth"]:
        god_autopilot_focus_obstacle = None


def trigger_hit_feedback(message, flash_time=0.55, text_time=0.95):
    global player_hit_flash_timer, player_hit_message_timer, player_hit_message

    player_hit_flash_timer = max(player_hit_flash_timer, flash_time)
    player_hit_message_timer = max(player_hit_message_timer, text_time)
    player_hit_message = message


def log_event(tag, message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] [{tag}] {message}")


def request_quit():
    global quit_requested
    quit_requested = True
    log_event("SYSTEM", "Quit requested")


def perform_quit():
    global window_id, quit_requested

    quit_requested = False
    log_event("SYSTEM", "Shutting down game")

    try:
        glutIdleFunc(None)
    except Exception:
        pass

    try:
        if callable(globals().get("glutLeaveMainLoop")):
            glutLeaveMainLoop()
    except Exception:
        pass

    if window_id:
        try:
            glutDestroyWindow(window_id)
        except Exception:
            pass
        window_id = 0


def start_jump():
    global player_is_jumping, player_velocity_y, player_is_sliding
    global player_slide_timer, player_slide_buffer_timer

    if player_is_jumping or player_y > 0.001:
        return

    player_is_jumping = True
    player_velocity_y = JUMP_FORCE
    player_is_sliding = False
    player_slide_timer = 0
    player_slide_buffer_timer = 0
    log_event("ACTION", "Jump started")


def start_slide():
    global player_is_sliding, player_slide_timer, player_slide_buffer_timer

    if player_is_jumping:
        player_slide_buffer_timer = SLIDE_BUFFER_DURATION
        log_event("ACTION", "Slide queued")
        return

    if player_is_dashing:
        return

    player_is_sliding = True
    player_slide_timer = SLIDE_DURATION
    player_slide_buffer_timer = 0
    log_event("ACTION", "Slide started")


def start_charge():
    global player_is_charging, player_charge_timer, player_charge_flash
    global player_charge_count, player_charge_restore_step_timer
    global player_is_sliding, player_slide_timer, player_slide_buffer_timer

    if player_is_dashing or player_is_charging:
        return

    if player_charge_count <= 0:
        return

    player_is_sliding = False
    player_slide_timer = 0
    player_slide_buffer_timer = 0
    player_is_charging = True
    player_charge_timer = CHARGE_DURATION
    player_charge_flash = 1
    player_charge_count = max(0, player_charge_count - 1)
    player_charge_restore_step_timer = 0
    spawn_particles(player_x, player_y + 1.1, player_z, COL_PLAYER_LIGHT, 15, 5, 3.5, 0.20, 0.45)
    log_event("ACTION", f"Charge started ({player_charge_count}/{PLAYER_MAX_CHARGES})")


def draw_text_raw(x, y, text, color, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))


def bitmap_text_width(text, font=GLUT_BITMAP_HELVETICA_18):
    pixel_width = 0
    for char in text:
        try:
            pixel_width += glutBitmapWidth(font, ord(char))
        except Exception:
            pixel_width += 14 if font == GLUT_BITMAP_TIMES_ROMAN_24 else 10
    return pixel_width * 2 / max(1, window_width)


def stroke_text_width(text):
    width = 0.0
    for char in text:
        try:
            width += glutStrokeWidth(GLUT_STROKE_ROMAN, ord(char))
        except Exception:
            width += 50 if char == " " else 100
    return width


def draw_text(x, y, text, color, font=GLUT_BITMAP_HELVETICA_18, shadow=True, shadow_color=None):
    if shadow:
        draw_text_raw(x + 0.005, y - 0.005, text, shadow_color or color_scale(COL_TEXT_DARK, 0.45), font)
    draw_text_raw(x, y, text, color, font)


def draw_centered_text(y, text, color, font=GLUT_BITMAP_HELVETICA_18, shadow=True, shadow_color=None):
    width = bitmap_text_width(text, font)
    draw_text(-width * 0.5, y, text, color, font, shadow=shadow, shadow_color=shadow_color)


def draw_stroke_text(x, y, text, color, scale=0.00025, centered=False, shadow=True, shadow_color=None, line_width=2.4):
    if centered:
        x -= stroke_text_width(text) * scale * 0.5

    if shadow:
        glPushMatrix()
        glTranslatef(x + 0.002, y - 0.01, 0)
        glScalef(scale, scale, 1)
        glLineWidth(line_width + 1)
        glColor3f(*(shadow_color or color_scale(COL_TEXT_DARK, 0.45)))
        for char in text:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
        glPopMatrix()

    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, 1)
    glLineWidth(line_width)
    glColor3f(*color)
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()
    glLineWidth(1)


def begin_2d():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)


def end_2d():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()


def draw_overlay_quad(x1, y1, x2, y2, color, alpha):
    glColor4f(color[0], color[1], color[2], alpha)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def draw_ui_panel(x1, y1, x2, y2, accent_color, alpha=0.30):
    draw_overlay_quad(x1, y1, x2, y2, COL_TEXT_DARK, alpha)
    draw_overlay_quad(x1, y2 - 0.015, x2, y2, accent_color, 0.95)
    draw_overlay_quad(x1, y1, x2, y1 + 0.005, color_scale(accent_color, 0.60), 0.40)


def draw_overlay_outline(x1, y1, x2, y2, color, width=1.6):
    glColor3f(*color)
    glLineWidth(width)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()
    glLineWidth(1.0)


def draw_box(x, y, z, sx, sy, sz, color):
    hx = sx * 0.5
    hy = sy * 0.5
    hz = sz * 0.5

    glPushMatrix()
    glTranslatef(x, y, z)

    glBegin(GL_QUADS)

    glColor3f(*color_scale(color, 1.10))
    glVertex3f(-hx, -hy, hz)
    glVertex3f(hx, -hy, hz)
    glVertex3f(hx, hy, hz)
    glVertex3f(-hx, hy, hz)

    glColor3f(*color_scale(color, 0.70))
    glVertex3f(-hx, -hy, -hz)
    glVertex3f(-hx, hy, -hz)
    glVertex3f(hx, hy, -hz)
    glVertex3f(hx, -hy, -hz)

    glColor3f(*color_scale(color, 1.0))
    glVertex3f(-hx, hy, -hz)
    glVertex3f(-hx, hy, hz)
    glVertex3f(hx, hy, hz)
    glVertex3f(hx, hy, -hz)

    glColor3f(*color_scale(color, 0.65))
    glVertex3f(-hx, -hy, -hz)
    glVertex3f(hx, -hy, -hz)
    glVertex3f(hx, -hy, hz)
    glVertex3f(-hx, -hy, hz)

    glColor3f(*color_scale(color, 0.90))
    glVertex3f(hx, -hy, -hz)
    glVertex3f(hx, hy, -hz)
    glVertex3f(hx, hy, hz)
    glVertex3f(hx, -hy, hz)

    glColor3f(*color_scale(color, 0.80))
    glVertex3f(-hx, -hy, -hz)
    glVertex3f(-hx, -hy, hz)
    glVertex3f(-hx, hy, hz)
    glVertex3f(-hx, hy, -hz)

    glEnd()
    glPopMatrix()


def draw_cylinder(radius, height, slices, color):
    glBegin(GL_QUADS)
    for index in range(slices):
        angle_1 = TAU * index / slices
        angle_2 = TAU * (index + 1) / slices

        x1 = math.cos(angle_1) * radius
        z1 = math.sin(angle_1) * radius
        x2 = math.cos(angle_2) * radius
        z2 = math.sin(angle_2) * radius

        shade = 0.75 + 0.25 * math.cos(angle_1)
        glColor3f(*color_scale(color, shade))
        glVertex3f(x1, 0, z1)
        glVertex3f(x2, 0, z2)
        glVertex3f(x2, height, z2)
        glVertex3f(x1, height, z1)
    glEnd()

    glColor3f(*color_scale(color, 0.60))
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for index in range(slices + 1):
        angle = TAU * index / slices
        glVertex3f(math.cos(angle) * radius, 0, math.sin(angle) * radius)
    glEnd()

    glColor3f(*color_scale(color, 1.05))
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, height, 0)
    for index in range(slices + 1):
        angle = TAU * index / slices
        glVertex3f(math.cos(angle) * radius, height, math.sin(angle) * radius)
    glEnd()


def draw_cone(radius, height, slices, color):
    glBegin(GL_TRIANGLES)
    for index in range(slices):
        angle_1 = TAU * index / slices
        angle_2 = TAU * (index + 1) / slices

        x1 = math.cos(angle_1) * radius
        z1 = math.sin(angle_1) * radius
        x2 = math.cos(angle_2) * radius
        z2 = math.sin(angle_2) * radius

        shade = 0.75 + 0.25 * math.cos(angle_1)
        glColor3f(*color_scale(color, shade))
        glVertex3f(0, height, 0)
        glVertex3f(x1, 0, z1)
        glVertex3f(x2, 0, z2)
    glEnd()

    glColor3f(*color_scale(color, 0.60))
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for index in range(slices + 1):
        angle = TAU * index / slices
        glVertex3f(math.cos(angle) * radius, 0, math.sin(angle) * radius)
    glEnd()


def draw_sphere(radius, color, slices=16, stacks=12):
    glColor3f(*color)
    glutSolidSphere(radius, slices, stacks)


def draw_translucent_sphere(radius, color, alpha, slices=16, stacks=12):
    glColor4f(color[0], color[1], color[2], alpha)
    glutSolidSphere(radius, slices, stacks)


def draw_ring_shape(outer_radius, inner_radius, color):
    segments = 40
    glBegin(GL_TRIANGLE_STRIP)
    for index in range(segments + 1):
        angle = TAU * index / segments
        c_val = math.cos(angle)
        s_val = math.sin(angle)
        glColor3f(*color_scale(color, 0.90 + 0.10 * c_val))
        glVertex3f(c_val * outer_radius, s_val * outer_radius, 0)
        glVertex3f(c_val * inner_radius, s_val * inner_radius, 0)
    glEnd()


def spawn_particles(x, y, z, color, count, speed=8, lift=5, size=0.25, life=0.5):
    for _ in range(count):
        particles.append(
            {
                "x": x,
                "y": y,
                "z": z,
                "vx": random.uniform(-speed, speed),
                "vy": random.uniform(-speed * 0.15, lift),
                "vz": random.uniform(-speed, speed),
                "life": random.uniform(life * 0.65, life * 1.15),
                "size": random.uniform(size * 0.7, size * 1.3),
                "color": color,
                "gravity": -8.0,
            }
        )


def spawn_dash_trail():
    for _ in range(2):
        particles.append(
            {
                "x": player_x + random.uniform(-0.8, 0.8),
                "y": player_y + 1.6 + random.uniform(-0.5, 0.5),
                "z": player_z + 0.6 + random.uniform(-0.3, 0.3),
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(-1.2, 1.4),
                "vz": random.uniform(6, 16),
                "life": random.uniform(0.20, 0.40),
                "size": random.uniform(0.30, 0.50),
                "color": COL_DASH_BLUE,
                "gravity": 0,
            }
        )


def spawn_hill(initial=False):
    side = random.choice([-1, 1])
    z_pos = random.uniform(-150, -950) if initial else random.uniform(-900, -1200)
    hills.append(
        {
            "x": side * random.uniform(65, 125),
            "z": z_pos,
            "radius": random.uniform(20, 35),
            "height": random.uniform(10, 20),
            "color": random.choice([COL_HILL_GREEN, COL_HILL_DARK]),
        }
    )


def spawn_palm(initial=False):
    side = random.choice([-1, 1])
    z_pos = random.uniform(-100, -900) if initial else random.uniform(-900, -1100)
    palms.append(
        {
            "x": side * random.uniform(30, 55),
            "z": z_pos,
            "height": random.uniform(8, 15),
            "tilt": side * random.uniform(4, 10),
            "leaf_len": random.uniform(4, 6),
            "sway": random.uniform(0, TAU),
        }
    )


def spawn_arch(initial=False):
    z_pos = random.uniform(-150, -1000) if initial else random.uniform(-950, -1300)
    arches.append(
        {
            "z": z_pos,
            "scale": random.uniform(0.9, 1.15),
            "color": random.choice([COL_ARCH, COL_ARCH_ALT]),
        }
    )


def init_environment():
    global hills, palms, arches

    hills = []
    palms = []
    arches = []

    for _ in range(12):
        spawn_hill(initial=True)

    for _ in range(18):
        spawn_palm(initial=True)

    for _ in range(7):
        spawn_arch(initial=True)


def reset_player():
    global player_x, player_y, player_z, player_lane_index, player_velocity_y
    global player_is_jumping, player_is_sliding, player_slide_timer, player_run_phase
    global player_slide_buffer_timer
    global player_invincible_timer, player_health, player_charge_count
    global player_rings, player_dash_meter
    global player_is_dashing, player_dash_timer, player_trail_timer
    global player_is_charging, player_charge_timer, player_charge_flash
    global player_magnet_timer, player_power_invincible_timer, player_shield_timer
    global player_hit_flash_timer, player_hit_message_timer, player_hit_message
    global player_health_restore_delay_timer, player_health_restore_step_timer, player_charge_restore_step_timer
    global god_autopilot_target_lane, god_autopilot_focus_obstacle, god_autopilot_lane_lock_timer

    player_x = 0
    player_y = 0
    player_z = 0
    player_lane_index = 1
    player_velocity_y = 0
    player_is_jumping = False
    player_is_sliding = False
    player_slide_timer = 0
    player_slide_buffer_timer = 0
    player_run_phase = 0
    player_invincible_timer = 0
    player_health = PLAYER_MAX_HEALTH
    player_charge_count = PLAYER_MAX_CHARGES
    player_rings = STARTING_RINGS
    player_dash_meter = 0
    player_is_dashing = False
    player_dash_timer = 0
    player_trail_timer = 0
    player_is_charging = False
    player_charge_timer = 0
    player_charge_flash = 0
    player_magnet_timer = 0
    player_power_invincible_timer = 0
    player_shield_timer = 0
    player_hit_flash_timer = 0
    player_hit_message_timer = 0
    player_hit_message = ""
    player_health_restore_delay_timer = 0
    player_health_restore_step_timer = 0
    player_charge_restore_step_timer = 0
    player_cheat_dash_refill_timer = 0
    god_autopilot_target_lane = 1
    god_autopilot_focus_obstacle = None
    god_autopilot_lane_lock_timer = 0


def start_new_run(menu_only=False):
    global game_state, last_time, countdown_timer
    global base_speed, current_speed, speed_tier, total_distance, score
    global obstacle_timer, collectible_timer, obstacles, collectibles, particles
    global exit_confirm_active, exit_confirm_return_state
    global world_anim_time

    reset_player()
    init_environment()

    base_speed = INITIAL_SPEED
    current_speed = INITIAL_SPEED
    speed_tier = 1
    total_distance = 0
    score = 0
    obstacle_timer = 0.85
    collectible_timer = 0.30
    countdown_timer = COUNTDOWN_DURATION

    obstacles = []
    collectibles = []
    particles = []
    exit_confirm_active = False
    exit_confirm_return_state = "menu"
    world_anim_time = 0

    game_state = "menu" if menu_only else "countdown"
    last_time = time.time()
    if menu_only:
        log_event("GAME", "Returned to menu")
    else:
        log_event("GAME", "New run started")


def init_game():
    start_new_run(menu_only=True)


def start_dash():
    global player_is_dashing, player_dash_timer, player_dash_meter
    global player_is_sliding, player_slide_timer, player_invincible_timer
    global player_is_charging, player_charge_timer, player_charge_flash
    global player_slide_buffer_timer, player_cheat_dash_refill_timer

    player_is_dashing = True
    player_dash_timer = DASH_DURATION
    player_dash_meter = 100 if player_cheat_mode else 0
    player_cheat_dash_refill_timer = 0
    player_is_sliding = False
    player_slide_timer = 0
    player_slide_buffer_timer = 0
    player_is_charging = False
    player_charge_timer = 0
    player_charge_flash = 1
    player_invincible_timer = max(player_invincible_timer, 0.2)
    spawn_particles(player_x, player_y + 1.8, player_z, COL_DASH_BLUE, 16, 6, 5, 0.30, 0.55)
    log_event("ACTION", "Dash started")


def take_damage(amount=1, source_label="HIT"):
    global player_health, player_invincible_timer

    player_health = max(0, player_health - amount)
    burst_color = COL_WARNING if player_health > 0 else COL_WARNING_STRIPE
    spawn_particles(player_x, player_y + 1.8, player_z, burst_color, 14 + amount * 4, 10, 7, 0.25, 0.85)
    player_invincible_timer = INVINCIBILITY_DURATION
    trigger_hit_feedback(f"{source_label} - HP {player_health}/{PLAYER_MAX_HEALTH}", flash_time=0.70, text_time=1.10)
    log_event("DAMAGE", f"{source_label} for {amount} (HP {player_health}/{PLAYER_MAX_HEALTH})")


def required_same_lane_obstacle_gap(new_type, existing_type):
    if new_type == "spike" and existing_type == "spike":
        return SPIKE_SAME_LANE_GAP

    if {new_type, existing_type} == {"branch", "barrier"}:
        return BRANCH_BARRIER_SAME_LANE_GAP

    return 0


def find_clear_obstacle_spawn_z(obstacle_type, lane, z_pos):
    adjusted_z = z_pos

    for _ in range(OBSTACLE_CLEARANCE_STEPS):
        changed = False
        for obstacle in obstacles:
            if obstacle["lane"] != lane:
                continue

            required_gap = required_same_lane_obstacle_gap(obstacle_type, obstacle["type"])
            if required_gap <= 0:
                continue

            if abs(obstacle["z"] - adjusted_z) < required_gap:
                adjusted_z = min(adjusted_z, obstacle["z"] - required_gap)
                changed = True
        if not changed:
            break

    return adjusted_z


def collectible_overlaps_obstacle(lane, z_pos, y_pos, collectible_type):
    collectible_half_height = 1.15 if collectible_type == "ring" else 0.95

    for obstacle in obstacles:
        if obstacle["lane"] != lane:
            continue

        obstacle_half_height = obstacle["height"] * 0.5
        obstacle_min_y = obstacle["y"] - obstacle_half_height
        obstacle_max_y = obstacle["y"] + obstacle_half_height
        collectible_min_y = y_pos - collectible_half_height
        collectible_max_y = y_pos + collectible_half_height

        if collectible_max_y < obstacle_min_y or collectible_min_y > obstacle_max_y:
            continue

        required_gap = obstacle["depth"] * 0.5 + COLLECTIBLE_BLOCKER_GAP
        if abs(z_pos - obstacle["z"]) <= required_gap:
            return obstacle

    return None


def find_clear_collectible_z(lane, z_pos, y_pos, collectible_type):
    adjusted_z = z_pos

    for _ in range(COLLECTIBLE_CLEARANCE_STEPS):
        blocking_obstacle = collectible_overlaps_obstacle(lane, adjusted_z, y_pos, collectible_type)
        if blocking_obstacle is None:
            return adjusted_z

        adjusted_z = blocking_obstacle["z"] + blocking_obstacle["depth"] * 0.5 + COLLECTIBLE_BLOCKER_GAP

    return adjusted_z


def spawn_obstacle(obstacle_type, lane, z_pos):
    x_pos = lane_to_x(lane)
    z_pos = find_clear_obstacle_spawn_z(obstacle_type, lane, z_pos)

    if obstacle_type == "barrier":
        obstacles.append(
            {
                "type": "barrier",
                "lane": lane,
                "x": x_pos,
                "y": 2.6,
                "z": z_pos,
                "width": 6.2,
                "height": 5.4,
                "depth": 4.4,
                "breakable": True,
                "score": 35,
                "phase": random.uniform(0.0, TAU),
            }
        )
    elif obstacle_type == "spike":
        obstacles.append(
            {
                "type": "spike",
                "lane": lane,
                "x": x_pos,
                "y": 1.0,
                "z": z_pos,
                "width": 6.8,
                "height": 2.4,
                "depth": 4.8,
                "breakable": True,
                "score": 25,
                "phase": random.uniform(0.0, TAU),
            }
        )
    elif obstacle_type == "branch":
        obstacles.append(
            {
                "type": "branch",
                "lane": lane,
                "x": x_pos,
                "y": 4.45,
                "z": z_pos,
                "width": 6.6,
                "height": 1.1,
                "depth": 3.0,
                "breakable": True,
                "score": 30,
                "phase": random.uniform(0.0, TAU),
            }
        )
    elif obstacle_type == "badnik":
        obstacles.append(
            {
                "type": "badnik",
                "lane": lane,
                "x": x_pos,
                "y": 3.0,
                "z": z_pos,
                "width": 4.4,
                "height": 4.4,
                "depth": 4.4,
                "breakable": True,
                "score": 45,
                "phase": random.uniform(0.0, TAU),
                "rot": random.uniform(0.0, 360.0),
            }
        )


def spawn_ring_chain(lane, front_z, count, arc=False):
    previous_z = None

    for index in range(count):
        ratio = index / max(1, count - 1)
        if arc:
            y_pos = 2 + math.sin(ratio * math.pi) * 3.4
        else:
            y_pos = 2.2

        z_pos = find_clear_collectible_z(lane, front_z - index * 12, y_pos, "ring")
        if previous_z is not None:
            z_pos = min(z_pos, previous_z - 8)
            z_pos = find_clear_collectible_z(lane, z_pos, y_pos, "ring")
        previous_z = z_pos

        collectibles.append(
            {
                "type": "ring",
                "lane": lane,
                "x": lane_to_x(lane),
                "base_x": lane_to_x(lane),
                "y": y_pos,
                "base_y": y_pos,
                "z": z_pos,
                "value": 10,
                "rot": random.uniform(0, 360),
                "phase": random.uniform(0, TAU),
                "magnetized": False,
            }
        )


def spawn_special_orb(collectible_type, lane, z_pos, y_pos=4.0):
    value_map = {
        "dash_orb": 35,
        "shield_orb": 45,
        "magnet_orb": 55,
        "charge_orb": 65,
        "invincibility_orb": 75,
        "health_orb": 85,
    }
    z_pos = find_clear_collectible_z(lane, z_pos, y_pos, collectible_type)
    collectibles.append(
        {
            "type": collectible_type,
            "lane": lane,
            "x": lane_to_x(lane),
            "y": y_pos,
            "z": z_pos,
            "value": value_map[collectible_type],
            "rot": random.uniform(0, 360),
            "phase": random.uniform(0, TAU),
        }
    )


def spawn_random_orb(lane, z_pos, y_pos=4):
    roll = random.random()
    if roll < 0.4:
        spawn_special_orb("dash_orb", lane, z_pos, y_pos)
    elif roll < 0.5:
        spawn_special_orb("shield_orb", lane, z_pos, y_pos)
    elif roll < 0.6:
        spawn_special_orb("magnet_orb", lane, z_pos, y_pos)
    elif roll < 0.7:
        spawn_special_orb("charge_orb", lane, z_pos, y_pos)
    elif roll < 0.8:
        spawn_special_orb("invincibility_orb", lane, z_pos, y_pos)
    else:
        spawn_special_orb("health_orb", lane, z_pos, y_pos)


def build_spawn_patterns():
    patterns = [
        [(0, "barrier")],
        [(1, "barrier")],
        [(2, "barrier")],
        [(0, "spike")],
        [(1, "spike")],
        [(2, "spike")],
    ]

    if total_distance >= 180:
        patterns.extend(
            [
                [(0, "barrier"), (2, "barrier")],
                [(0, "spike"), (2, "spike")],
                [(0, "barrier"), (1, "spike")],
                [(1, "barrier"), (2, "spike")],
            ]
        )

    if total_distance >= 420:
        patterns.extend(
            [
                [(0, "branch")],
                [(1, "branch")],
                [(2, "branch")],
                [(0, "branch"), (1, "barrier")],
                [(2, "branch"), (1, "spike")],
                [(0, "barrier"), (2, "branch")],
            ]
        )

    if total_distance >= 820:
        patterns.extend(
            [
                [(0, "badnik")],
                [(1, "badnik")],
                [(2, "badnik")],
                [(1, "badnik"), (2, "branch")],
            ]
        )

    return patterns


def spawn_wave_collectibles(pattern, z_pos):
    if len(collectibles) > 20:
        return

    blocked_lanes = {lane for lane, _ in pattern}
    safe_lanes = [lane for lane in (0, 1, 2) if lane not in blocked_lanes]

    if safe_lanes and random.random() < 0.82:
        ring_lane = random.choice(safe_lanes)
        spawn_ring_chain(ring_lane, z_pos + random.uniform(100, 140), random.randint(5, 7), arc=False)

    spike_lanes = [lane for lane, obstacle_type in pattern if obstacle_type == "spike"]
    if spike_lanes and random.random() < 0.48:
        spawn_ring_chain(random.choice(spike_lanes), z_pos + 72, 4, arc=True)

    if safe_lanes and random.random() < 0.12:
        spawn_random_orb(random.choice(safe_lanes), z_pos + 78, 4.3)


def spawn_obstacle_wave():
    z_pos = TRACK_BACK_Z
    pattern = random.choice(build_spawn_patterns())

    for lane, obstacle_type in pattern:
        spawn_obstacle(obstacle_type, lane, z_pos)

    spawn_wave_collectibles(pattern, z_pos)


def spawn_bonus_collectibles():
    if len(collectibles) > 18:
        return

    lane = random.randint(0, 2)
    z_pos = TRACK_BACK_Z + random.uniform(110, 155)

    if total_distance > 250 and random.random() < 0.14:
        spawn_random_orb(lane, z_pos, 4.0)
    else:
        arc = total_distance > 280 and random.random() < 0.26
        spawn_ring_chain(lane, z_pos, random.randint(4, 6), arc=arc)


def update_environment(distance_delta):
    global hills, palms, arches

    for hill in hills:
        hill["z"] += distance_delta * 0.55

    for palm in palms:
        palm["z"] += distance_delta
        palm["sway"] += distance_delta * 0.01

    for arch in arches:
        arch["z"] += distance_delta

    hills = [hill for hill in hills if hill["z"] < 120]
    palms = [palm for palm in palms if palm["z"] < 90]
    arches = [arch for arch in arches if arch["z"] < 90]

    while len(hills) < 12:
        spawn_hill()

    while len(palms) < 18:
        spawn_palm()

    while len(arches) < 7:
        spawn_arch()


def update_player(dt):
    global player_x, player_y, player_velocity_y, player_is_jumping
    global player_is_sliding, player_slide_timer, player_run_phase
    global player_slide_buffer_timer
    global player_invincible_timer, player_is_dashing, player_dash_timer
    global player_trail_timer, player_is_charging, player_charge_timer
    global player_magnet_timer, player_power_invincible_timer, player_shield_timer
    global player_charge_flash, player_hit_flash_timer, player_hit_message_timer
    global player_hit_message, player_dash_meter, player_cheat_dash_refill_timer

    target_x = lane_to_x(player_lane_index)
    player_x = lerp(player_x, target_x, clamp(dt * 11, 0, 1))

    if player_is_jumping:
        player_y += player_velocity_y * dt
        player_velocity_y += GRAVITY * dt
        if player_y <= 0:
            player_y = 0
            player_velocity_y = 0
            player_is_jumping = False
            log_event("ACTION", "Jump ended")
            spawn_particles(player_x, 0.25, player_z, COL_WHITE, 4, 2, 2, 0.14, 0.25)
            if player_slide_buffer_timer > 0 and not player_is_attacking():
                player_is_sliding = True
                player_slide_timer = SLIDE_DURATION
                player_slide_buffer_timer = 0

    if player_slide_buffer_timer > 0:
        player_slide_buffer_timer = max(0, player_slide_buffer_timer - dt)

    if player_is_sliding:
        player_slide_timer -= dt
        if player_slide_timer <= 0:
            player_is_sliding = False
            player_slide_timer = 0
            log_event("ACTION", "Slide ended")

    if player_is_charging:
        player_charge_timer -= dt
        if player_charge_timer <= 0:
            player_is_charging = False
            player_charge_timer = 0
            log_event("ACTION", "Charge ended")
        elif player_y <= 0.001 and random.random() < 0.35:
            spawn_particles(player_x, 0.5, player_z, COL_PLAYER_LIGHT, 2, 1.5, 2.2, 0.10, 0.20)

    if player_invincible_timer > 0:
        player_invincible_timer = max(0, player_invincible_timer - dt)
        if player_invincible_timer <= 0:
            log_event("STATUS", "Hit recovery ended")

    if player_charge_flash > 0:
        player_charge_flash = max(0, player_charge_flash - dt * 2.8)

    if player_magnet_timer > 0:
        player_magnet_timer = max(0, player_magnet_timer - dt)
        if player_magnet_timer <= 0:
            log_event("STATUS", "Magnet ended")

    if player_power_invincible_timer > 0:
        player_power_invincible_timer = max(0, player_power_invincible_timer - dt)
        if player_power_invincible_timer <= 0:
            log_event("STATUS", "Invincibility ended")

    if player_shield_timer > 0:
        player_shield_timer = max(0, player_shield_timer - dt)
        if player_shield_timer <= 0:
            log_event("STATUS", "Shield ended")

    if player_hit_flash_timer > 0:
        player_hit_flash_timer = max(0, player_hit_flash_timer - dt * 1.7)

    if player_hit_message_timer > 0:
        player_hit_message_timer = max(0, player_hit_message_timer - dt)
        if player_hit_message_timer <= 0:
            player_hit_message = ""

    if player_is_dashing:
        player_dash_timer -= dt
        player_trail_timer -= dt
        player_dash_meter = max(0, 100 * (player_dash_timer / float(DASH_DURATION)))
        if player_trail_timer <= 0:
            spawn_dash_trail()
            player_trail_timer = 0.03
        if player_dash_timer <= 0:
            player_is_dashing = False
            player_dash_timer = 0
            player_dash_meter = 0
            log_event("ACTION", "Dash ended")
            if player_cheat_mode:
                player_cheat_dash_refill_timer = 0

    run_rate = 5.5 + current_speed * 0.08
    player_run_phase += dt * run_rate
    if player_run_phase > TAU:
        player_run_phase -= TAU


def update_obstacles(dt, distance_delta):
    global obstacles

    for obstacle in obstacles[:]:
        obstacle["z"] += distance_delta
        if obstacle["type"] == "badnik":
            obstacle["rot"] += dt * 220
        if obstacle["z"] > 20:
            obstacles.remove(obstacle)


def update_collectibles(dt, distance_delta):
    global collectibles

    for collectible in collectibles[:]:
        collectible["z"] += distance_delta
        collectible["rot"] += dt * 180

        if collectible["type"] == "ring" and player_magnet_timer > 0.0:
            collectible["magnetized"] = True
            target_y = player_collision_center_y() - 0.3
            dx = player_x - collectible["x"]
            dy = target_y - collectible["y"]
            dz = player_z - collectible["z"]
            distance = math.sqrt(dx * dx + dy * dy + dz * dz)
            if distance > 0.001:
                pull_step = min(distance, 96 * dt)
                collectible["x"] += dx / distance * pull_step
                collectible["y"] += dy / distance * pull_step
                collectible["z"] += dz / distance * pull_step
        elif collectible["type"] == "ring" and collectible.get("magnetized"):
            collectible["x"] = collectible.get("base_x", lane_to_x(collectible["lane"]))
            collectible["y"] = collectible.get("base_y", collectible["y"])
            collectible["magnetized"] = False

        remove_limit = 80 if collectible["type"] == "ring" and player_magnet_timer > 0 else 22
        if collectible["z"] > remove_limit:
            collectibles.remove(collectible)


def update_particles(dt):
    global particles

    for particle in particles[:]:
        particle["x"] += particle["vx"] * dt
        particle["y"] += particle["vy"] * dt
        particle["z"] += particle["vz"] * dt
        particle["vy"] += particle.get("gravity", -8) * dt
        particle["life"] -= dt
        if particle["life"] <= 0:
            particles.remove(particle)


def obstacle_cleared(obstacle):
    if obstacle["type"] == "spike":
        return player_y > 3.1
    if obstacle["type"] == "branch":
        return player_is_sliding
    if obstacle["type"] == "badnik":
        return player_is_jumping and player_collision_center_y() > obstacle_center_y(obstacle) + obstacle["height"] * 0.40
    return False


def force_god_mode_obstacle_action(obstacle):
    global player_x, player_y, player_velocity_y, player_is_jumping
    global player_is_sliding, player_slide_timer, player_slide_buffer_timer
    global player_is_charging, player_charge_timer, player_charge_flash
    global god_autopilot_focus_obstacle

    obstacle_type = obstacle["type"]

    if obstacle_type == "barrier":
        current_lane = nearest_lane_index_from_x(player_x)
        escape_lane = choose_barrier_escape_lane(current_lane)
        if escape_lane is None:
            escape_lane = choose_any_barrier_escape_lane(current_lane)
        if escape_lane is None:
            options = adjacent_lanes(current_lane)
            if options:
                escape_lane = options[0]
        if escape_lane is not None and escape_lane != current_lane:
            set_god_autopilot_lane(escape_lane, 1.10)
            player_x = lane_to_x(escape_lane)
            god_autopilot_focus_obstacle = None
            return True
        return False

    if obstacle_type == "spike":
        if player_is_jumping or player_y > 0.001:
            return True
        start_jump()
        player_is_jumping = True
        player_is_sliding = False
        player_slide_timer = 0
        player_slide_buffer_timer = 0
        player_y = max(player_y, 3.4)
        player_velocity_y = max(player_velocity_y, 0)
        return True

    if obstacle_type == "branch":
        player_is_jumping = False
        player_y = 0
        player_velocity_y = 0
        player_is_sliding = True
        player_slide_timer = max(player_slide_timer, SLIDE_DURATION)
        player_slide_buffer_timer = 0
        return True

    if obstacle_type == "badnik":
        start_charge()
        player_is_charging = True
        player_charge_timer = max(player_charge_timer, CHARGE_DURATION)
        player_charge_flash = 1
        return True

    return False


def destroy_obstacle(obstacle, dash_smash=False, burst_color=None):
    global score

    if obstacle in obstacles:
        obstacles.remove(obstacle)
    score += obstacle["score"]
    if dash_smash:
        log_event("SMASH", f"{obstacle['type']} smashed")
    effect_color = burst_color or (COL_DASH_BLUE if dash_smash else COL_WARNING)
    spawn_particles(obstacle["x"], obstacle_center_y(obstacle), obstacle["z"], effect_color, 14, 10, 7, 0.22, 0.55)


def handle_collectible_pickup(collectible):
    global player_rings, player_dash_meter, score, player_health
    global player_charge_count, player_magnet_timer, player_power_invincible_timer, player_shield_timer

    if collectible in collectibles:
        collectibles.remove(collectible)

    if collectible["type"] == "ring":
        player_rings += 1
        if not player_cheat_mode:
            player_dash_meter = min(100, player_dash_meter + 1)
        score += collectible["value"]
        spawn_particles(collectible["x"], collectible["y"], collectible["z"], COL_RING, 8, 4, 3, 0.12, 0.35)
    elif collectible["type"] == "dash_orb":
        if not player_cheat_mode:
            player_dash_meter = min(100, player_dash_meter + 5)
        score += collectible["value"]
        spawn_particles(collectible["x"], collectible["y"], collectible["z"], COL_DASH_BLUE, 12, 5, 3.5, 0.18, 0.45)
        log_event("PICKUP", f"Dash orb collected (dash {int(player_dash_meter)}%)")
    elif collectible["type"] == "charge_orb":
        player_charge_count = PLAYER_MAX_CHARGES
        score += collectible["value"]
        spawn_particles(collectible["x"], collectible["y"], collectible["z"], COL_CHARGE_ORB, 12, 5, 3.6, 0.18, 0.45)
        log_event("PICKUP", "Charge orb collected (charge reset)")
    elif collectible["type"] == "magnet_orb":
        player_magnet_timer = MAGNET_DURATION
        score += collectible["value"]
        spawn_particles(collectible["x"], collectible["y"], collectible["z"], COL_MAGNET_ORB, 12, 5, 3.6, 0.18, 0.45)
        log_event("PICKUP", f"Magnet orb collected ({MAGNET_DURATION}s)")
    elif collectible["type"] == "shield_orb":
        player_shield_timer = SHIELD_DURATION
        score += collectible["value"]
        spawn_particles(collectible["x"], collectible["y"], collectible["z"], COL_SHIELD_ORB, 14, 5.1, 3.8, 0.18, 0.48)
        log_event("PICKUP", f"Shield orb collected ({SHIELD_DURATION}s)")
    elif collectible["type"] == "invincibility_orb":
        player_power_invincible_timer = ORB_INVINCIBILITY_DURATION
        score += collectible["value"]
        spawn_particles(collectible["x"], collectible["y"], collectible["z"], COL_INVINCIBILITY_ORB, 14, 5.2, 3.8, 0.20, 0.48)
        log_event("PICKUP", f"Invincibility orb collected ({ORB_INVINCIBILITY_DURATION}s)")
    elif collectible["type"] == "health_orb":
        player_health = min(PLAYER_MAX_HEALTH, player_health + 2)
        score += collectible["value"]
        spawn_particles(collectible["x"], collectible["y"], collectible["z"], COL_HEALTH_ORB, 16, 5.4, 4, 0.20, 0.50)
        log_event("PICKUP", f"Health orb collected (HP {player_health}/{PLAYER_MAX_HEALTH})")


def check_collectible_collisions():
    player_cx = player_x
    player_cz = player_z
    player_min_y, player_max_y, player_pickup_radius = player_collectible_profile()

    for collectible in collectibles[:]:
        collectible_y = current_collectible_y(collectible)
        closest_player_y = clamp(collectible_y, player_min_y, player_max_y)
        dy = collectible_y - closest_player_y
        dx = collectible["x"] - player_cx
        dz = collectible["z"] - player_cz
        pickup_radius = player_pickup_radius + collectible_contact_radius(collectible["type"])
        if player_magnet_timer > 0 and collectible["type"] == "ring":
            pickup_radius += 2.0

        if dx * dx + dy * dy + dz * dz <= pickup_radius * pickup_radius:
            handle_collectible_pickup(collectible)


def check_obstacle_collisions():
    global game_state, player_health, player_charge_count, god_autopilot_focus_obstacle, player_x, player_shield_timer

    for obstacle in obstacles[:]:
        dx = abs(obstacle["x"] - player_x)
        dz = abs(obstacle["z"] - player_z)

        if dx > obstacle["width"] * 0.5 + PLAYER_RADIUS:
            continue
        if dz > obstacle["depth"] * 0.5 + PLAYER_RADIUS:
            continue

        if player_power_invincible_timer > 0.0 and not player_god_mode:
            destroy_obstacle(obstacle, dash_smash=True)
            continue

        attack_can_smash = player_is_dashing or not player_god_mode or obstacle["type"] == "badnik"
        if player_is_attacking() and obstacle["breakable"] and attack_can_smash:
            if obstacle["type"] == "badnik" and player_is_charging:
                if player_charge_count < PLAYER_MAX_CHARGES:
                    player_charge_count += 1
                    spawn_particles(obstacle["x"], obstacle_center_y(obstacle), obstacle["z"], COL_CHARGE_ORB, 8, 6.0, 4.0, 0.16, 0.35)
            destroy_obstacle(obstacle, dash_smash=True)
            continue

        if obstacle_cleared(obstacle):
            continue

        if player_shield_timer > 0.0 and not player_god_mode:
            player_shield_timer = 0
            spawn_particles(player_x, player_collision_center_y(), player_z, COL_SHIELD_NET, 16, 8.8, 6.2, 0.18, 0.42)
            destroy_obstacle(obstacle, burst_color=COL_SHIELD_NET)
            log_event("SHIELD", f"{obstacle['type']} blocked and shield broke")
            continue

        if player_invincible_timer > 0.0 and not player_is_attacking():
            continue

        if player_cheat_mode:
            clear_hit_feedback()
            register_mode_health_loss(2 if obstacle["type"] == "badnik" else 1)
            destroy_obstacle(obstacle, dash_smash=True)
            continue

        if player_god_mode:
            if force_god_mode_obstacle_action(obstacle):
                if obstacle["type"] == "badnik":
                    destroy_obstacle(obstacle, dash_smash=True)
            continue

        damage = 2 if obstacle["type"] == "badnik" else 1
        source_label = "BADNIK HIT" if obstacle["type"] == "badnik" else "HIT"
        take_damage(damage, source_label)
        destroy_obstacle(obstacle, dash_smash=False)
        if player_health <= 0:
            player_health = 0
            trigger_hit_feedback("CRASH", flash_time=0.85, text_time=1.1)
            spawn_particles(player_x, player_collision_center_y(), player_z, COL_WARNING, 18, 11.0, 8.0, 0.22, 0.85)
            game_state = "gameover"
            log_event("GAME", f"Game over (score {int(score)}, distance {int(total_distance)}m)")
            break


def update_difficulty():
    global speed_tier, base_speed

    speed_tier = int(total_distance // 250.0) + 1
    base_speed = min(MAX_BASE_SPEED, INITIAL_SPEED + (speed_tier - 1) * SPEED_STEP)


def current_speed_multiplier():
    if player_is_dashing:
        return DASH_SPEED_MULTIPLIER
    if player_is_charging:
        return CHARGE_SPEED_MULTIPLIER
    return 1.0


def target_player_speed():
    return base_speed * current_speed_multiplier()


def simulation_step_dt(remaining_dt):
    step_speed = max(INITIAL_SPEED, current_speed, target_player_speed())
    max_step = MAX_COLLISION_STEP_DISTANCE / max(1.0, step_speed)
    return min(remaining_dt, max_step)


def update_mode_regeneration(dt):
    global player_health, player_charge_count
    global player_health_restore_delay_timer, player_health_restore_step_timer, player_charge_restore_step_timer

    if player_cheat_mode:
        if player_health_restore_delay_timer > 0:
            player_health_restore_delay_timer = max(0, player_health_restore_delay_timer - dt)
        elif player_health < PLAYER_MAX_HEALTH:
            player_health_restore_step_timer += dt
            while player_health_restore_step_timer >= MODE_HEALTH_RESTORE_STEP and player_health < PLAYER_MAX_HEALTH:
                player_health += 1
                player_health_restore_step_timer -= MODE_HEALTH_RESTORE_STEP

        if player_charge_count < PLAYER_MAX_CHARGES:
            player_charge_restore_step_timer += dt
            while player_charge_restore_step_timer >= MODE_CHARGE_RESTORE_STEP and player_charge_count < PLAYER_MAX_CHARGES:
                player_charge_count += 1
                player_charge_restore_step_timer -= MODE_CHARGE_RESTORE_STEP
        else:
            player_charge_restore_step_timer = 0
    elif player_god_mode:
        if player_charge_count < PLAYER_MAX_CHARGES:
            player_charge_restore_step_timer += dt
            while player_charge_restore_step_timer >= MODE_CHARGE_RESTORE_STEP and player_charge_count < PLAYER_MAX_CHARGES:
                player_charge_count += 1
                player_charge_restore_step_timer -= MODE_CHARGE_RESTORE_STEP
        else:
            player_charge_restore_step_timer = 0


def update_playing_step(dt):
    global current_speed, total_distance, score, obstacle_timer, collectible_timer
    global world_anim_time, player_cheat_dash_refill_timer, player_dash_meter

    world_anim_time += dt
    update_difficulty()
    update_mode_regeneration(dt)
    update_god_autopilot(dt)

    target_speed = target_player_speed()
    current_speed = lerp(current_speed, target_speed, clamp(dt * 3.0, 0.0, 1.0))

    distance_delta = current_speed * dt
    total_distance += distance_delta
    score += distance_delta * 0.34

    update_player(dt)
    if player_cheat_mode and not player_is_dashing:
        player_cheat_dash_refill_timer = min(DASH_DURATION, player_cheat_dash_refill_timer + dt)
        player_dash_meter = min(100, (player_cheat_dash_refill_timer / float(DASH_DURATION)) * 100)

    update_environment(distance_delta)
    update_obstacles(dt, distance_delta)
    update_collectibles(dt, distance_delta)
    update_particles(dt)

    obstacle_timer -= dt
    collectible_timer -= dt

    while obstacle_timer <= 0.0 and game_state == "playing":
        spawn_obstacle_wave()
        obstacle_timer += max(
            OBSTACLE_SPAWN_MIN,
            OBSTACLE_SPAWN_START - (speed_tier - 1) * 0.08,
        ) + random.uniform(-0.08, 0.14)

    while collectible_timer <= 0.0 and game_state == "playing":
        spawn_bonus_collectibles()
        collectible_timer += max(
            COLLECTIBLE_SPAWN_MIN,
            COLLECTIBLE_SPAWN_START - (speed_tier - 1) * 0.05,
        ) + random.uniform(0.0, 0.24)

    check_collectible_collisions()
    check_obstacle_collisions()


def update_game():
    global last_time, game_state, countdown_timer, current_speed
    global total_distance, score, obstacle_timer, collectible_timer
    global player_run_phase, player_dash_meter, player_charge_count, player_health, world_anim_time
    global player_health_restore_delay_timer, player_health_restore_step_timer, player_charge_restore_step_timer
    global player_cheat_dash_refill_timer

    now = time.time()
    dt = now - last_time
    last_time = now

    if dt > MAX_FRAME_DT:
        dt = MAX_FRAME_DT

    if exit_confirm_active:
        return

    if game_state == "menu":
        world_anim_time += dt
        update_environment(dt * 18.0)
        update_particles(dt)
        player_run_phase = (player_run_phase + dt * 4.5) % TAU
        return

    if game_state == "countdown":
        world_anim_time += dt
        countdown_timer -= dt
        player_run_phase = (player_run_phase + dt * 5.5) % TAU
        current_speed = lerp(current_speed, INITIAL_SPEED * 0.6, clamp(dt * 4.0, 0.0, 1.0))
        update_environment(dt * 20.0)
        update_particles(dt)
        if countdown_timer <= 0.0:
            game_state = "playing"
            last_time = time.time()
        return

    if game_state in ("paused", "gameover"):
        return

    remaining_dt = dt
    while remaining_dt > 0.0 and game_state == "playing":
        step_dt = simulation_step_dt(remaining_dt)
        if step_dt <= 0.0:
            break
        update_playing_step(step_dt)
        remaining_dt -= step_dt


def draw_gradient_sky():
    begin_2d()

    glBegin(GL_QUADS)
    glColor3f(*COL_SKY_TOP)
    glVertex2f(-1.0, 1.0)
    glVertex2f(1.0, 1.0)
    glColor3f(*COL_SKY_MID)
    glVertex2f(1.0, 0.18)
    glVertex2f(-1.0, 0.18)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(*COL_SKY_MID)
    glVertex2f(-1.0, 0.18)
    glVertex2f(1.0, 0.18)
    glColor3f(*COL_SKY_BOTTOM)
    glVertex2f(1.0, -1.0)
    glVertex2f(-1.0, -1.0)
    glEnd()

    end_2d()


def draw_track():
    stripe_offset = total_distance % 22.0

    glBegin(GL_QUADS)
    glColor3f(*COL_SHOULDER_A)
    glVertex3f(-90.0, -0.1, TRACK_FRONT_Z)
    glVertex3f(-TRACK_HALF_WIDTH, -0.1, TRACK_FRONT_Z)
    glVertex3f(-TRACK_HALF_WIDTH, -0.1, TRACK_BACK_Z)
    glVertex3f(-90.0, -0.1, TRACK_BACK_Z)

    glColor3f(*COL_SHOULDER_B)
    glVertex3f(TRACK_HALF_WIDTH, -0.1, TRACK_FRONT_Z)
    glVertex3f(90.0, -0.1, TRACK_FRONT_Z)
    glVertex3f(90.0, -0.1, TRACK_BACK_Z)
    glVertex3f(TRACK_HALF_WIDTH, -0.1, TRACK_BACK_Z)

    glColor3f(*COL_TRACK_EDGE)
    glVertex3f(-TRACK_HALF_WIDTH, 0.0, TRACK_FRONT_Z)
    glVertex3f(TRACK_HALF_WIDTH, 0.0, TRACK_FRONT_Z)
    glVertex3f(TRACK_HALF_WIDTH, 0.0, TRACK_BACK_Z)
    glVertex3f(-TRACK_HALF_WIDTH, 0.0, TRACK_BACK_Z)
    glEnd()

    for lane in range(3):
        lane_center = lane_to_x(lane)
        lane_color = color_lerp(COL_TRACK, COL_LANE_GLOW, 0.22 if lane == 1 else 0.12)
        glBegin(GL_QUADS)
        glColor3f(*lane_color)
        glVertex3f(lane_center - 4.6, 0.02, TRACK_FRONT_Z)
        glVertex3f(lane_center + 4.6, 0.02, TRACK_FRONT_Z)
        glVertex3f(lane_center + 4.6, 0.02, TRACK_BACK_Z)
        glVertex3f(lane_center - 4.6, 0.02, TRACK_BACK_Z)
        glEnd()

    checker_size = 24.0
    checker_index = 0
    z_cursor = TRACK_FRONT_Z
    while z_cursor > TRACK_BACK_Z:
        left_color = COL_SHOULDER_A if checker_index % 2 == 0 else COL_SHOULDER_B
        right_color = COL_SHOULDER_B if checker_index % 2 == 0 else COL_SHOULDER_A

        glBegin(GL_QUADS)
        glColor3f(*left_color)
        glVertex3f(-78.0, -0.05, z_cursor)
        glVertex3f(-TRACK_HALF_WIDTH, -0.05, z_cursor)
        glVertex3f(-TRACK_HALF_WIDTH, -0.05, z_cursor - checker_size)
        glVertex3f(-78.0, -0.05, z_cursor - checker_size)

        glColor3f(*right_color)
        glVertex3f(TRACK_HALF_WIDTH, -0.05, z_cursor)
        glVertex3f(78.0, -0.05, z_cursor)
        glVertex3f(78.0, -0.05, z_cursor - checker_size)
        glVertex3f(TRACK_HALF_WIDTH, -0.05, z_cursor - checker_size)
        glEnd()

        checker_index += 1
        z_cursor -= checker_size

    glLineWidth(2.2)
    glBegin(GL_LINES)
    glColor3f(*COL_LANE_GLOW)
    glVertex3f(-5.0, 0.08, TRACK_FRONT_Z)
    glVertex3f(-5.0, 0.08, TRACK_BACK_Z)
    glVertex3f(5.0, 0.08, TRACK_FRONT_Z)
    glVertex3f(5.0, 0.08, TRACK_BACK_Z)
    glEnd()
    glLineWidth(1.0)

    for lane in range(3):
        lane_center = lane_to_x(lane)
        z_val = TRACK_FRONT_Z - 22.0 + stripe_offset
        while z_val > TRACK_BACK_Z:
            glBegin(GL_QUADS)
            glColor3f(*color_scale(COL_WHITE, 0.8))
            glVertex3f(lane_center - 1.3, 0.05, z_val)
            glVertex3f(lane_center + 1.3, 0.05, z_val)
            glVertex3f(lane_center + 1.0, 0.05, z_val - 9.0)
            glVertex3f(lane_center - 1.0, 0.05, z_val - 9.0)
            glEnd()
            z_val -= 22.0


def draw_checker_hill(hill):
    glPushMatrix()
    glTranslatef(hill["x"], hill["height"] * 0.42 - 1.0, hill["z"])
    glScalef(hill["radius"], hill["height"], hill["radius"] * 0.95)
    draw_sphere(1.0, hill["color"], 18, 12)
    glPopMatrix()

    glColor3f(*color_scale(hill["color"], 0.55))
    glLineWidth(1.0)
    glBegin(GL_LINES)
    for index in range(-4, 5):
        x_pos = hill["x"] + index * hill["radius"] * 0.18
        glVertex3f(x_pos, 0.5, hill["z"] - hill["radius"] * 0.45)
        glVertex3f(x_pos, hill["height"] * 0.85, hill["z"] + hill["radius"] * 0.30)
    for index in range(5):
        y_pos = 1.0 + index * hill["height"] * 0.18
        glVertex3f(hill["x"] - hill["radius"] * 0.58, y_pos, hill["z"] - hill["radius"] * 0.10)
        glVertex3f(hill["x"] + hill["radius"] * 0.58, y_pos, hill["z"] - hill["radius"] * 0.10)
    glEnd()


def draw_palm_tree(tree):
    glPushMatrix()
    glTranslatef(tree["x"], 0.0, tree["z"])
    glRotatef(tree["tilt"], 0.0, 0.0, 1.0)

    glPushMatrix()
    draw_cylinder(0.40, tree["height"], 8, COL_PALM_TRUNK)
    glPopMatrix()

    glTranslatef(0.0, tree["height"], 0.0)
    sway_angle = math.sin(world_time() * 2.2 + tree["sway"]) * 10.0
    for index in range(6):
        glPushMatrix()
        glRotatef(index * 60.0 + sway_angle, 0.0, 1.0, 0.0)
        glRotatef(-68.0, 0.0, 0.0, 1.0)
        draw_cone(0.26, tree["leaf_len"], 10, COL_PALM_LEAF)
        glPopMatrix()

    glPopMatrix()


def draw_speed_arch(arch):
    glPushMatrix()
    glTranslatef(0.0, 0.0, arch["z"])
    glScalef(arch["scale"], arch["scale"], arch["scale"])

    draw_box(-17.5, 6.0, 0.0, 1.8, 12.0, 1.8, arch["color"])
    draw_box(17.5, 6.0, 0.0, 1.8, 12.0, 1.8, arch["color"])

    for index in range(12):
        ratio = index / 11.0
        angle = math.pi * ratio
        x_pos = math.cos(angle) * 17.5
        y_pos = 12.0 + math.sin(angle) * 7.8
        block_color = color_lerp(arch["color"], COL_WHITE, 0.20 + ratio * 0.22)
        draw_box(x_pos, y_pos, 0.0, 2.2, 2.0, 2.0, block_color)

    glPopMatrix()


def draw_environment():
    draw_gradient_sky()
    draw_track()

    for hill in hills:
        draw_checker_hill(hill)

    for arch in arches:
        draw_speed_arch(arch)

    for palm in palms:
        draw_palm_tree(palm)


def runner_body_color():
    if player_god_mode:
        return COL_PLAYER_GOD

    if player_cheat_mode:
        return COL_PLAYER_CHEAT

    body_blue = COL_PLAYER_BLUE

    if player_invincible_timer > 0.0:
        blink = 0.5 + 0.5 * math.sin(world_time() * 30.0)
        body_blue = color_lerp(body_blue, COL_WHITE, 0.24 * blink)

    return body_blue


def draw_runner_glove():
    draw_sphere(0.30, COL_PLAYER_GLOVE, 10, 8)
    glPushMatrix()
    glTranslatef(0.0, 0.0, -0.18)
    draw_box(0.0, 0.0, 0.0, 0.30, 0.20, 0.18, COL_PLAYER_LIGHT)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.0, -0.22, -0.04)
    draw_box(0.0, 0.0, 0.0, 0.36, 0.14, 0.20, COL_PLAYER_GLOVE)
    glPopMatrix()


def draw_runner_quills(body_blue):
    for offset, tilt, length in (
        (-0.62, -34.0, 1.82),
        (-0.26, -16.0, 1.70),
        (0.0, 2.0, 1.88),
        (0.26, 16.0, 1.70),
        (0.62, 34.0, 1.82),
    ):
        glPushMatrix()
        glTranslatef(offset, 4.28, -0.92)
        glRotatef(tilt, 1.0, 0.0, 0.0)
        glRotatef(180.0, 1.0, 0.0, 0.0)
        draw_cone(0.30, length, 10, body_blue)
        glPopMatrix()


def draw_roll_band(outer_radius, inner_radius, color, rotate_x=0.0, rotate_y=0.0, rotate_z=0.0):
    glPushMatrix()
    glRotatef(rotate_x, 1.0, 0.0, 0.0)
    glRotatef(rotate_y, 0.0, 1.0, 0.0)
    glRotatef(rotate_z, 0.0, 0.0, 1.0)
    draw_ring_shape(outer_radius, inner_radius, color)
    glPopMatrix()


def player_roll_radius(mode):
    return 1.46


def draw_shield_loop(radius_a, radius_b, color, alpha, rotate_x=0.0, rotate_y=0.0, rotate_z=0.0, phase=0.0):
    segments = 52
    glPushMatrix()
    glRotatef(rotate_x, 1.0, 0.0, 0.0)
    glRotatef(rotate_y, 0.0, 1.0, 0.0)
    glRotatef(rotate_z, 0.0, 0.0, 1.0)
    glBegin(GL_LINE_LOOP)
    for index in range(segments):
        angle = TAU * index / segments
        shimmer = 0.78 + 0.22 * (0.5 + 0.5 * math.sin(world_time() * 4.2 + angle * 2.0 + phase))
        loop_color = color_lerp(COL_SHIELD_ORB, color, 0.45 + 0.45 * shimmer)
        glColor4f(loop_color[0], loop_color[1], loop_color[2], alpha * (0.82 + 0.18 * shimmer))
        glVertex3f(math.cos(angle) * radius_a, math.sin(angle) * radius_b, 0.0)
    glEnd()
    glPopMatrix()


def draw_collectible_shield_orb(collectible, current_y):
    pulse = 1.0 + 0.05 * math.sin(world_time() * 6.5 + collectible["phase"])
    spin = collectible["rot"]

    glPushMatrix()
    glTranslatef(collectible["x"], current_y, collectible["z"])
    glScalef(pulse, pulse, pulse)

    draw_sphere(0.80, color_lerp(COL_SHIELD_ORB, COL_WHITE, 0.14), 18, 14)
    glPushMatrix()
    glTranslatef(-0.16, 0.16, 0.36)
    draw_sphere(0.22, color_lerp(COL_SHIELD_ORB, COL_WHITE, 0.42), 10, 8)
    glPopMatrix()

    glPushMatrix()
    glRotatef(spin * 1.15, 0.0, 1.0, 0.0)
    glRotatef(72.0, 1.0, 0.0, 0.0)
    glRotatef(18.0, 0.0, 0.0, 1.0)
    glScalef(1.16, 0.30, 1.0)
    draw_ring_shape(1.34, 1.08, COL_WHITE)
    glPopMatrix()

    glPushMatrix()
    glRotatef(spin * 1.15 + 18.0, 0.0, 1.0, 0.0)
    glRotatef(72.0, 1.0, 0.0, 0.0)
    glRotatef(18.0, 0.0, 0.0, 1.0)
    glScalef(1.04, 0.30, 1.0)
    draw_ring_shape(1.34, 1.18, color_scale(COL_SHIELD_ORB, 0.78))
    glPopMatrix()

    glLineWidth(1.4)
    draw_shield_loop(0.98, 0.98, COL_SHIELD_NET, 0.30, rotate_y=spin * 1.3, phase=collectible["phase"])
    glLineWidth(1.0)
    glPopMatrix()


def draw_shield_aura():
    rolling_form = player_is_dashing or player_is_charging or player_is_sliding or player_is_jumping
    radius = 2.82 if not rolling_form else 2.05
    center_y = 2.72 if not rolling_form else player_roll_radius("jump") + 0.16
    pulse = 0.96 + 0.05 * math.sin(world_time() * 4.2)
    glow = 0.18 + 0.16 * (0.5 + 0.5 * math.sin(world_time() * 6.2))
    shield_color = color_lerp(COL_SHIELD_ORB, COL_WHITE, glow)
    inner_color = color_scale(shield_color, 0.82)
    spin = (player_run_phase * (210.0 if rolling_form else 120.0) * 57.2958 + world_time() * 48.0) % 360.0
    outer_radius = radius * pulse
    band_outer = outer_radius * 1.010
    band_inner = outer_radius * 0.978
    ring_sets = [
        (90.0, 0.0, spin),
        (0.0, 90.0, spin * 0.85),
        (0.0, 0.0, spin * 1.12),
        (55.0, 0.0, spin * 0.70),
        (-55.0, 0.0, -spin * 0.70),
        (0.0, 55.0, spin * 0.52),
        (0.0, -55.0, -spin * 0.52),
    ]

    glPushMatrix()
    glTranslatef(0.0, center_y, 0.0)

    for rotate_x, rotate_y, rotate_z in ring_sets:
        draw_roll_band(band_outer, band_inner, shield_color, rotate_x=rotate_x, rotate_y=rotate_y, rotate_z=rotate_z)

    for rotate_x, rotate_y, rotate_z in ((35.0, 35.0, -spin * 0.45), (-35.0, 35.0, spin * 0.45)):
        draw_roll_band(outer_radius * 0.995, outer_radius * 0.968, inner_color, rotate_x=rotate_x, rotate_y=rotate_y, rotate_z=rotate_z)

    glPopMatrix()


def draw_player_upright():
    body_blue = runner_body_color()
    run_wave = math.sin(player_run_phase)
    arm_swing = run_wave * 26.0
    leg_swing = -run_wave * 30.0

    glPushMatrix()
    glTranslatef(0.0, 2.55, -0.04)
    glScalef(1.10, 1.30, 0.90)
    draw_sphere(1.0, body_blue, 18, 14)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 1.50, -0.02)
    glScalef(0.95, 0.62, 0.80)
    draw_sphere(1.0, color_scale(body_blue, 0.92), 14, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 4.36, 0.02)
    draw_sphere(1.02, body_blue, 18, 14)
    glPopMatrix()

    draw_runner_quills(body_blue)

    glPushMatrix()
    glTranslatef(0.0, 3.98, 0.86)
    draw_box(0.0, 0.0, 0.0, 0.98, 0.56, 0.60, COL_PLAYER_SKIN)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 2.84, 0.62)
    draw_box(0.0, 0.0, 0.0, 1.18, 0.26, 0.32, color_scale(COL_WHITE, 0.95))
    glPopMatrix()

    for side, swing in ((-1.0, arm_swing), (1.0, -arm_swing)):
        glPushMatrix()
        glTranslatef(side * 1.22, 3.22, -0.06)
        draw_sphere(0.23, body_blue, 10, 8)
        glRotatef(swing, 1.0, 0.0, 0.0)
        draw_box(0.0, -0.60, -0.02, 0.34, 1.12, 0.34, body_blue)
        glTranslatef(0.0, -1.14, 0.00)
        glRotatef(-swing * 0.36, 1.0, 0.0, 0.0)
        draw_box(0.0, -0.48, 0.00, 0.30, 0.96, 0.30, body_blue)
        glTranslatef(0.0, -1.02, 0.00)
        draw_runner_glove()
        glPopMatrix()

    for side, swing in ((-1.0, leg_swing), (1.0, -leg_swing)):
        glPushMatrix()
        glTranslatef(side * 0.70, 1.82, -0.02)
        draw_sphere(0.26, body_blue, 10, 8)
        glRotatef(swing, 1.0, 0.0, 0.0)
        draw_box(0.0, -0.68, 0.02, 0.60, 1.34, 0.60, color_scale(body_blue, 0.94))
        glTranslatef(0.0, -1.32, -0.02)
        draw_sphere(0.23, color_scale(body_blue, 0.90), 10, 8)
        glRotatef(-swing * 0.42, 1.0, 0.0, 0.0)
        draw_box(0.0, -0.58, -0.04, 0.46, 1.22, 0.50, color_scale(body_blue, 0.88))
        draw_box(0.0, -1.10, -0.08, 0.42, 0.18, 0.44, color_scale(body_blue, 0.82))
        glPopMatrix()


def draw_player_roll(mode):
    body_blue = runner_body_color()
    radius = player_roll_radius(mode)
    center_y = radius + 0.10
    outer_band_color = color_lerp(body_blue, COL_WHITE, 0.14)
    seam_color = color_scale(body_blue, 0.72)
    highlight_color = color_lerp(body_blue, COL_WHITE, 0.28)
    spin_factor = 8 if mode == "dash" else 6 if mode == "charge" else 4
    spin_angle = (player_run_phase * spin_factor * 57.2958) % 360

    glPushMatrix()
    glTranslatef(0.0, center_y, 0.0)
    glRotatef(spin_angle, 1.0, 0.0, 0.0)
    draw_sphere(radius, body_blue, 20, 16)

    glPushMatrix()
    glTranslatef(0.0, -radius * 0.18, 0.18)
    glScalef(0.94, 0.68, 1.02)
    draw_sphere(1.0, color_scale(body_blue, 0.74), 18, 12)
    glPopMatrix()

    draw_roll_band(radius * 1.03, radius * 0.88, outer_band_color, rotate_x=90.0)
    draw_roll_band(radius * 1.02, radius * 0.93, seam_color, rotate_y=90.0)
    draw_roll_band(radius * 1.02, radius * 0.96, highlight_color, rotate_z=32.0)

    for angle in (-28.0, 0.0, 28.0):
        glPushMatrix()
        glRotatef(angle, 0.0, 1.0, 0.0)
        glTranslatef(0.0, radius * 0.14, -radius * 0.72)
        glRotatef(180.0, 1.0, 0.0, 0.0)
        draw_cone(radius * 0.16, radius * 0.86, 8, color_scale(body_blue, 0.70))
        glPopMatrix()

    glPopMatrix()


def draw_dash_aura(mode):
    pulse = 1 + 0.08 * math.sin(player_run_phase * 2.5)
    color = color_lerp(runner_body_color(), COL_WHITE, 0.12)
    aura_radius = player_roll_radius(mode) * 1.16 * pulse
    glPushMatrix()
    glTranslatef(0.0, player_roll_radius(mode) + 0.12, 0.0)
    draw_roll_band(aura_radius, aura_radius * 0.91, color, rotate_x=90.0)
    draw_roll_band(aura_radius * 0.98, aura_radius * 0.86, color_scale(runner_body_color(), 0.82), rotate_y=90.0)
    glPopMatrix()


def draw_player():
    if camera_mode == "first" and game_state in ("playing", "paused", "countdown"):
        return

    if player_invincible_timer > 0.0 and not (player_cheat_mode or player_god_mode) and int(world_time() * 18.0) % 2 == 0:
        return

    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)

    if player_shield_timer > 0:
        draw_shield_aura()

    if player_is_dashing:
        draw_dash_aura("dash")
    elif player_is_charging:
        draw_dash_aura("charge")

    glRotatef(180.0, 0.0, 1.0, 0.0)

    if player_is_dashing:
        draw_player_roll("dash")
    elif player_is_charging:
        draw_player_roll("charge")
    elif player_is_sliding:
        draw_player_roll("slide")
    elif player_is_jumping:
        draw_player_roll("jump")
    else:
        draw_player_upright()

    glPopMatrix()


def draw_barrier(obstacle):
    draw_box(obstacle["x"], obstacle["y"], obstacle["z"], 6.4, 5.5, 4.4, COL_STEEL_DARK)
    draw_box(obstacle["x"], obstacle["y"], obstacle["z"], 5.5, 4.6, 3.6, COL_BARRIER)
    draw_box(obstacle["x"], obstacle["y"] + 2.26, obstacle["z"], 5.8, 0.52, 3.9, color_scale(COL_STEEL, 0.86))

    for side in (-1.0, 1.0):
        draw_box(obstacle["x"] + side * 2.46, obstacle["y"], obstacle["z"], 0.44, 5.7, 4.0, COL_STEEL)

    draw_box(obstacle["x"], obstacle["y"] + 0.65, obstacle["z"] + 1.88, 3.54, 1.30, 0.26, COL_OBS_GLOW)
    draw_box(obstacle["x"], obstacle["y"] - 1.06, obstacle["z"] + 1.92, 4.02, 2.00, 0.16, color_scale(COL_STEEL_DARK, 0.90))

    for stripe in (-0.96, 0.0, 0.96):
        draw_box(obstacle["x"] + stripe, obstacle["y"] - 1.02, obstacle["z"] + 2.02, 0.30, 1.92, 0.12, COL_WARNING_STRIPE)


def draw_spike(obstacle):
    draw_box(obstacle["x"], 0.30, obstacle["z"], 6.8, 0.60, 5.0, COL_STEEL_DARK)
    draw_box(obstacle["x"], 0.58, obstacle["z"], 6.0, 0.18, 4.2, COL_STEEL)
    draw_box(obstacle["x"], 0.63, obstacle["z"], 4.4, 0.10, 2.2, COL_WARNING_STRIPE)

    for corner_x in (-2.8, 2.8):
        for corner_z in (-1.9, 1.9):
            glPushMatrix()
            glTranslatef(obstacle["x"] + corner_x, 0.72, obstacle["z"] + corner_z)
            draw_sphere(0.16, COL_OBS_GLOW, 8, 6)
            glPopMatrix()

    for row_z in (-1.02, 0.0, 1.02):
        for index in range(-2, 3):
            glPushMatrix()
            glTranslatef(obstacle["x"] + index * 1.05, 0.62, obstacle["z"] + row_z)
            glRotatef(-90.0, 1.0, 0.0, 0.0)
            draw_cone(0.34, 1.50, 8, color_lerp(COL_SPIKE, COL_COOL_CYAN, 0.12))
            glPopMatrix()


def draw_branch(obstacle):
    sway = math.sin(world_time() * 2.3 + obstacle["phase"]) * 5.0
    for side in (-1.0, 1.0):
        draw_box(obstacle["x"] + side * 2.70, 2.05, obstacle["z"], 0.48, 4.2, 0.50, COL_STEEL_DARK)
        draw_box(obstacle["x"] + side * 2.70, 3.86, obstacle["z"], 0.66, 0.36, 0.66, COL_STEEL)

    glPushMatrix()
    glTranslatef(obstacle["x"], obstacle["y"] + 0.02, obstacle["z"])
    glRotatef(sway, 0.0, 0.0, 1.0)
    glRotatef(90.0, 0.0, 0.0, 1.0)
    draw_cylinder(0.36, 5.5, 10, COL_BRANCH)
    glPopMatrix()

    draw_box(obstacle["x"], obstacle["y"] + 0.24, obstacle["z"], 6.0, 0.20, 0.22, COL_OBS_GLOW)
    draw_box(obstacle["x"], obstacle["y"] - 0.58, obstacle["z"] + 0.02, 2.3, 0.46, 0.14, COL_WARNING)


def draw_badnik(obstacle):
    bob_y = obstacle_center_y(obstacle)
    glPushMatrix()
    glTranslatef(obstacle["x"], bob_y, obstacle["z"])
    glRotatef(obstacle["rot"], 0.0, 1.0, 0.0)

    draw_sphere(1.42, COL_BADNIK, 18, 14)
    draw_roll_band(1.48, 1.24, COL_STEEL, rotate_x=90.0)

    glPushMatrix()
    glTranslatef(0.0, 0.18, 1.20)
    draw_box(0.0, 0.0, 0.0, 1.56, 0.54, 0.24, COL_BADNIK_EYE)
    draw_box(-0.34, 0.0, 0.18, 0.18, 0.18, 0.18, COL_BLACK)
    draw_box(0.34, 0.0, 0.18, 0.18, 0.18, 0.18, COL_BLACK)
    glPopMatrix()

    for side in (-1.0, 1.0):
        glPushMatrix()
        glTranslatef(side * 1.24, -0.08, 0.0)
        glRotatef(90.0, 0.0, 0.0, 1.0)
        draw_cylinder(0.15, 0.86, 8, COL_STEEL_DARK)
        glTranslatef(0.0, 0.76, 0.0)
        draw_cone(0.20, 0.46, 8, COL_STEEL)
        glPopMatrix()

    for angle in (-32.0, 0.0, 32.0):
        glPushMatrix()
        glRotatef(angle, 0.0, 1.0, 0.0)
        glTranslatef(0.0, 0.60, -1.12)
        glRotatef(180.0, 1.0, 0.0, 0.0)
        draw_cone(0.18, 0.62, 8, color_scale(COL_BADNIK, 0.75))
        glPopMatrix()

    glPopMatrix()


def draw_obstacles():
    for obstacle in obstacles:
        if obstacle["type"] == "barrier":
            draw_barrier(obstacle)
        elif obstacle["type"] == "spike":
            draw_spike(obstacle)
        elif obstacle["type"] == "branch":
            draw_branch(obstacle)
        elif obstacle["type"] == "badnik":
            draw_badnik(obstacle)


def draw_collectibles():
    for collectible in collectibles:
        current_y = current_collectible_y(collectible)
        if collectible["type"] == "ring":
            glPushMatrix()
            glTranslatef(collectible["x"], current_y, collectible["z"])
            glRotatef(collectible["rot"], 0.0, 1.0, 0.0)
            draw_ring_shape(1.15, 0.62, COL_RING)
            glPopMatrix()
        elif collectible["type"] == "dash_orb":
            pulse = 1.0 + 0.08 * math.sin(world_time() * 10.0 + collectible["phase"])
            glPushMatrix()
            glTranslatef(collectible["x"], current_y, collectible["z"])
            glScalef(pulse, pulse, pulse)
            draw_sphere(0.85, COL_DASH_ORB, 16, 12)
            glRotatef(collectible["rot"], 0.0, 1.0, 0.0)
            draw_ring_shape(1.32, 1.10, COL_WHITE)
            glRotatef(90.0, 1.0, 0.0, 0.0)
            draw_ring_shape(1.32, 1.10, COL_DASH_BLUE)
            glPopMatrix()
        elif collectible["type"] == "shield_orb":
            draw_collectible_shield_orb(collectible, current_y)
        elif collectible["type"] in ("charge_orb", "magnet_orb", "invincibility_orb", "health_orb"):
            orb_colors = {
                "charge_orb": COL_CHARGE_ORB,
                "magnet_orb": COL_MAGNET_ORB,
                "invincibility_orb": COL_INVINCIBILITY_ORB,
                "health_orb": COL_HEALTH_ORB,
            }
            core_color = orb_colors[collectible["type"]]
            pulse = 1.0 + 0.08 * math.sin(world_time() * 10.0 + collectible["phase"])
            glPushMatrix()
            glTranslatef(collectible["x"], current_y, collectible["z"])
            glScalef(pulse, pulse, pulse)
            draw_sphere(0.85, core_color, 16, 12)
            glRotatef(collectible["rot"], 0.0, 1.0, 0.0)
            draw_ring_shape(1.32, 1.10, COL_WHITE)
            glRotatef(90.0, 1.0, 0.0, 0.0)
            draw_ring_shape(1.32, 1.10, color_lerp(core_color, COL_WHITE, 0.18))
            glPopMatrix()


def draw_particles():
    for particle in particles:
        alpha = clamp(particle["life"] / 0.8, 0.0, 1.0)
        glColor4f(particle["color"][0], particle["color"][1], particle["color"][2], alpha)
        glPushMatrix()
        glTranslatef(particle["x"], particle["y"], particle["z"])
        glutSolidSphere(particle["size"], 8, 6)
        glPopMatrix()


def draw_hud():
    begin_2d()

    if game_state == "menu":
        menu_panel_shift = 0.10
        panel_top = 0.22 + menu_panel_shift
        panel_bottom = -0.68 + menu_panel_shift
        collectibles_bottom = -0.60 + menu_panel_shift

        draw_overlay_quad(-1.0, -1.0, 1.0, 1.0, COL_WHITE, 0.10)
        draw_ui_panel(-0.42, 0.40, 0.42, 0.74, COL_PLAYER_BLUE, 0.22)
        draw_stroke_text(0.0, 0.60, "SONIC DASH", color_lerp(COL_WHITE, COL_PLAYER_LIGHT, 0.24), scale=0.00056, centered=True, line_width=2.8)
        draw_centered_text(0.49, "3D ENDLESS ADVENTURE", color_lerp(COL_WHITE, COL_PLAYER_BLUE, 0.18), GLUT_BITMAP_TIMES_ROMAN_24)

        draw_ui_panel(-0.90, panel_bottom, -0.08, panel_top, COL_RING, 0.28)
        draw_text(-0.82, 0.14 + menu_panel_shift, "[CONTROLS]", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)

        controls = [
            ("[A] / [D]", "Switch Lanes"),
            ("[W] / [MWU]", "Jump"),
            ("[S] / [MWD]", "Slide"),
            ("[F] / [LMB]", "Charge"),
            ("[SPACE] / [RMB]", "Dash"),
        ]
        y_pos = 0.06 + menu_panel_shift
        for key_text, label_text in controls:
            draw_text(-0.82, y_pos, key_text, COL_PLAYER_LIGHT)
            draw_text(-0.48, y_pos, f":  {label_text}", COL_WHITE)
            y_pos -= 0.06

        draw_text(-0.82, -0.30 + menu_panel_shift, "[OTHERS]", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)
        others = [
            ("[C]", "Cheat Mode"),
            ("[G]", "God Mode"),
            ("[V]", "First / Third Person"),
            ("[R]", "Pause / Resume Game"),
            ("[SPACE]", "Start / Restart Game"),
            ("[ESC]", "Quit Game"),
        ]
        y_pos = -0.36 + menu_panel_shift
        for key_text, label_text in others:
            draw_text(-0.82, y_pos, key_text, COL_PLAYER_LIGHT)
            draw_text(-0.48, y_pos, f":  {label_text}", COL_WHITE)
            y_pos -= 0.06

        draw_ui_panel(0.30, collectibles_bottom, 0.96, panel_top, COL_DASH_BLUE, 0.28)
        draw_text(0.36, 0.14 + menu_panel_shift, "COLLECTIBLES", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)
        collectible_rows = [
            ("Ring +1 Dash Meter", COL_RING),
            ("Cyan Orb +5 Dash Meter", COL_DASH_ORB),
            ("Red Orb Pulls Rings", COL_MAGNET_ORB),
            ("Grey Orb 5s Shield", COL_SHIELD_ORB),
            ("Blue Orb Charge Reset", COL_CHARGE_ORB),
            ("Orange Orb Invincible", COL_INVINCIBILITY_ORB),
            ("Green Orb +2 Health Bar", COL_HEALTH_ORB),
        ]
        y_pos = 0.02 + menu_panel_shift
        for row_text, row_color in collectible_rows:
            draw_text(0.36, y_pos, row_text, row_color)
            y_pos -= 0.075

        pulse = 0.60 + 0.40 * math.sin(time.time() * 4.0)
        draw_ui_panel(-0.30, -0.84, 0.30, -0.70, COL_DASH_BLUE, 0.20 + pulse * 0.06)
        draw_stroke_text(0.0, -0.79, "PRESS SPACE TO START", COL_WHITE, scale=0.00018, centered=True, line_width=2.2)
    elif game_state == "countdown":
        label = "GO!" if countdown_timer < 0.45 else str(max(1, int(math.ceil(countdown_timer))))
        draw_ui_panel(-0.34, -0.26, 0.34, 0.30, COL_DASH_BLUE if label == "GO!" else COL_RING, 0.30)
        draw_stroke_text(0.0, 0.04, label, COL_DASH_BLUE if label == "GO!" else COL_WHITE, scale=0.00076, centered=True, line_width=3.2)
        draw_stroke_text(0.0, -0.14, "BUILDING SPEED...", COL_WHITE, scale=0.00018, centered=True, line_width=2.2)
    else:
        form_label, form_color = current_player_form()
        health_ratio = player_health / float(PLAYER_MAX_HEALTH)
        health_color = color_lerp(COL_WARNING, COL_SHOULDER_A, health_ratio)
        draw_ui_panel(-0.98, 0.78, -0.70, 0.96, COL_PLAYER_BLUE, 0.32)
        draw_text(-0.93, 0.90, f"DIST {int(total_distance)}m", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(-0.93, 0.82, f"SCORE {int(score)}", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)

        draw_ui_panel(-0.34, 0.88, 0.34, 0.955, health_color, 0.30)
        draw_overlay_quad(-0.24, 0.906, 0.24, 0.928, COL_TEXT_DARK, 0.56)
        draw_overlay_quad(-0.24, 0.906, -0.24 + 0.48 * health_ratio, 0.928, health_color, 0.95)
        draw_centered_text(0.936, f"HEALTH {player_health}/{PLAYER_MAX_HEALTH}", COL_WHITE)

        draw_ui_panel(-0.20, 0.70, 0.20, 0.87, COL_RING, 0.30)
        draw_centered_text(0.805, f"RINGS {player_rings}", COL_RING, GLUT_BITMAP_TIMES_ROMAN_24)
        draw_centered_text(0.735, f"CHARGE {player_charge_count}/{PLAYER_MAX_CHARGES}", COL_PLAYER_LIGHT)

        draw_ui_panel(0.70, 0.78, 0.98, 0.96, COL_DASH_BLUE, 0.32)
        draw_text(0.74, 0.90, f"TIER {speed_tier}", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(0.74, 0.82, f"SPEED {int(current_speed)}", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)

        bar_x1 = -0.34
        bar_x2 = 0.34
        bar_y1 = -0.92
        bar_y2 = -0.84
        display_dash_meter = player_dash_meter
        if player_is_dashing:
            display_dash_meter = clamp((player_dash_timer / float(DASH_DURATION)) * 100.0, 0.0, 100.0)
        fill_width = (bar_x2 - bar_x1) * (display_dash_meter / 100.0)
        fill_color = COL_DASH_BLUE if display_dash_meter >= 100.0 else color_lerp(COL_RING, COL_DASH_BLUE, display_dash_meter / 100.0)

        draw_ui_panel(bar_x1 - 0.04, -0.98, bar_x2 + 0.04, -0.80, fill_color, 0.22)
        draw_overlay_quad(bar_x1, bar_y1, bar_x2, bar_y2, COL_TEXT_DARK, 0.48)
        draw_overlay_quad(bar_x1, bar_y1, bar_x1 + fill_width, bar_y2, fill_color, 0.95)
        draw_stroke_text(0.0, -0.965, f"DASH {int(display_dash_meter)}%", COL_WHITE, scale=0.00016, centered=True, line_width=2.0)

        if camera_mode == "first":
            draw_text(-0.95, 0.72, "VIEW FP", COL_PLAYER_LIGHT, GLUT_BITMAP_TIMES_ROMAN_24)
            draw_ui_panel(-0.20, -0.78, 0.20, -0.66, form_color, 0.28)
            draw_stroke_text(0.0, -0.74, form_label, form_color, scale=0.00018, centered=True, line_width=2.2)
            if player_invincible_timer > 0.0 and not player_god_mode:
                draw_stroke_text(0.0, 0.58, f"RECOVERING {player_invincible_timer:.1f}s", COL_WARNING_STRIPE, scale=0.00015, centered=True, line_width=2.0)

        effect_bars = []
        if player_is_charging:
            effect_bars.append(("CHARGE", clamp(player_charge_timer / float(CHARGE_DURATION), 0.0, 1.0), COL_CHARGE_ORB))
        if player_power_invincible_timer > 0.0:
            effect_bars.append(("INVINCIBLE", clamp(player_power_invincible_timer / float(ORB_INVINCIBILITY_DURATION), 0.0, 1.0), COL_INVINCIBILITY_ORB))
        if player_magnet_timer > 0.0:
            effect_bars.append(("MAGNET", clamp(player_magnet_timer / float(MAGNET_DURATION), 0.0, 1.0), COL_MAGNET_ORB))
        if player_shield_timer > 0.0:
            effect_bars.append(("SHIELD", clamp(player_shield_timer / float(SHIELD_DURATION), 0.0, 1.0), COL_SHIELD_ORB))

        mode_label = None
        if player_cheat_mode:
            mode_label = ("CHEAT MODE", COL_PLAYER_CHEAT)
        elif player_god_mode:
            mode_label = ("GOD MODE", COL_PLAYER_GOD)

        effect_bar_y1 = -0.745
        effect_bar_height = 0.014
        effect_group_step = 0.080
        effect_label_gap = 0.026
        for index, (effect_label, ratio, effect_color) in enumerate(effect_bars):
            current_y1 = effect_bar_y1 + index * effect_group_step
            current_y2 = current_y1 + effect_bar_height
            current_label_y = current_y2 + effect_label_gap
            draw_stroke_text(0.0, current_label_y, effect_label, effect_color, scale=0.0002, centered=True, line_width=1.9)
            draw_overlay_quad(bar_x1, current_y1, bar_x2, current_y2, COL_TEXT_DARK, 0.48)
            draw_overlay_quad(bar_x1, current_y1, bar_x1 + (bar_x2 - bar_x1) * ratio, current_y2, effect_color, 0.95)
            draw_overlay_outline(bar_x1, current_y1, bar_x2, current_y2, COL_WHITE, 1.4)

        if mode_label is not None:
            mode_label_y = effect_bar_y1 + len(effect_bars) * effect_group_step + effect_label_gap + 0.02
            draw_stroke_text(0.0, mode_label_y, mode_label[0], mode_label[1], scale=0.0002, centered=True, line_width=1.9)

        if player_dash_meter >= 100.0 and not player_is_dashing:
            draw_stroke_text(0.0, -0.785, "DASH READY - PRESS SPACE", COL_DASH_BLUE, scale=0.00015, centered=True, line_width=2.0)

        if player_hit_flash_timer > 0.0:
            hit_strength = clamp(player_hit_flash_timer / 0.55, 0.0, 1.0)
            hit_color = color_lerp(COL_WARNING, COL_RING, 0.18)
            full_alpha = 0.04 if camera_mode != "first" else 0.09
            edge_alpha = 0.14 if camera_mode != "first" else 0.26
            draw_overlay_quad(-1.0, -1.0, 1.0, 1.0, hit_color, full_alpha * hit_strength)
            draw_overlay_quad(-1.0, 0.72, 1.0, 1.0, hit_color, edge_alpha * hit_strength)
            draw_overlay_quad(-1.0, -1.0, 1.0, -0.72, hit_color, edge_alpha * hit_strength)
            draw_overlay_quad(-1.0, -1.0, -0.78, 1.0, hit_color, edge_alpha * hit_strength)
            draw_overlay_quad(0.78, -1.0, 1.0, 1.0, hit_color, edge_alpha * hit_strength)

        if player_hit_message_timer > 0.0 and player_hit_message:
            banner_alpha = clamp(player_hit_message_timer / 0.95, 0.0, 1.0)
            draw_ui_panel(-0.28, 0.08, 0.28, 0.22, COL_WARNING, 0.18 + 0.16 * banner_alpha)
            draw_stroke_text(0.0, 0.14, player_hit_message, COL_WARNING_STRIPE, scale=0.00017, centered=True, line_width=2.2)

        if game_state == "paused":
            draw_overlay_quad(-1.0, -1.0, 1.0, 1.0, COL_BLACK, 0.44)
            draw_ui_panel(-0.34, -0.26, 0.34, 0.28, COL_DASH_BLUE, 0.34)
            draw_stroke_text(0.0, 0.04, "PAUSED", COL_WHITE, scale=0.00054, centered=True, line_width=3.0)
            draw_stroke_text(0.0, -0.14, "PRESS R TO RESUME", COL_WHITE, scale=0.00018, centered=True, line_width=2.2)
        elif game_state == "gameover":
            draw_overlay_quad(-1.0, -1.0, 1.0, 1.0, COL_BLACK, 0.50)
            draw_ui_panel(-0.40, -0.40, 0.40, 0.34, COL_WARNING, 0.34)
            draw_stroke_text(0.0, 0.12, "GAME OVER", COL_WARNING, scale=0.00056, centered=True, line_width=3.0)
            draw_centered_text(-0.02, f"FINAL DISTANCE {int(total_distance)}m", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)
            draw_centered_text(-0.14, f"FINAL SCORE {int(score)}", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)
            draw_stroke_text(0.0, -0.30, "PRESS SPACE TO RESTART", COL_WHITE, scale=0.00018, centered=True, line_width=2.2)

    if exit_confirm_active:
        draw_overlay_quad(-1.0, -1.0, 1.0, 1.0, COL_BLACK, 0.54)
        draw_ui_panel(-0.42, -0.34, 0.42, 0.28, COL_WARNING, 0.30)
        draw_stroke_text(0.0, 0.10, "EXIT", COL_WHITE, scale=0.00050, centered=True, line_width=3.0)
        draw_centered_text(-0.04, "ARE YOU SURE YOU WANT TO EXIT?", COL_WHITE, GLUT_BITMAP_TIMES_ROMAN_24)
        draw_stroke_text(0.0, -0.18, "[Y] : YES    [N] : NO", COL_WHITE, scale=0.00018, centered=True, line_width=2.2)

    end_2d()


def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(62.0, float(window_width) / float(window_height), 0.1, 1200.0)
    glMatrixMode(GL_MODELVIEW)


def setup_camera():
    if game_state == "menu":
        gluLookAt(0.0, 12.5, 32.0, 0.0, 4.0, -120.0, 0.0, 1.0, 0.0)
        return

    bob = math.sin(player_run_phase * 2.0) * (0.15 if game_state == "playing" else 0.05)

    if camera_mode == "first":
        hit_shake = clamp(player_hit_flash_timer / 0.55, 0.0, 1.0)
        shake_x = math.sin(world_time() * 54.0) * 0.16 * hit_shake
        shake_y = math.sin(world_time() * 38.0 + 0.9) * 0.08 * hit_shake
        eye_y = player_y + (1.55 if (player_is_sliding or player_is_attacking()) and not player_is_jumping else 3.55)
        eye_z = player_z + 0.85
        look_y = eye_y - 0.15 + bob * 0.3
        gluLookAt(player_x + shake_x, eye_y + bob + shake_y, eye_z, player_x + shake_x * 0.65, look_y + shake_y * 0.35, player_z - 120.0, 0.0, 1.0, 0.0)
        return

    cam_x = player_x * 0.55
    cam_y = 11.0 + bob
    cam_z = 26.0

    look_x = player_x * 0.85
    look_y = 3.0 + player_y * 0.25
    look_z = -72.0
    gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0.0, 1.0, 0.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_projection()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    setup_camera()

    draw_environment()
    draw_collectibles()
    draw_obstacles()
    draw_player()
    draw_particles()
    draw_hud()

    glutSwapBuffers()


def handle_keyboard(key, x, y):
    global game_state, player_lane_index, last_time
    global camera_mode, player_cheat_mode, player_god_mode

    lowered = key.lower()

    if exit_confirm_active:
        if lowered == b"y":
            request_quit()
        elif lowered == b"n":
            close_exit_confirmation()
        return

    if lowered == b"\x1b":
        open_exit_confirmation()
        return

    if game_state == "menu":
        if lowered == b" ":
            start_new_run(menu_only=False)
        elif lowered == b"v":
            camera_mode = "first" if camera_mode == "third" else "third"
            log_event("VIEW", f"Camera switched to {camera_mode} person")
        return

    if game_state == "countdown":
        if lowered == b"v":
            camera_mode = "first" if camera_mode == "third" else "third"
            log_event("VIEW", f"Camera switched to {camera_mode} person")
        return

    if game_state == "paused":
        if lowered == b"r":
            game_state = "playing"
            last_time = time.time()
            log_event("GAME", "Resumed")
        elif lowered == b"v":
            camera_mode = "first" if camera_mode == "third" else "third"
            log_event("VIEW", f"Camera switched to {camera_mode} person")
        elif lowered == b"c":
            toggle_cheat_mode()
        elif lowered == b"g":
            toggle_god_mode()
        return

    if game_state == "gameover":
        if lowered == b" ":
            start_new_run(menu_only=False)
        elif lowered == b"v":
            camera_mode = "first" if camera_mode == "third" else "third"
            log_event("VIEW", f"Camera switched to {camera_mode} person")
        return

    if lowered == b"v":
        camera_mode = "first" if camera_mode == "third" else "third"
        log_event("VIEW", f"Camera switched to {camera_mode} person")
        return
    if lowered == b"c":
        toggle_cheat_mode()
        return
    if lowered == b"g":
        toggle_god_mode()
        return
    if lowered == b"r":
        game_state = "paused"
        log_event("GAME", "Paused")
        return

    if player_god_mode:
        return

    if lowered == b"a" and player_lane_index > 0:
        player_lane_index -= 1
    elif lowered == b"d" and player_lane_index < 2:
        player_lane_index += 1
    elif lowered == b"w":
        start_jump()
    elif lowered == b"s":
        start_slide()
    elif lowered == b" ":
        if player_dash_meter >= 100.0 and not player_is_dashing:
            start_dash()
    elif lowered == b"f":
        start_charge()


def handle_mouse(button, state, x, y):
    if exit_confirm_active or game_state != "playing" or state != GLUT_DOWN:
        return

    if player_god_mode:
        return

    if button == GLUT_LEFT_BUTTON:
        start_charge()
    elif button == GLUT_RIGHT_BUTTON:
        if player_dash_meter >= 100.0 and not player_is_dashing:
            start_dash()
    elif button == 3:
        start_jump()
    elif button == 4:
        start_slide()


def reshape(width, height):
    global window_width, window_height

    window_width = max(1, width)
    window_height = max(1, height)
    glViewport(0, 0, window_width, window_height)


def idle():
    if quit_requested:
        perform_quit()
        return

    update_game()
    if window_id:
        glutPostRedisplay()


def main():
    global window_id

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(120, 80)
    window_id = glutCreateWindow(WINDOW_TITLE)

    glClearColor(*COL_SKY_BOTTOM, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glShadeModel(GL_SMOOTH)

    try:
        glutIgnoreKeyRepeat(1)
    except Exception:
        pass

    init_game()

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(handle_keyboard)
    glutMouseFunc(handle_mouse)
    glutReshapeFunc(reshape)

    print("=" * 58)
    print("Sonic Dash - 3D Endless Adventure")
    print("=" * 58)
    print("[CONTROLS]")
    print("[A] / [D]      : Switch Lanes")
    print("[W] / [MWU]    : Jump")
    print("[S] / [MWD]    : Slide")
    print("[F] / [LMB]    : Charge")
    print("[SPACE] / [RMB]: Dash")
    print("")
    print("[OTHERS]")
    print("[C]            : Cheat Mode")
    print("[G]            : God Mode")
    print("[V]            : First / Third Person")
    print("[R]            : Pause / Resume Game")
    print("[SPACE]        : Start / Restart Game")
    print("[ESC]          : Quit Game")
    print("=" * 58)

    glutMainLoop()


if __name__ == "__main__":
    main()
