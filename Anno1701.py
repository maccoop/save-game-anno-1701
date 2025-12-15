import subprocess
import os
import sys
import time
from datetime import datetime
import psutil

# ====== CONFIG ======
SAVE_DIR = r"C:\Users\Admin\Documents\Anno 1701 History Edition"
GAME_DIR = r"C:\Users\Admin\Documents\Games\Anno 1701 History Edition"
BRANCH = "main"   # hoặc branch riêng cho máy này
GAME_PROCESS_NAME = "Anno1701.exe"
# ====================


def run(cmd):
    print(f"> {cmd}")
    return subprocess.run(cmd, cwd=SAVE_DIR, shell=True)


def git_pull():
    run("git fetch")
    run(f"git checkout {BRANCH}")
    run("git pull")


def git_push():
    # check có thay đổi không
    status = subprocess.check_output(
        "git status --porcelain", cwd=SAVE_DIR, shell=True
    ).decode().strip()

    if not status:
        print("✔ Không có thay đổi save game")
        return

    run("git add .")

    msg = f"Auto save {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run(f'git commit -m "{msg}"')
    run("git push")


def run_game():
    os.chdir(GAME_DIR)
    subprocess.Popen(f'start "" "{GAME_PROCESS_NAME}"', shell=True)
    print("⏳ Đang chờ game khởi động...")
    time.sleep(30)
    wait_for_game_exit()


def wait_for_game_exit():
    print("⏳ Đang chờ game đóng...")
    while True:
        found = False
        for p in psutil.process_iter(['name']):
            if p.info['name'] == GAME_PROCESS_NAME:
                found = True
                break
        if not found:
            break
        time.sleep(3)
    print("🛑 Game đã đóng")

if __name__ == "__main__":
    os.chdir(SAVE_DIR)

    print("🔄 Pull save game mới nhất")
    git_pull()

    run_game()

    print("⬆ Push save game lên git")
    git_push()

    print("✅ Hoàn tất")
