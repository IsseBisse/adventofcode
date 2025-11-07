def get_data(path):
    with open(path) as file:
        text = file.read()

    registers, code = text.split("\n\n")
    registers = [int(row.split(": ")[1]) for row in registers.split("\n")]

    code = [int(num) for num in code.split(": ")[1].split(",")]

    return registers, code


class Program:
    def __init__(self, registers, code):
        self.ptr = 0
        self.output = []
        self.num_steps = 0

        self.registers = registers
        self.code = code

    def run(self):
        while self.ptr < len(self.code):
            opcode = self.code[self.ptr]
            op = self.code[self.ptr + 1]

            operation, use_combo_op = self.OPCODES[opcode]
            if use_combo_op:
                if op > 3:
                    op = self.registers[op - 4]

            operation(self, op)

            self.ptr += 2
            self.num_steps += 1

            if self.num_steps > 1000:
                return ""

        return ",".join(str(val) for val in self.output)

    def adv(self, op, register_idx=0):
        num = self.registers[0]
        den = 2**op
        res = int(num / den)
        self.registers[register_idx] = res

    def bxl(self, op):
        val = self.registers[1] ^ op
        self.registers[1] = val

    def bst(self, op):
        val = op % 8
        self.registers[1] = val

    def jnz(self, op):
        if self.registers[0] == 0:
            return

        self.ptr = op - 2

    def bxc(self, _):
        val = self.registers[1] ^ self.registers[2]
        self.registers[1] = val

    def out(self, op):
        val = op % 8
        self.output.append(val)

    def bdv(self, op):
        self.adv(op, register_idx=1)

    def cdv(self, op):
        self.adv(op, register_idx=2)

    OPCODES = {
        0: (adv, True),
        1: (bxl, False),
        2: (bst, True),
        3: (jnz, False),
        4: (bxc, False),
        5: (out, True),
        6: (bdv, True),
        7: (cdv, True),
    }


def part_one():
    registers, code = get_data("17/input.txt")

    program = Program(registers, code)
    output = program.run()

    print(output)


def part_two():
    registers, code = get_data("17/input.txt")

    a = 0
    output_string = ""
    while True:
        registers = [a, 0, 0]
        program = Program(registers, code)
        output = program.run()

        output += ",0" * (3 - (len(output) + 1) // 2)
        print(output)

        first_digit = output.split(",")[0]
        output_string += first_digit

        if len(output_string) > 21 and output_string[:20] == output_string[-20:]:
            break

        # if first_digit not in mapping_dict:
        #     mapping_dict[first_digit] = a

        # if all(num in mapping_dict for num in range(8)):
        #     break

        a += 1

    mapping = [int(char) for char in output_string[:1024]]
    print(mapping)

    # min_a = 0
    # for idx, digit in enumerate(code):

    #     pass

    # for i in range(4):
    #     plt.subplot(2, 2, i+1)
    #     x = range(1, 4096)
    #     y = [int(output.split(",")[i]) if len(output.split(",")) > i else 0 for output in outputs]

    #     print(y[:3*8**(i+1):8**i])

    #     plt.plot(x, y)

    # plt.show()


if __name__ == "__main__":
    # part_one()
    part_two()
