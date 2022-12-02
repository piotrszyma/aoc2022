with open("day1.input.txt", "r") as f:
    kcal_per_elf = set()
    current_elf = 0
    for line in f:
        line = line.strip()

        if line == "":
            kcal_per_elf.add(current_elf)
            current_elf = 0
        else:
            current_elf += int(line)

    if current_elf != 0:
        kcal_per_elf.add(current_elf)

print(sum(sorted(kcal_per_elf, reverse=True)[:3]))
