import sys
import os

# Get the absolute path to the parent directory of your child directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Construct the path to your child directory
child_dir = os.path.join(parent_dir, "MainUIClass")

# Add the child directory to the Python path
sys.path.append(child_dir)


