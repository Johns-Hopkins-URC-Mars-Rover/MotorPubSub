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

from std_msgs.msg import Int8


class Base_Publisher(Node):

    def __init__(self):
        super().__init__('base_motor_publisher')
        self.publisher_ = self.create_publisher(Int8, 'base_motors', 10)
        timer_period = 0.25  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Int8()
        msg.data = i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%i"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    base_pub = Base_Publisher()

    rclpy.spin(base_pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    base_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
