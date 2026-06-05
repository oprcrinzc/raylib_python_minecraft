import re
import pyray as rl
import math
import time

# import raylib as rl
from raylib import Vector3Multiply
import raylib.defines

rl.set_config_flags(
    rl.ConfigFlags.FLAG_VSYNC_HINT
    | rl.ConfigFlags.FLAG_WINDOW_RESIZABLE
    | rl.ConfigFlags.FLAG_WINDOW_UNDECORATED
    | rl.ConfigFlags.FLAG_MSAA_4X_HINT
)
rl.init_window(1920, 1080, "3d")
rl.set_target_fps(144)


class block:
    type = ""
    width = 1.0
    height = 1.0
    long = 1.0

    def __init__(self, t: str) -> None:
        self.type = t


b = block("grass")

chunk = {0: {0: {0: b, 1: b, 3: b}}}

playerPos = rl.Vector3(0, 20, 0)
playerAngleY = 0.0  # degree, rotation of axis y
playerAngleX = 0.0  # degree, rotation of axis x
playerRadius = 5.0
playerSpeed = 2.0
playerMinY = 0.0
playerMass = 5.0
playerVelocity = rl.Vector3(0, 0, 0)
playerAcceleration = rl.Vector3(0, 0, 0)

t_g = 0.01
g = 9.80665

target = rl.Vector3(playerRadius, playerPos.y, 0.0)
# target = rl.Vector3(playerRadius, playerPos.y, 0.0)

mainCam = rl.Camera3D(playerPos, target, rl.Vector3(0.0, 1.0, 0.0), 55.0, 0)

timeNowJump = 0.0
timeLastJump = 0.0


def UpdatePlayer():
    global target, mainCam, playerAngleY, playerAngleX
    if playerAngleY > 360 or playerAngleY < -360:
        playerAngleY = 0.0
    if playerAngleX >= 87:
        playerAngleX = 87
    if playerAngleX <= -87:
        playerAngleX = -87
    Movement()
    PlayerPhysicSystem()
    mainCam.position = playerPos
    mainCam.position.y = mainCam.position.y + 1.7


def Movement():
    global playerPos, target, mainCam, timeNowJump, timeLastJump

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

    if rl.is_key_down(rl.KeyboardKey.KEY_T):
        playerPos.y = 100

    if rl.is_key_down(rl.KeyboardKey.KEY_SPACE):
        timeNowJump = time.perf_counter()
        if timeNowJump - timeLastJump > 0.25 and playerPos.y == playerMinY:
            AddAcceleration(rl.Vector3(0.0, 22.5, 0.0), 0.25)
            timeLastJump = timeNowJump
        # vf = rl.Vector3(0.0, 15.0 * rl.get_frame_time(), 0.0)

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
    global playerVelocity, playerPos

    # netVel = rl.Vector3(0.0, 0.0, 0.0)
    # v = u + at
    if playerPos.y <= playerMinY:
        playerVelocity.y = 0

    if playerPos.y > playerMinY:
        v = playerVelocity.y - (g * t_g)
        playerVelocity.y = v


def AddAcceleration(a: rl.Vector3, t):
    global playerVelocity
    # v = u + at
    v = rl.vector3_add(playerVelocity, rl.vector3_multiply(a, rl.Vector3(t, t, t)))
    playerVelocity = v


def FindGround(stack: int = 0):
    pX, pY, pZ = (
        math.floor(playerPos.x),
        math.floor(playerPos.y),
        math.floor(playerPos.z),
    )
    global playerMinY
    if stack > 5:
        return
    try:
        block = chunk[pX][pY - stack][pZ]
        playerMinY = pY - stack

    except:
        playerMinY = -1
        FindGround(stack + 1)


def PlayerPhysicSystem():
    global playerPos, playerVelocity, playerMinY

    FindGround()

    # update position
    playerPos.x += playerVelocity.x * rl.get_frame_time()
    playerPos.y += playerVelocity.y * rl.get_frame_time()
    playerPos.z += playerVelocity.z * rl.get_frame_time()

    # if playerPos.y >= 1.7 - 0.000001 and playerPos.y <= 1.7 + 0.000001:
    #    playerPos.y = 1.7
    if playerPos.y < playerMinY and playerPos.y != playerMinY:
        playerPos.y = playerMinY
        playerVelocity.y = 0


chunkLoad = False


def UpdateChunk():
    global chunkLoad
    for x in range(40):
        for y in range(40):
            for z in range(40):
                try:
                    block = chunk[x][y][z]
                    rl.draw_cube(
                        rl.Vector3(x + 0.5, y, z + 0.5),
                        block.width,
                        block.height,
                        block.long,
                        rl.GREEN,
                    )
                except:
                    pass
    chunkLoad = True


rl.disable_cursor()

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.DARKBLUE)
    # rl.rl_clear_screen_buffers()
    rl.draw_fps(40, 40)
    rl.draw_text("X:" + str(math.floor(playerPos.x)), 40, 70, 30, rl.BLACK)
    rl.draw_text("Y:" + str(math.floor(playerPos.y)), 40, 100, 30, rl.BLACK)
    rl.draw_text("Z:" + str(math.floor(playerPos.z)), 40, 130, 30, rl.BLACK)
    rl.draw_text("minY:" + str(playerMinY), 40, 160, 30, rl.BLACK)
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

    UpdateChunk()

    rl.draw_sphere(rl.Vector3(target.x, target.y, target.z), 0.05, rl.RED)

    rl.end_mode_3d()

    rl.end_drawing()
