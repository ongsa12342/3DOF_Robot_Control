#!/usr/bin/python3

from funny_3dof_robot.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node
from funny_3dof_robot_interfaces.srv import Notify, Mode

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        self.mode_service = self.create_service(
                Mode,
                '/mode',
                self.mode
            )

        self.mode = 0
        
    def mode(self, request: Mode.Request, response: Mode.Response):


        self.get_logger().info(f"Received flag_request: {request.mode_request}")
        
        self.mode = request.mode_request
        
        # Respond to the service
        response.mode_response = True
        return response
def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
