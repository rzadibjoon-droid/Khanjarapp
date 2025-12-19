"""
Background Service for Khanjar Scanner
"""

from jnius import autoclass
from time import sleep

PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

def run_service():
    while True:
        sleep(60)

if __name__ == '__main__':
    run_service()
