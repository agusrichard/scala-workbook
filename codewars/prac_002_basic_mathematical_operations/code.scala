def basicOp(op: Char, a: Int, b: Int): Int =
  if op == '+' then
    a + b
  else if op == '-' then
    a - b
  else if op == '*' then
    a * b
  else if op == '/' then
    a / b
  else
    throw new RuntimeException("Please provide the correct operation: +, -, *, /")
  
  // it's better to use match case 