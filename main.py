class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("Peek from empty stack")

    def size(self):
        return len(self.items)


def precedence(operator):
    if operator in ('+', '-'):
        return 1
    if operator in ('*', '/'):
        return 2
    return 0


def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            raise ValueError("Division by zero")
        return int(a / b) # Using integer division to match typical integer results


def evaluate_expression(expression):
    expression = expression.replace(" ", "")
    if not expression:
        return ""
    
    stack_val = Stack()
    stack_op = Stack()
    
    i = 0
    n = len(expression)
    
    while i < n:
        if expression[i] == '(':
            stack_op.push(expression[i])
        elif expression[i].isdigit():
            val = 0
            while i < n and expression[i].isdigit():
                val = (val * 10) + int(expression[i])
                i += 1
            stack_val.push(val)
            continue
        elif expression[i] == ')':
            while not stack_op.is_empty() and stack_op.peek() != '(':
                val2 = stack_val.pop()
                val1 = stack_val.pop()
                op = stack_op.pop()
                stack_val.push(apply_op(val1, val2, op))
            if not stack_op.is_empty() and stack_op.peek() == '(':
                stack_op.pop()
        elif expression[i] in ('+', '-', '*', '/'):
            while (not stack_op.is_empty() and 
                   precedence(stack_op.peek()) >= precedence(expression[i])):
                val2 = stack_val.pop()
                val1 = stack_val.pop()
                op = stack_op.pop()
                stack_val.push(apply_op(val1, val2, op))
            stack_op.push(expression[i])
        i += 1

    while not stack_op.is_empty():
        val2 = stack_val.pop()
        val1 = stack_val.pop()
        op = stack_op.pop()
        stack_val.push(apply_op(val1, val2, op))

    return str(stack_val.pop())


def process_files(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        lines = infile.readlines()
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("-----"):
                outfile.write(line)
            elif stripped == "":
                outfile.write("\n")
            else:
                try:
                    result = evaluate_expression(stripped)
                    outfile.write(result + "\n")
                except Exception as e:
                    outfile.write(f"Error: {e}\n")


if __name__ == "__main__":
    process_files("input.txt", "output.txt")
    print("Expressions evaluated successfully. Results written to output.txt.")