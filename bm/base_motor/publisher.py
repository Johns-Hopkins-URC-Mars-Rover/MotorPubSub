
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

import json
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Base_Publisher(Node):
    def __init__(self, name:str, topic:str, data:dict, lock:threading.Lock):
        super().__init__(name)
        self.publisher_ = self.create_publisher(String, topic, 10)
        self.data = data # dictionary storing data to be sent
        self.lock = lock # ensure concurrent modification doesn't happen
        timer_period = 0.25  # seconds between each send
        self.timer = self.create_timer(timer_period, self.publish_data)

    def publish_data(self):
        msg = String()
        with self.lock:
            # convert data to JSON
            msg.data = json.dumps(self.data)
            # publish message
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)

class PublishThread(threading.Thread):
    def __init__(self, name:str, topic:str, data:dict, lock:threading.Lock):
        rclpy.init(args=None)
        super(PublishThread, self).__init__()

        # data to be published
        self.data = data
        
        # publisher to use for publishing data
        self.publisher = Base_Publisher(name, topic, self.data, lock)

        self.done = False
        self.start() # start thread

    def stop(self):
        self.publisher.destroy_node()
        rclpy.shutdown()
        self.done = True
        self.join()

    def run(self):
        while not self.done:
            if not self.data:
                # dictionary is empty
                continue
            else:
                # publish once
                rclpy.spin_once(self.publisher)

        # Publish stop message when thread exits.
        self.publisher.publish_data("stop")


def main(args=None):
    data = {"speed": 500}
    lock = threading.Lock()
    publisher = PublishThread("base_publisher", "base_motors", data, lock)
    for i in range(100):
        publisher.run()
        data["speed"] +=i
    #when its over
    publisher.stop()

if __name__ == '__main__':
    main()