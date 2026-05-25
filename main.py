import pyray as rl
import math

# import raylib as rl
import raylib.defines

rl.set_config_flags(
    rl.ConfigFlags.FLAG_VSYNC_HINT
    | rl.ConfigFlags.FLAG_WINDOW_RESIZABLE
    | rl.ConfigFlags.FLAG_WINDOW_UNDECORATED
    | rl.ConfigFlags.FLAG_MSAA_4X_HINT
)
rl.init_window(1920, 1080, "3d")
rl.set_target_fps(144)

playerPos = rl.Vector3(0, 20, 0)
playerAngleY = 0.0  # degree, rotation of axis y
playerAngleX = 0.0  # degree, rotation of axis x
playerRadius = 5.0
playerSpeed = 2.0

target = rl.Vector3(playerRadius, playerPos.y, 0.0)
# target = rl.Vector3(playerRadius, playerPos.y, 0.0)

mainCam = rl.Camera3D(playerPos, target, rl.Vector3(0.0, 1.0, 0.0), 30.0, 0)


def UpdatePlayer():
    global target, mainCam, playerAngleY, playerAngleX
    if playerAngleY > 360 or playerAngleY < -360:
        playerAngleY = 0.0
    if playerAngleX > 360 or playerAngleX < -360:
        playerAngleX = 0.0
    Movement()
    mainCam.position = playerPos


def Movement():
    global playerPos, target, mainCam

    vM = rl.Vector3(0.0, 0.0, 0.0)
    vX, vZ = 0.0, 0.0
    vf = rl.Vector3(0.0, 0.0, 0.0)

    if rl.is_key_down(rl.KeyboardKey.KEY_W):
        vM.x += 1
    if rl.is_key_down(rl.KeyboardKey.KEY_S):
        vM.x += -1
    if rl.is_key_down(rl.KeyboardKey.KEY_D):
        vM.z += 1
    if rl.is_key_down(rl.KeyboardKey.KEY_A):
        vM.z += -1

    if rl.is_key_down(rl.KeyboardKey.KEY_SPACE):
        vf = rl.Vector3(0.0, 15.0 * rl.get_frame_time(), 0.0)

    vZrl = math.sin(raylib.defines.DEG2RAD * (playerAngleY + 90)) * rl.get_frame_time()
    vXrl = math.cos(raylib.defines.DEG2RAD * (playerAngleY + 90)) * rl.get_frame_time()
    vZ = math.sin(raylib.defines.DEG2RAD * (playerAngleY)) * rl.get_frame_time()
    vX = math.cos(raylib.defines.DEG2RAD * (playerAngleY)) * rl.get_frame_time()
    # vY = 120.0

    if vM.x != 0:
        vf = rl.vector3_add(vf, rl.Vector3(vX * vM.x, 0, vZ * vM.x))
    if vM.z != 0:
        vf = rl.vector3_add(vf, rl.Vector3(vXrl * vM.z, 0, vZrl * vM.z))
    vf = rl.vector3_multiply(vf, rl.Vector3(playerSpeed, 1.0, playerSpeed))

    """
    print(vX * vM.x, vZ * vM.x, vXrl * vM.z, vZrl * vM.z)
    rl.draw_text("vX  :" + str(vX * vM.x), 40, 140, 30, rl.BLACK)
    rl.draw_text("vZ  :" + str(vZ * vM.x), 40, 180, 30, rl.BLACK)
    rl.draw_text("vXrl:" + str(vXrl * vM.z), 40, 220, 30, rl.BLACK)
    rl.draw_text("vZrl:" + str(vZrl * vM.z), 40, 260, 30, rl.BLACK)
    """
    playerPos = rl.vector3_add(playerPos, vf)
    target = rl.vector3_add(target, vf)
    mainCam.target = target


def UpdateCamera():
    global playerAngleY, playerAngleX, target
    mouseDelta = rl.get_mouse_delta()
    dx = mouseDelta.x
    dy = -mouseDelta.y
    # if dx == 0 and dy == 0:
    #    return
    speedY = 6.0
    speedX = 3.0
    playerAngleY = playerAngleY + (speedY * dx * rl.get_frame_time())
    playerAngleX = playerAngleX + (speedX * dy * rl.get_frame_time())
    radY = playerAngleY * raylib.defines.DEG2RAD
    radX = playerAngleX * raylib.defines.DEG2RAD
    tanY = math.tan(radY)
    tanX = math.tan(radX)
    if tanX == 0:
        mr = 1.0
    else:
        mr = (math.sin(radX)) / tanX

    if tanY == 0:
        x = playerRadius * mr
    else:
        x = (math.sin(radY) * playerRadius) / (tanY) * mr
    y = math.sin(radX) * playerRadius
    z = (math.sin(radY) * playerRadius) * mr

    # print(playerAngleY, playerAngleX, x, y, z)
    target.x = x + playerPos.x
    target.y = y + playerPos.y
    target.z = z + playerPos.z
    mainCam.target = target


def Gravity():
    global playerPos, target, mainCam
    targetPos = 0.0
    if playerPos.y > 1.7:
        targetPos += playerPos.y - (9.8 * rl.get_frame_time())
    if targetPos <= 1.7:
        targetPos = 1.7
    playerPos.y = targetPos


rl.disable_cursor()

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.DARKBLUE)
    rl.draw_fps(40, 40)
    rl.draw_text("aY:" + str(playerAngleY), 40, 70, 30, rl.BLACK)
    rl.draw_text("aX:" + str(playerAngleX), 40, 100, 30, rl.BLACK)
    Gravity()
    UpdatePlayer()
    UpdateCamera()
    rl.begin_mode_3d(mainCam)

    rl.draw_grid(50, 1)
    # rl.draw_cube(rl.Vector3(0, 0, 0), 1, 1, 1, rl.WHITE)
    rl.draw_cube(rl.Vector3(10, 1, 0), 1, 1, 1, rl.SKYBLUE)
    rl.draw_cube(rl.Vector3(0, 1, 10), 1, 1, 1, rl.RED)
    rl.draw_cube(rl.Vector3(-10, 1, 0), 1, 1, 1, rl.GREEN)
    rl.draw_cube(rl.Vector3(0, 1, -10), 1, 1, 1, rl.WHITE)

    rl.draw_sphere(rl.Vector3(target.x, target.y, target.z), 0.05, rl.RED)

    rl.end_mode_3d()

    rl.end_drawing()
