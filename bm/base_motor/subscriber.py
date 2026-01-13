# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import can 
from motor_wrapper_ak.AKMotorControl import AK7010MotorControl
import time
import PublisherSubscriber.subscriber as sub

bus = can.ThreadSafeBus(interface="socketcan", channel="can0", bitrate=1000000)

motors_l_ids = [1, 2, 3]
motors_r_ids = [4, 5, 6]

motors_r = [AK7010MotorControl.Motor(i, bus) for i in motors_r_ids]
motors_l = [AK7010MotorControl.Motor(i, bus) for i in motors_l_ids]

motors_all = motors_l + motors_r

def receive_data(data):
    if data.get("speed") is None or data.get("speed") == 0:
        for i in range(0, 3):
            motors_l[i].stop()
            motors_r[i].stop()
    elif data.get("heading") == 0:
        for i in range(0, 3):
            motors_l[i].set_speed(data.get("speed"))
            motors_r[i].set_speed(-data.get("speed"))
    elif data.get("heading") < 0:
        for i in range(0, 3):
            motors_l[i].set_speed(data.get("speed"))
            motors_r[i].set_speed(data.get("speed"))
    elif data.get("heading") > 0:
        for i in range(0, 3):
            motors_l[i].set_speed(-data.get("speed"))
            motors_r[i].set_speed(-data.get("speed"))


def main(args=None):
    rclpy.init(args=args)

    subscriber = sub.Subscriber('rasp_subscriber', "base_motors", receive_data)
    rclpy.spin(subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()