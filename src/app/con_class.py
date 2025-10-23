import getclasses

def run(filter):
    class_list = getclasses.run(filter)
    for class_i in class_list:
        print(class_i)

if __name__ == "__main__":
    run()