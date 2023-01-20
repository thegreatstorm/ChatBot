
def learn_chat(filepath, data):
    f = open(filepath, "a")
    f.write(str(data))
    f.close()


def read_cortex(filepath):
    data = None
    with open(filepath, 'r') as file:
        data = file.read().replace('\n', ' ')
    return data