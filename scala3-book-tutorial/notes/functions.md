# Functions

## Anonymous Functions

- An anonymous function—also referred to as a lambda—is a block of code that’s passed as an argument to a higher-order function.
- Wikipedia defines an anonymous function as, “a function definition that is not bound to an identifier.”
- You can create a new list by doubling each element in ints, using the List class map method and your custom anonymous function:
  ```scala
  val doubledInts = ints.map(_ * 2)   // List(2, 4, 6)
  ```

### Longer forms

- Snippet:
  ```scala
  val doubledInts = ints.map((i: Int) => i * 2)
  val doubledInts = ints.map((i) => i * 2)
  val doubledInts = ints.map(i => i * 2)
  ```

### Shortening anonymous functions

- If you’re not familiar with this syntax, it helps to think of the => symbol as a transformer, because the expression transforms the parameter list on the left side of the symbol (an Int variable named i) into a new result using the algorithm on the right side of the => symbol (in this case, an expression that doubles the Int).

#### Shortening that expression

- Snippet:

  ```scala
  // First, here’s that longest and most explicit form again:
  val doubledInts = ints.map((i: Int) => i * 2)

  // Because the Scala compiler can infer from the data in ints that i is an Int, the Int declaration can be removed:
  val doubledInts = ints.map((i) => i * 2)

  // Because there’s only one argument, the parentheses around the parameter i aren’t needed:
  val doubledInts = ints.map(i => i * 2)

  // Because Scala lets you use the _ symbol instead of a variable name when the parameter appears only once in your function, the code can be simplified even more:
  val doubledInts = ints.map(_ * 2)
  ```

#### Going even shorter

- Kinda explicit:
  ```scala
  ints.foreach((i: Int) => println(i))
  ints.foreach(i => println(i))
  ints.foreach(println(_))
  ```
- Finally, if an anonymous function consists of one method call that takes a single argument, you don’t need to explicitly name and specify the argument, so you can finally write only the name of the method (here, println):
  ```scala
  ints.foreach(println)
  ```
