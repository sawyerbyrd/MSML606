import csv
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class HomeWork2:

    # Problem 1: Construct an expression tree (Binary Tree) from a postfix expression
    # input -> list of strings (e.g., [3,4,+,2,*])
    # this is parsed from p1_construct_tree.csv (check it out for clarification)

    # there are no duplicate numeric values in the input
    # support basic operators: +, -, *, /

    # output -> the root node of the expression tree. Here: [*,+,2,3,4,None,None]
    # Tree Node with * as root node, the tree should be as follows
    #         *
    #        / \
    #       +   2
    #      / \
    #     3   4

    def constructBinaryTree(self, input) -> TreeNode:
        self.stack = [] # creating a stack to hold the nodes
        
        # loop through input
        for token in input:
            
            # check if token is a number OR a negative number
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                node = TreeNode(int(token)) # create new TreeNode with the numeric value
                self.stack.append(node) 
            else:   # token is an operator
                
                # take the last 2 nodes read from input as children
                right = self.stack.pop()
                left = self.stack.pop()
                
                # check for invalid cases
                if left is None or right is None:   # not enough children for the operator
                    raise ValueError("Invalid expression: insufficient children for operator '{}'".format(token))
                if token not in ['+', '-', '*', '/']:   # invalid operator
                    raise ValueError("Invalid operator '{}' in expression".format(token))
                if token == '/' and right.val == 0:     # division by zero
                    raise ZeroDivisionError("Division by zero")
                
                # create a new TreeNode with the operator and left and right children
                node = TreeNode(token, left, right)
                # append the new node to the stack
                self.stack.append(node)
                
        # return the root of the expression tree
        return self.stack.pop()



    # Problem 2.1: Use pre-order traversal (root, left, right) to generate prefix notation
    # return an array of elements of a prefix expression
    # expected output for the tree from problem 1 is [*,+,3,4,2]
    # you can see the examples in p2_traversals.csv

    def prefixNotationPrint(self, head: TreeNode) -> list:
        ret = []    # list to hold the prefix notation elements
        
        if head is None:    # handling empty tree case
            return ret
        
        # add root first
        ret.append(str(head.val))
        
        # then add left and right subtrees (recursively)
        ret.extend(self.prefixNotationPrint(head.left))
        ret.extend(self.prefixNotationPrint(head.right))
        
        return ret
        

    # Problem 2.2: Use in-order traversal (left, root, right) for infix notation with appropriate parentheses.
    # return an array of elements of an infix expression
    # expected output for the tree from problem 1 is [(,(,3,+,4,),*,2,)]
    # you can see the examples in p2_traversals.csv

    # don't forget to add parentheses to maintain correct sequence
    # even the outermost expression should be wrapped
    # treat parentheses as individual elements in the returned list (see output)

    def infixNotationPrint(self, head: TreeNode) -> list:
        ret = []    # list to hold the infix notation elements
        
        if head is None:    # handling empty tree case
            return ret
        
        if head.left is None and head.right is None:   # if it's a leaf node, just return the value
            ret.append(str(head.val))
            return ret
        
        # else, add left and right trees with parentheses around them
        ret.append('(')     # add opening parenthesis before left subtree
        ret.extend(self.infixNotationPrint(head.left))
        
        # then add root
        ret.append(str(head.val))
        
        ret.extend(self.infixNotationPrint(head.right))
        ret.append(')')     # add closing parenthesis after right subtree
        
        return ret


    # Problem 2.3: Use post-order traversal (left, right, root) to generate postfix notation.
    # return an array of elements of a postfix expression
    # expected output for the tree from problem 1 is [3,4,+,2,*]
    # you can see the examples in p2_traversals.csv

    def postfixNotationPrint(self, head: TreeNode) -> list:
        ret = []    # list to hold the postfix notation elements
        
        if head is None:    # handling empty tree case
            return ret
        
        # add left and right subtrees first (recursively)
        ret.extend(self.postfixNotationPrint(head.left))
        ret.extend(self.postfixNotationPrint(head.right))
        
        # then add root
        ret.append(str(head.val))
        
        return ret


