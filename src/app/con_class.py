import getclasses
import sys
import json

#Main method for doing shit
def run(_filter):
    class_list = getclasses.run(_filter)
    print(json.dumps(class_list))

#Only for testing
run("")


#Called from flask server
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print("No argument provided")