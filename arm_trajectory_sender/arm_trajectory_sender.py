import rclpy
from rclpy.node import Node
from rclpy.clock import Clock
from rclpy.duration import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import time
import csv

# time_stamp = Clock().now()

class arm_pose(Node):
    def __init__(self):
        super().__init__('arm_trajectory_sender')
        self.publisher_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory',10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.move_to_pose_callback)
        self.seq_num = 0
        self.old_key = ''
        csv_file = self.declare_parameter('csv_file','N/A').get_parameter_value().string_value
        print("loading csv file:"+csv_file)
        self.trajectory_list = []
        with open(csv_file) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.trajectory_list.append(row)
                
        # for i in range(len(self.trajectory_list)):
            # print("id: "+ str(i))
            # print(self.trajectory_list[i][1])
            # print(self.trajectory_list[i][2])
            # print(self.trajectory_list[i][3])
            # print(self.trajectory_list[i][4])
            # print(self.trajectory_list[i][5])
            # print(self.trajectory_list[i][6])
           

    def move_to_pose_callback(self):
        msg = JointTrajectory()
        t = self.get_clock().now()
        msg.header.stamp = t.to_msg()
        msg.header.frame_id = ''
        msg.joint_names = [
            'joint1',
            'joint2',
            'joint3',
            'joint4',
            'joint5',
            'joint6']

        for i in range(len(self.trajectory_list)):
            # print(i)
            point = JointTrajectoryPoint()
            point.positions = [        
                float(self.trajectory_list[i][1]),        
                float(self.trajectory_list[i][2]),                
                float(self.trajectory_list[i][3]),        
                float(self.trajectory_list[i][4]),        
                float(self.trajectory_list[i][5]),        
                float(self.trajectory_list[i][6])]
            point.velocities = []
            point.accelerations = []
            point.effort = []
            point.time_from_start = Duration(seconds=10).to_msg()
            msg.points.append(point)
        
        self.publisher_.publish(msg)
        time.sleep(10)            

def main(args=None):
    rclpy.init(args=args)
    arm_trajectory_publisher = arm_pose()
    rclpy.spin(arm_trajectory_publisher)

    arm_trajectory_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
