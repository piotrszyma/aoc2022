# Day 7
from dataclasses import dataclass
from typing import Iterable, Union
from functools import cached_property


@dataclass
class File:
    size: int
    name: str


@dataclass
class Dir:
    name: str
    content: list[Union[File, "Dir"]]
    parent: "Dir"

    @cached_property
    def size(self) -> int:
        return sum(c.size for c in self.content)


@dataclass
class RootDir(Dir):
    parent: None = None


def get_dir_sizes(root: Dir) -> Iterable[int]:
    yield root.size
    for f in root.content:
        if isinstance(f, Dir):
            yield from get_dir_sizes(f)


def main():
    with open("day7.input.txt", "r") as f:
        root = RootDir(name="/", content=[])
        cwd = root

        ls_mode = False

        for idx, line in enumerate(f):
            line = line.strip()

            if idx == 0:
                assert line == "$ cd /"
                continue

            if line == "$ ls":
                ls_mode = True
                continue

            if line.startswith("$ cd"):
                ls_mode = False
                _, _, new_dir_name = line.split(" ")
                if new_dir_name == "..":
                    assert cwd.parent
                    cwd = cwd.parent
                else:
                    [new_cwd] = [
                        d
                        for d in cwd.content
                        if isinstance(d, Dir) and d.name == new_dir_name
                    ]
                    cwd = new_cwd
            else:  # File listing
                assert ls_mode
                size, name = line.split(" ")
                if size == "dir":
                    cwd.content.append(Dir(name=name, content=[], parent=cwd))
                else:
                    size = int(size)
                    cwd.content.append(File(size=size, name=name))

    print(sum(s for s in get_dir_sizes(root) if s <= 100000))


if __name__ == "__main__":
    main()
