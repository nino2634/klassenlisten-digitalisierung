import get_classes
import sys
import json

#Main method for doing shit
def run(_filter):
    class_list = get_classes.run(_filter)
    for class_i in class_list:
        print(class_i)
    class_json = json.dumps(class_list)
    return class_json
    print(json.dumps(class_list))

#Only for testing
run("")


#Called from JavaScript server
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print("No argument provided")

