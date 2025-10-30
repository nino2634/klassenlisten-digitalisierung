import getclasses
import sys

#Main method for doing shit
def run(_filter):
    class_list = getclasses.run(_filter)
    for class_i in class_list:
        print(class_i)

#Only for testing
result = subprocess.run(
['python3', 'mein_script.py', arg],
capture_output=True,
text=True
"""

#Called from flask server
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print("No argument provided")