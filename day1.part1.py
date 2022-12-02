with open("day1.input.txt", "r") as f:
    max_elf = 0
    current_elf = 0
    for line in f:
        line = line.strip()

        if line == "":
            max_elf = max(max_elf, current_elf)
            current_elf = 0
        else:
            current_elf += int(line)

    if current_elf != 0:
        max_elf = max(max_elf, current_elf)

print(max_elf)
