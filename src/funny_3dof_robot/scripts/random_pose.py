#!/usr/bin/python3

from funny_3dof_robot.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped

import numpy as np

class RandomPoseNode(Node):
    def __init__(self):
        super().__init__('random_pose')
        # Publishers 
        self.posestamp = self.create_publisher(
            PoseStamped, '/target', 10
        )
        self.create_timer(1. / 10. , self.timer_callback)


    def timer_callback(self):
        msg = PoseStamped()
        msg.header.frame_id = "link_0"
        msg.header.stamp = self.get_clock().now().to_msg()
        theta1 = np.random.uniform(0,2*np.pi,1)[0]
        theta2 = np.random.uniform(0,2*np.pi,1)[0]
        r = np.random.uniform(0.3,0.58,1)[0]
        msg.pose.position.x = r*np.sin(theta1)*np.cos(theta2)
        msg.pose.position.y = r*np.sin(theta1)*np.sin(theta2)
        msg.pose.position.z= r*np.cos(theta2)
        print(msg.pose.position.x,msg.pose.position.y,msg.pose.position.z)
        self.posestamp.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RandomPoseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
