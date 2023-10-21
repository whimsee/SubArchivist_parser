with open("test.ass", "r") as file:
    while True:
        next_line = file.readline()

        if not next_line:
            break;
        print(next_line.strip())
