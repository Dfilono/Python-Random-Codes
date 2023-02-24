# Interpreters:
The interpreters in this file will build upon one another. Each one will add an additional feature to the previous. All the `.py` files will be ordered in the order I added feature so progress can be tracked.

## Calculator v1:
To use this interpreter, your `input` must be single digits `0, 1, 2, 3, 4, 5, 6, 7, 8, 9` and only addition `(+)` is supported. `input` must also not contain any spaces

## Calculator v2:
To use this interpreter, your `input` can be multidgit, and can contain spaces. Both addition `(+)` and subtraction `(-)` are supported.

## Calculator v3:
To use this interpreter, your `input` can be multidigit, and can contain spaces. Addition `(+)`, subtraction `(-)`, multiplication `(*)`, and division `(/)` are supported. Parenthesis `()` are also supported, and PEMDAS will be followed during expressions.

## IR_v1: 
The intermediate representaton interpreter is a different way of writing an interpreter that will ultimately allow for more complex inputs. For now, it has the same functionality as \textbf{Calculator v3} with the addition of unary operators. The unary `+` and unary `-` operators operate on one operand only, and take priort over the binary operators. For example:

```
+-3 if both operators are unary is equiblaent to +(-(3)) = -3
```