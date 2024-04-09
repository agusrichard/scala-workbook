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

## Function Variables

- The reason it’s called anonymous is because it’s not assigned to a variable, and therefore doesn’t have a name.
- However, an anonymous function—also known as a function literal—can be assigned to a variable to create a function variable:
  ```scala
  val double = (i: Int) => i * 2
  ```
- This creates a function variable named double. In this expression, the original function literal is on the right side of the = symbol
- Like the parameter list for a method, this means that the double function takes one parameter, an Int named i.

#### Invoking the function

- Now you can call the double function like this:
  ```scala
  val x = double(2)   // 4
  ```
- You can also pass double into a map call:
  ```scala
  List(1, 2, 3).map(double)   // List(2, 4, 6)
  ```
- You can store them in a List or Map:

  ```scala
  val functionList = List(double, triple)

  val functionMap = Map(
    "2x" -> double,
    "3x" -> triple
  )
  ```

## Eta Expansion

- When you look at the Scaladoc for the map method on Scala collections classes, you see that it’s defined to accept a function:
  ```scala
  def map[B](f: (A) => B): List[B]
            -----------
  ```
- Indeed, the Scaladoc clearly states, “f is the function to apply to each element.” But despite that, somehow you can pass a method into map, and it still works:
  ```scala
  def times10(i: Int) = i * 10   // a method
  List(1, 2, 3).map(times10)     // List(10,20,30)
  ```
- Have you ever wondered how this works—how you can pass a method into map, which expects a function? The technology behind this is known as Eta Expansion. It converts an expression of method type to an equivalent expression of function type, and it does so seamlessly and quietly.

### The differences between methods and functions

- Historically, methods have been a part of the definition of a class, although in Scala 3 you can now have methods outside of classes, such as Toplevel definitions and extension methods.
- Unlike methods, functions are complete objects themselves, making them first-class entities.
- Their syntax is also different. This example shows how to define a method and a function that perform the same task, determining if the given integer is even:
  ```scala
  def isEvenMethod(i: Int) = i % 2 == 0         // a method
  val isEvenFunction = (i: Int) => i % 2 == 0   // a function
  ```
- The function truly is an object, so you can use it just like any other variable, such as putting it in a list:

  ```scala
  val functions = List(isEvenFunction)

  val functions = List(isEvenFunction)   // works
  val methods = List(isEvenMethod)       // works
  ```

- The important part for Scala 3 is that the Eta Expansion technology is improved, so now when you attempt to use a method as a variable, it just works—you don’t have to handle the manual conversion yourself.

## Higher-order Functions
