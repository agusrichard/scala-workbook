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

- A higher-order function (HOF) is often defined as a function that (a) takes other functions as input parameters or (b) returns a function as a result. In Scala, HOFs are possible because functions are first-class values.

### Understanding filter’s Scaladoc

- For instance, you can understand the type of functions filter accepts by looking at its Scaladoc. Here’s the filter definition in the List[A] class:
  ```scala
  def filter(p: A => Boolean): List[A]
  ```
- This states that filter is a method that takes a function parameter named p. By convention, p stands for a predicate, which is just a function that returns a Boolean value. So filter takes a predicate p as an input parameter, and returns a List[A], where A is the type held in the list; if you call filter on a List[Int], A is the type Int.
- `p: A => Boolean` means that whatever function you pass in must take the type A as an input parameter and return a Boolean.
- So if your list is a List[Int], you can replace the generic type A with Int, and read that signature like this:

### Writing methods that take function parameters

- To make the following discussion clear, we’ll refer to the code you’re writing as a method, and the code you’re accepting as an input parameter as a function.

#### A first example

- To create a method that takes a function parameter, all you have to do is:
  - In your method’s parameter list, define the signature of the function you want to accept
  - Use that function inside your method
- To demonstrate this, here’s a method that takes an input parameter named f, where f is a function:
  ```scala
  def sayHello(f: () => Unit): Unit = f()
  ```
- Here’s how this works:
  - f is the name of the function input parameter. It’s just like naming a String parameter s or an Int parameter i.
  - The type signature of f specifies the type of the functions this method will accept.
  - The () portion of f’s signature (on the left side of the => symbol) states that f takes no input parameters.
  - The Unit portion of the signature (on the right side of the => symbol) indicates that f should not return a meaningful result.
  - Looking back at the body of the sayHello method (on the right side of the = symbol), the f() statement there invokes the function that’s passed in.
- The following function takes no input parameters and returns nothing, so it matches f’s type signature:

  ```scala
  def helloJoe(): Unit = println("Hello, Joe")

  def bonjourJulien(): Unit = println("Bonjour, Julien")
  ```

- Because the type signatures match, you can pass helloJoe into sayHello:
  ```scala
  sayHello(helloJoe)   // prints "Hello, Joe"
  ```

### The general syntax for defining function input parameters

- To demonstrate more type signature examples, here’s a function that takes a String parameter and returns an Int:
  ```scala
  f: String => Int
  ```
- Similarly, this function takes two Int parameters and returns an Int:
  ```scala
  f: (Int, Int) => Int
  ```
- Can you imagine what sort of functions match that signature? The answer is that any function that takes two Int input parameters and returns an Int matches that signature, so all of these “functions” (methods, really) are a match:
  ```scala
  def add(a: Int, b: Int): Int = a + b
  def subtract(a: Int, b: Int): Int = a - b
  def multiply(a: Int, b: Int): Int = a * b
  ```

### Taking a function parameter along with other parameters

- For instance, here’s a method named executeNTimes that has two input parameters: a function, and an Int:
  ```scala
  def executeNTimes(f: () => Unit, n: Int): Unit =
    for i <- 1 to n do f()
  ```
- As the code shows, executeNTimes executes the f function n times. Because a simple for loop like this has no return value, executeNTimes returns Unit.
- To test executeNTimes, define a method that matches f’s signature:

  ```scala
  // a method of type `() => Unit`
  def helloWorld(): Unit = println("Hello, world")

  executeNTimes(helloWorld, 3)
  // Hello, world
  // Hello, world
  // Hello, world
  ```

- Complicated example:

  ```scala
  def executeAndPrint(f: (Int, Int) => Int, i: Int, j: Int): Unit =
    println(f(i, j))

  def sum(x: Int, y: Int) = x + y
  def multiply(x: Int, y: Int) = x * y

  executeAndPrint(sum, 3, 11)       // prints 14
  executeAndPrint(multiply, 3, 9)   // prints 27
  ```

### Function type signature consistency

- A great thing about learning about Scala’s function type signatures is that the syntax you use to define function input parameters is the same syntax you use to write function literals.
- For instance, if you were to write a function that calculates the sum of two integers, you’d write it like this:

```scala
val f: (Int, Int) => Int = (a, b) => a + b

// That code consists of the type signature:
val f: (Int, Int) => Int = (a, b) => a + b
       -----------------

// The input parameters:
val f: (Int, Int) => Int = (a, b) => a + b
                           ------

// and the body of the function:
val f: (Int, Int) => Int = (a, b) => a + b
                                     -----

// Scala’s consistency is shown here, where this function type:
val f: (Int, Int) => Int = (a, b) => a + b
       -----------------
```
