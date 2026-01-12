# Base Motor Pub Sub

This combines Clara's old pub sub thread safe code with cyans motor driver (which is a seperate repo you also should download)

# Setup and Use
Clone git repo into your ws/src.
## Dependencies
ROS2
Packages: rclpy and std_msgs (but these should be auto installed)
Install the AK motor driver first (another repo here)
Install python-can
```pip3 install python-can```
AK motor driver is a dependency, make sure to install that as well before running the following:
## Run: 
``` 
colcon build --packages-select base_motor 
source install/setup.bash
```
On base device, run
``` 
ros2 run base_motor talker
```
On server, run
``` ros2 run base_motor listener
```