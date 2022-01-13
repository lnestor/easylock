import yaml

def read_yaml(filename):
    with open(filename) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print("Error parsing yaml file (%s): %s" % (filename, e))
            exit(-1)

    return data

