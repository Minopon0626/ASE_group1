"""
赤外線のsendするモジュール
"""

import subprocess

command = ["cgir", "send", "light:on", "-g", "21"]
subprocess.call(command)