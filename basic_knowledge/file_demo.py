with open("target_write.txt", "a") as f1:
    f1.write("hello\r\n")

with open('target_write.txt', 'r') as f:
    for line in f.readlines():
        print(line.strip())
