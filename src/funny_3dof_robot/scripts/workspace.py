#!/usr/bin/python3

# from funny_3dof_robot.dummy_module import dummy_function, dummy_var
# import rclpy
# from rclpy.node import Node


# class DummyNode(Node):
#     def __init__(self):
#         super().__init__('dummy_node')

# def main(args=None):
#     rclpy.init(args=args)
#     node = DummyNode()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

import matplotlib.pyplot as plt
import numpy as np

def main():
    #plot 1:
    # plt.figure(figsize=(10,5))
    # R = 580 off = 200

    # inner
    # R = 30 off 200
    circle1 = plt.Circle((0, 0.2), 0.58, alpha=0.5, color='blue')
    circle2 = plt.Circle((0, 0.2), 0.03, color='white')

    circle3 = plt.Circle((0, 0.2), 0.58, alpha=0.5, color='blue')
    circle4 = plt.Circle((0, 0.2), 0.03, color='white')

    # plt.plot(circle)
    figs, axs =  plt.subplots(nrows=1, ncols=2)

    axs[0].grid()

    axs[0].add_patch(circle1)
    axs[0].add_patch(circle2)

    axs[0].axis('equal')
    axs[0].set_title('X-Z plane', fontsize=10)

    axs[1].grid()
    
    axs[1].add_patch(circle3)
    axs[1].add_patch(circle4)

    axs[1].axis('equal')
    axs[1].set_title('Y-Z plane', fontsize=10)
    

    plt.show()
if __name__=='__main__':
    main()
