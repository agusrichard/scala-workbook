# A TASTE OF SCALA

Source: https://docs.scala-lang.org/scala3/book/taste-intro.html

### Your First Scala Program

- Snippet:
  ```scala
  @main def hello() = println("Hello World")
  ```
- In this code, hello is a method. It’s defined with def, and declared to be a “main” method with the @main annotation. It prints the "Hello, World!" string to standard output (STDOUT) using the println method.
- Next, compile the code with scalac:
  ```shell
  $ scalac hello.scala
  ```

### Ask For User Input

- There are several ways to read input from a command-line, but a simple way is to use the readLine method in the scala.io.StdIn object.
- Snippet:

  ```scala
  import scala.io.StdIn.readLine

  @main def helloInteractive() =
      println("Please enter your name: ")
      val name = readLine()

      println("Hello, " + name + "!")

  ```

### THE REPL

- You start a REPL session by running the scala or scala3 command depending on your installation at your operating system command line, where you’ll see a “welcome” prompt like this: `$ scala`
- The REPL is a command-line interpreter, so it sits there waiting for you to type something. Now you can type Scala expressions to see how they work:

  ```scala
  scala> 1 + 1
  val res0: Int = 2

  scala> 2 + 2
  val res1: Int = 4
  ```

- As shown in the output, if you don’t assign a variable to the result of an expression, the REPL creates variables named res0, res1, etc., for you. You can use these variable names in subsequent expressions:
  ```scala
  scala> val x = res0 * 10
  val x: Int = 20
  ```

### Two types of variables

- `val` Creates an immutable variable—like final in Java. You should always create a variable with val, unless there’s a reason you need a mutable variable.
- `var` Creates a mutable variable, and should only be used when a variable’s contents will change over time.
- In an application, a val can’t be reassigned. You’ll cause a compiler error if you try to reassign one:
  ```scala
  val msg = "Hello, world"
  msg = "Aloha"   // "reassignment to val" error; this won’t compile
  ```
- Conversely, a var can be reassigned:
  ```scala
  var msg = "Hello, world"
  msg = "Aloha"   // this compiles because a var can be reassigned
  ```

### Declaring variable types

- How:
  ```scala
  val x: Int = 1   // explicit
  val x = 1        // implicit; the compiler infers the type
  ```
- You can always explicitly declare a variable’s type if you prefer, but in simple assignments like these it isn’t necessary:
  ```scala
  val x: Int = 1
  val s: String = "a string"
  val p: Person = Person("Richard")
  ```

### Built-in data types

- In Scala, everything is an object.
- How to declare variables of the numeric types:
  ```scala
  val b: Byte = 1
  val i: Int = 1
  val l: Long = 1
  val s: Short = 1
  val d: Double = 2.0
  val f: Float = 3.0
  ```
- Because Int and Double are the default numeric types, you typically create them without explicitly declaring the data type:
  ```scala
  val i = 123   // defaults to Int
  val j = 1.0   // defaults to Double
  ```
- In your code you can also append the characters L, D, and F (and their lowercase equivalents) to numbers to specify that they are Long, Double, or Float values:
  ```scala
  val x = 1_000L   // val x: Long = 1000
  val y = 2.2D     // val y: Double = 2.2
  val z = 3.3F     // val z: Float = 3.3
  ```
- When you need really large numbers, use the BigInt and BigDecimal types:
  ```scala
  var a = BigInt(1_234_567_890_987_654_321L)
  var b = BigDecimal(123_456.789)
  ```
- String interpolation provides a very readable way to use variables inside strings. For instance, given these three variables:

  ```scala
  val firstName = "John"
  val mi = 'C'
  val lastName = "Doe"

  println(s"Name: $firstName $mi $lastName")   // "Name: John C Doe"
  ```

- To embed arbitrary expressions inside a string, enclose them in curly braces:

  ```scala
  println(s"2 + 2 = ${2 + 2}")   // prints "2 + 2 = 4"

  val x = -1
  println(s"x.abs = ${x.abs}")   // prints "x.abs = 1"
  ```
