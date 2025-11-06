from .get_classes import run as get_classes
import sys
import json

#This can only be returned as a string, not as a json
#means it has to be turned into a json in the flask server
#using jsonify!! will be returned in list [,] format with "[]" though!

def con_classes(_filter):
    class_list = get_classes(_filter)
    for class_i in class_list:
        print(class_i)
    class_json = json.dumps(class_list)
    print(class_json)
 
#Only for testing
run("")