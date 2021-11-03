from typing import List, Optional, Tuple, List
import cv2
import numpy as np
from ROAR_iOS.udp_receiver import UDPStreamer
from ROAR.utilities_module.vehicle_models import VehicleControl
import struct
MAX_DGRAM = 9600


class ControlStreamer(UDPStreamer):
    def __init__(self, **kwargs):
        super(ControlStreamer, self).__init__(**kwargs)
        self.control_tx = VehicleControl()

    def send(self, control:VehicleControl):
        self.control_tx = control
        string_format = f"{control.throttle},{control.steering}"
        self._send_data(string_format)

    def run_in_series(self, **kwargs):
        pass


# import logging
# from ROAR.utilities_module.module import Module
# from ROAR.utilities_module.vehicle_models import VehicleControl
# from typing import Optional, List
# from pathlib import Path
# from websocket import create_connection
# import websocket
# import requests


# class ControlStreamer(Module):
#     def save(self, **kwargs):
#         # no need to save. use Agent's saving mechanism
#         pass
#
#     def __init__(self, ios_addr: str, ios_port: int, name: str = "control",
#                  threaded: bool = True):
#         super().__init__(threaded=threaded, name=name)
#         self.logger = logging.getLogger(f"{self.name} server [{ios_addr}:{ios_port}]")
#         self.host = ios_addr
#         self.port = ios_port
#         self.control_rx: VehicleControl = VehicleControl()
#         self.control_tx: VehicleControl = VehicleControl()
#         self.ws_tx = websocket.WebSocket()
#         self.ws_rx = None
#         self.logger.info(f"{name} initialized")
#
#     def connect(self):
#         try:
#             self.logger.info(f"Connecting to ws://{self.host}:{self.port}/{self.name}_rx")
#             self.ws_tx.connect(f"ws://{self.host}:{self.port}/{self.name}_rx", timeout=1)
#             self.logger.info("connected")
#         except:
#             raise Exception("Unable to connect to Control Streamer")
#
#     def send(self, vehicle_control: VehicleControl):
#         try:
#             self.control_tx = vehicle_control
#             self.ws_tx.send(f"{self.control_tx.throttle},{self.control_tx.steering}")
#         except Exception as e:
#             self.logger.error(e)
#
#     def receive(self):
#         try:
#             self.ws_rx = create_connection(f"ws://{self.host}:{self.port}/{self.name}_tx")
#             result: bytes = self.ws_rx.recv()
#             try:
#                 self.control_rx = VehicleControl.fromBytes(result)
#             except Exception as e:
#                 self.logger.error(f"Failed to parse data {e}. {result}")
#
#         except Exception as e:
#             self.logger.error(f"Failed to get data: {e}")
#
#     def run_in_series(self, **kwargs):
#         self.receive()
#
#     def shutdown(self):
#         super(ControlStreamer, self).shutdown()
