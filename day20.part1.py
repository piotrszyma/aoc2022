# Day 20
from typing import NamedTuple, Union
from dataclasses import dataclass, field


@dataclass
class Num:
    value: int
    original_idx: int


@dataclass
class Node:
    value: int
    next: Union["Node", None] = field(repr=False)
    prev: Union["Node", None] = field(repr=False)


def to_list(node: Node, size: int) -> list[int]:
    lst: list[int] = []
    curr_node = node
    while len(lst) < size:
        assert curr_node
        lst.append(curr_node.value)
        curr_node = curr_node.next

    return lst


def move_node(head: Node, node_to_move: Node, shift: int, size: int) -> Node:
    if head == node_to_move:
        assert head.next
        new_head = head.next
    else:
        new_head = head

    node_to_move_old_next = node_to_move.next
    assert node_to_move_old_next

    node_to_move_old_prev = node_to_move.prev
    assert node_to_move_old_prev

    if shift > 0:
        shift = shift % (size - 1)
    elif shift < 0:
        # TODO: fixme
        shift = shift % (size - 1)  # modulo so always positive

    assert shift >= 0
    if shift == 0:
        return head  # Nothing changed - return old head.

    node_before = node_to_move
    for _ in range(shift):
        assert node_before
        node_before = node_before.next

    assert node_before

    node_before_old_next = node_before.next
    assert node_before_old_next

    # Clean-up nodes before / after `node_to_move` - old positions.
    node_to_move_old_prev.next = node_to_move.next
    node_to_move_old_next.prev = node_to_move_old_prev

    node_before.next = node_to_move
    node_to_move.prev = node_before
    node_to_move.next = node_before_old_next

    node_before_old_next.prev = node_to_move

    return new_head


def decode(nums: list[int]) -> list[int]:
    # Create a linked list of nums.
    root_node: Node | None = None
    prev_node: Node | None = None
    for num in nums:
        node_to_move = Node(value=num, next=None, prev=prev_node)
        if root_node is None:  # Only in first iteration.
            root_node = node_to_move

        if prev_node is not None:  # All except first iteration.
            prev_node.next = node_to_move

        prev_node = node_to_move

    assert root_node, "Must have at least 1 element."
    assert prev_node, "Must have at least 1 element."

    # Form a cycle - last node points on first etc.
    root_node.prev = prev_node
    prev_node.next = root_node

    # Create list of nodes - initial  order.
    nodes: list[Node] = []
    curr_node = root_node
    while len(nodes) < len(nums):
        assert curr_node
        nodes.append(curr_node)
        curr_node = curr_node.next

    head = root_node

    # Move each node in initial order.
    for node_to_move in nodes:
        shift = node_to_move.value
        head = move_node(head, node_to_move, shift, size=len(nodes))

    new_nums: list[int] = []
    curr_node = head
    while len(new_nums) < len(nums):
        assert curr_node
        new_nums.append(curr_node.value)
        curr_node = curr_node.next

    # print(new_nums)
    return new_nums


def main():
    nums: list[int] = []
    with open("day20.input.txt", "r") as f:
        for l in f:
            nums.append(int(l.strip()))

    print(nums[0], nums[-1])

    # Create a linked list of nums.
    root_node: Node | None = None
    prev_node: Node | None = None
    for num in nums:
        node_to_move = Node(value=num, next=None, prev=prev_node)
        if root_node is None:  # Only in first iteration.
            root_node = node_to_move

        if prev_node is not None:  # All except first iteration.
            prev_node.next = node_to_move

        prev_node = node_to_move

    assert root_node, "Must have at least 1 element."
    assert prev_node, "Must have at least 1 element."

    # Form a cycle - last node points on first etc.
    root_node.prev = prev_node
    prev_node.next = root_node

    # Create list of nodes - initial  order.
    nodes: list[Node] = []
    curr_node = root_node
    while len(nodes) < len(nums):
        assert curr_node
        nodes.append(curr_node)
        curr_node = curr_node.next

    head = root_node

    # Move each node in initial order.
    for node_to_move in nodes:
        shift = node_to_move.value
        head = move_node(head, node_to_move, shift, size=len(nodes))

    new_nums: list[int] = []
    curr_node = head
    while len(new_nums) < len(nums):
        assert curr_node
        new_nums.append(curr_node.value)
        curr_node = curr_node.next

    # print(new_nums)

    zero_idx = new_nums.index(0)
    num_1000th = new_nums[(1000 + zero_idx) % len(new_nums)]
    num_2000th = new_nums[(2000 + zero_idx) % len(new_nums)]
    num_3000th = new_nums[(3000 + zero_idx) % len(new_nums)]
    print(f"{num_1000th=} {num_2000th=} {num_3000th=}")
    res = num_1000th + num_2000th + num_3000th
    print(res)


if __name__ == "__main__":
    # Testing.
    first = Node(value=1, next=None, prev=None)
    second = Node(value=2, next=None, prev=first)
    third = Node(value=-3, next=None, prev=second)
    forth = Node(value=3, next=None, prev=third)
    fifth = Node(value=-2, next=None, prev=forth)
    sixth = Node(value=0, next=None, prev=fifth)
    seventh = Node(value=4, next=None, prev=sixth)

    first.prev = seventh
    first.next = second
    second.next = third
    third.next = forth
    forth.next = fifth
    fifth.next = sixth
    sixth.next = seventh
    seventh.next = first

    head = first

    size = 7

    assert to_list(head, size=size) == [1, 2, -3, 3, -2, 0, 4]

    head = move_node(head, first, first.value, size)
    assert head

    assert to_list(head, size=size) == [2, 1, -3, 3, -2, 0, 4], to_list(head, size=7)

    head = move_node(head, second, second.value, size)

    assert to_list(head, size=size) == [1, -3, 2, 3, -2, 0, 4], to_list(head, size=7)

    assert third.value == -3
    head = move_node(head, third, third.value, size)

    assert to_list(head, size=size) == [1, 2, 3, -2, -3, 0, 4], to_list(head, size=7)

    assert forth.value == 3
    head = move_node(head, forth, forth.value, size)

    assert to_list(head, size=size) == [1, 2, -2, -3, 0, 3, 4], to_list(head, size=7)

    assert fifth.value == -2
    head = move_node(head, fifth, fifth.value, size)

    assert to_list(head, size=size) == [1, 2, -3, 0, 3, 4, -2], to_list(head, size=7)

    assert sixth.value == 0
    head = move_node(head, sixth, sixth.value, size)

    assert to_list(head, size=size) == [1, 2, -3, 0, 3, 4, -2], to_list(head, size=7)

    assert seventh.value == 4
    head = move_node(head, seventh, seventh.value, size)

    assert to_list(head, size=size) == [1, 2, -3, 4, 0, 3, -2], to_list(head, size=7)

    assert decode([1, 2, -3, 3, -2, 0, 4]) == [1, 2, -3, 4, 0, 3, -2]
    main()
