#!/usr/bin/python3

import os
import subprocess
from pathlib import Path

import rclpy
from rclpy.node import Node


def main(args=None):
    rclpy.init(args=args)

    node = Node("subprocess_node_{}".format(os.getpid()))
    node.declare_parameter("cmd", value="")
    cmd_raw = node.get_parameter("cmd").get_parameter_value().string_value

    node.declare_parameter("raw", value=False)
    if node.get_parameter("raw").get_parameter_value().bool_value:
        cmd = cmd_raw
    else:
        node.declare_parameter("sudo", value=False)
        sudo_prefix = "sudo " if node.get_parameter("sudo").get_parameter_value().bool_value else ""

        src_filepath = Path(__file__).resolve()
        src_scripts_dir = src_filepath.parent.parent.joinpath("scripts")
        cmd_raw_split = cmd_raw.split(" ")
        cmd = " ".join([str(src_scripts_dir.joinpath(cmd_raw_split[0]))] + cmd_raw_split[1:])

        cmd = 'bash -c "{}{}"'.format(sudo_prefix, cmd)

    result = subprocess.run(cmd, shell=True, check=True)
    node.get_logger().info('"{}" finished with result: {}'.format(cmd, result.returncode))

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
