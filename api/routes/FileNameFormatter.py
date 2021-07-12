
def NameFormatter(filename):
    filename = str(filename)
    separator = "_"

    if filename.isspace():
        temp_array = filename.split(" ")
        filename = separator.join(temp_array)
        NameFormatter(filename)


    elif filename.find("(") != -1:
        temp_array = filename.split("(")
        filename = separator.join(temp_array)
        NameFormatter(filename)


    elif filename.find(")") != -1:
        temp_array = filename.split(")")
        filename = separator.join(temp_array)
        NameFormatter(filename)


        return filename
        