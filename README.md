# subprocess_node
A simple ROS node to invoke bash commands.

Build:
```
chmod a+x scripts/*.sh subprocess_node/*.py
cd ../..
colcon build --symlink-install --packages-select subprocess_node
```

### Enabling a script to be run as root without a password
1. ```sudo chown root:root /path/to/script```
1. ```sudo visudo``` (safer than ```echo >>```)
1. Append the following lines:
   ```
   <username> ALL = (ALL) ALL
   <username> ALL = (root) NOPASSWD: /path/to/script
   ```
   - \<username\>: result of ```echo $USER```
   - /path/to/script: a file in /this/checkout/root/scripts/
1. Save and apply
1. ```sudo /path/to/script ARGS```

## subprocess_node.py
```
ros2 run subprocess_node subprocess_node.py --ros-args -p cmd:="CMD_AND_ARGS"
```
Parameters:
- ```raw``` (default: false): if true, CMD_AND_ARGS is run as-is. Otherwise, the command that is run is
  ```
  bash -c "{sudo }/your/ros2/workspace/src/subprocess_node/scripts/CMD_AND_ARGS"
  ```
- ```sudo``` (default: false): if true, sets {sudo } above

## reset_usb_port.sh
```
ros2 run subprocess_node subprocess_node.py --ros-args -p sudo:=true -p cmd:="reset_usb_port.sh PORT"
```
where PORT is of the format ```{bus}-{port}(.{subport})```

1. ```sudo udevadm info -q path -n /dev/device```
    - ```sudo dmesg | tail``` or ```lsusb -t``` could also be used
1. Look at the last port before device label: e.g. /.../2-3:1.0/video4linux/... → bus 2, port 3, no subport
1. PORT then becomes "2-3"
