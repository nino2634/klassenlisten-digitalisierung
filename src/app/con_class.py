import get_classes
import get_headers
import sys
import json

#Main method for doing shit
def run(_filter):
    class_list = get_classes.run(_filter)
    for class_i in class_list:
        print(class_i)
    class_json = json.dumps(class_list)
    return class_json