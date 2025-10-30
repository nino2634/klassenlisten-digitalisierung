import get_classes
<<<<<<< Updated upstream
<<<<<<< Updated upstream
import get_headers
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
import sys
import json

#Main method for doing shit
def run(_filter):
    class_list = get_classes.run(_filter)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    for class_i in class_list:
        print(class_i)
    class_json = json.dumps(class_list)
    return class_json
=======
=======
>>>>>>> Stashed changes
    print(json.dumps(class_list))

#Only for testing
run("")


#Called from JavaScript server
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        print("No argument provided")
>>>>>>> Stashed changes