class Stack:
    # Implement your stack using either an array or a list
    # (i.e., implement the functions based on the Stack ADT we covered in class)
    # You may use Python's list structure as the underlying storage.
    # While you can use .append() to add elements, please ensure the implementation strictly follows the logic we discussed in class
    # (e.g., manually managing the "top" of the stack
    
    # Use your own stack implementation to solve problem 3

    def __init__(self):
        self.stack = [] # list to hold stack elements
        self.top = -1   # index of the top element in the stack (starts at -1 for an empty stack)
        
    # defining push func for adding an item to the stack
    def push(self, item):
        self.stack.append(item) # append to stack
        self.top += 1   # increment index of top element

    # define a pop func for removing and returning the top item from the stack
    def pop(self):
        # check if stack is empty
        if self.top == -1:
            raise IndexError("Stack is empty")
        
        # return the item at the top of the stack
        item = self.stack[self.top]
        self.top -= 1   # decrement index of top element
        self.stack = self.stack[:self.top + 1]  # remove the popped item from the stack
        return item

    # Problem 3: Write code to evaluate a postfix expression using stack and return the integer value
    # Use stack which you implemented above for this problem

    # input -> a postfix expression string. E.g.: "5 1 2 + 4 * + 3 -"
    # see the examples of test entries in p3_eval_postfix.csv
    # output -> integer value after evaluating the string. Here: 14

    # integers are positive and negative
    # support basic operators: +, -, *, /
    # handle division by zero appropriately

    # DO NOT USE EVAL function for evaluating the expression

    def evaluatePostfix(self, exp: str) -> int:
        tokens = exp.split()  # split the input string into tokens based on whitespace
        stack = Stack()   # create an instance of the Stack class
        
        for token in tokens:
            
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                stack.push(int(token))  # push numeric values onto the stack
            else:   # token is an operator
                # pop the top two operands from the stack
                right = stack.pop()
                left = stack.pop()
                
                # check for invalid operator
                if token not in ['+', '-', '*', '/']:
                    raise ValueError("Invalid operator '{}' in expression".format(token))
                # check for insufficient operands for the operator (left or right is None)
                if left is None or right is None:
                    raise ValueError("Invalid expression: insufficient operands for operator '{}'".format(token))
                
                # perform the operation based on the operator
                if token == '+':
                    result = left + right
                elif token == '-':
                    result = left - right
                elif token == '*':
                    result = left * right
                elif token == '/':
                    if right == 0:  # check for division by zero
                        raise ZeroDivisionError("Division by zero is not allowed in postfix expression")
                    result = left // right # using floor division because the output has to be an int
                
                stack.push(result)  # push the result back onto the stack
        
        # there should only be one element left on the stack, which is the final result
        if stack.top != 0:
            raise ValueError("Invalid expression: too many operands left on the stack")
        
        return stack.pop()  # the final result should be the only element left on the stack


# Main Function. Do not edit the code below
if __name__ == "__main__":
    homework2 = HomeWork2()

    print("\nRUNNING TEST CASES FOR PROBLEM 1")
    testcases = []
    try:
        with open('p1_construct_tree.csv', 'r') as f:
            testcases = list(csv.reader(f))
    except FileNotFoundError:
        print("p1_construct_tree.csv not found")

    for i, (postfix_input,) in enumerate(testcases, 1):
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)
        output = homework2.postfixNotationPrint(root)

        assert output == postfix, f"P1 Test {i} failed: tree structure incorrect"
        print(f"P1 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 2")
    testcases = []
    with open('p2_traversals.csv', 'r') as f:
        testcases = list(csv.reader(f))

    for i, row in enumerate(testcases, 1):
        postfix_input, exp_pre, exp_in, exp_post = row
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)
    
        assert homework2.prefixNotationPrint(root) == exp_pre.split(","), f"P2-{i} prefix failed"
        assert homework2.infixNotationPrint(root) == exp_in.split(","), f"P2-{i} infix failed"
        assert homework2.postfixNotationPrint(root) == exp_post.split(","), f"P2-{i} postfix failed"

        print(f"P2 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 3")
    testcases = []
    try:
        with open('p3_eval_postfix.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                testcases.append(row)
    except FileNotFoundError:
        print("p3_eval_postfix.csv not found")

    for idx, row in enumerate(testcases, start=1):
        expr, expected = row

        try:
            s = Stack()
            result = s.evaluatePostfix(expr)
            if expected == "DIVZERO":
                print(f"Test {idx} failed (expected division by zero)")
            else:
                expected = int(expected)
                assert result == expected, f"Test {idx} failed: {result} != {expected}"
                print(f"Test case {idx} passed")

        except ZeroDivisionError:
            assert expected == "DIVZERO", f"Test {idx} unexpected division by zero"
            print(f"Test case {idx} passed (division by zero handled)")