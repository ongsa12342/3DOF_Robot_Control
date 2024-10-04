#!/usr/bin/python3

from funny_3dof_robot.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node
from funny_3dof_robot_interfaces.srv import Notify, Mode
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
import roboticstoolbox as rtb
from spatialmath import SE3
import numpy as np
class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.mode_service = self.create_service(
                Mode,
                '/mode',
                self.mode
            )

        self.create_subscription(PoseStamped, "/target", self.target_callback, 10)
        self.joint_state = self.create_publisher(
            JointState, '/joint_states', 10
        )
        self.mode = 0
        self.create_timer(1. / 100. , self.timer_callback)
        self.target_pos = np.array([0. , -0.02 , 0.73])
        self.robot_pos = np.array([0. , -0.02 , 0.73])

        self.target_q = np.array([0. , 0. , 0.])
        self.robot_q = np.array([0. , 0. , 0.])


        self.robot = rtb.DHRobot([
            rtb.RevoluteDH(a=0, alpha=0, d=0.2),  #F1
            rtb.RevoluteDH(alpha= -np.pi/2, qlim=[0,0]),
            rtb.RevoluteDH(d=-0.12,offset=-np.pi/2), #F2
            rtb.RevoluteDH(a=0.25, d=0.1, qlim=[0,0]), #F3
            rtb.RevoluteDH(a=0.28, alpha=0)
        ], name="robot")
# header:
#   stamp:
#     sec: 1727995167
#     nanosec: 253565841
#   frame_id: ''
# name:
# - joint_0
# - joint_1
# - joint_2
# position:
# - 0.4586725274241097
# - -1.3407800000000003
# - 1.0355720000000006
# velocity: []
# effort: []

    def mode(self, request: Mode.Request, response: Mode.Response):


        self.get_logger().info(f"Received flag_request: {request.mode_request}")
        response.mode_response = False
        self.mode = request.mode_request
        if self.mode == 0:
            response.mode_response = self.IPK()
        
        return response
    
    def target_callback(self, msg):
        self.target_pos[0] = msg.pose.position.x
        self.target_pos[1] = msg.pose.position.y
        self.target_pos[2] = msg.pose.position.z

        print(self.target_pos)


    def timer_callback(self):
        msg = JointState()
        
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ["joint_0","joint_1","joint_2"]
        msg.position = self.robot_q.tolist()

        self.joint_state.publish(msg)
    
    def IPK(self):
        T = SE3(self.target_pos)

        solution = self.robot.ikine_min(T, qlim=True)

        if solution.success:
            self.target_q[0] = solution.q[0]
            self.target_q[1] = solution.q[2]
            self.target_q[2] = solution.q[4]
            self.robot_q = self.target_q
            return True
        return False


def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
