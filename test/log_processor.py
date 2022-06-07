import re

if __name__ == '__main__':
    files= {}
    with open("test.log") as f:
        for string in f:
            string = re.search("(?<=processing )(.*?\.java)", string)
            if (string != None):
                if files.keys().__contains__(string.group(0)) :
                    files[string.group(0)] = 2
                else:
                    files[string.group(0)] = 1
        for file in files.keys():
            if(files[file]) == 1:
                print(file)
