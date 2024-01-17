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

### if/else

- Snippet:
  ```scala
  if x < 0 then
    println("negative")
  else if x == 0 then
    println("zero")
  else
    println("positive")
  ```
- Short version:
  ```scala
  val x = if a < b then a else b
  ```

### for loops and expressions

- Snippet:

  ```scala
  val ints = List(1, 2, 3, 4, 5)

  for i <- ints do println(i)
  ```

- Guards:

```scala
for
  i <- ints
  if i > 2
do
  println(i)

for
  i <- 1 to 3
  j <- 'a' to 'c'
  if i == 2
  if j == 'b'
do
  println(s"i = $i, j = $j")   // prints: "i = 2, j = b"
```

### for expressions

- The for keyword has even more power: When you use the yield keyword instead of do, you create for expressions which are used to calculate and yield results.
  ```scala
  scala> val doubles = for i <- ints yield i * 2
  val doubles: List[Int] = List(2, 4, 6, 8, 10)
  ```
- Scala’s control structure syntax is flexible, and that for expression can be written in several other ways, depending on your preference:

  ```scala
  val doubles = for i <- ints yield i * 2     // style shown above
  val doubles = for (i <- ints) yield i * 2
  val doubles = for (i <- ints) yield (i * 2)
  val doubles = for { i <- ints } yield (i * 2)
  ```

- Snippet:

  ```scala
  val names = List("chris", "ed", "maurice")
  val capNames = for name <- names yield name.capitalize

  val fruits = List("apple", "banana", "lime", "orange")

  val fruitLengths = for
    f <- fruits
    if f.length > 4
  yield
    // you can use multiple lines
    // of code here
    f.length

  // fruitLengths: List[Int] = List(5, 6, 6)
  ```

### match expressions

- Scala has a match expression, which in its most basic use is like a Java switch statement:

  ```scala
  val i = 1

  // later in the code ...
  i match
    case 1 => println("one")
    case 2 => println("two")
    case _ => println("other")
  ```

- However, match really is an expression, meaning that it returns a result based on the pattern match, which you can bind to a variable:
  ```scala
  val result = i match
    case 1 => "one"
    case 2 => "two"
    case _ => "other"
  ```
- match isn’t limited to working with just integer values, it can be used with any data type:

  ```scala
  val p = Person("Fred")

  // later in the code
  p match
    case Person(name) if name == "Fred" =>
      println(s"$name says, Yubba dubba doo")

    case Person(name) if name == "Bam Bam" =>
      println(s"$name says, Bam bam!")

    case _ => println("Watch the Flintstones!")
  ```

- More types:

  ```scala
  // getClassAsString is a method that takes a single argument of any type.
  def getClassAsString(x: Matchable): String = x match
    case s: String => s"'$s' is a String"
    case i: Int => "Int"
    case d: Double => "Double"
    case l: List[?] => "List"
    case _ => "Unknown"

  // examples
  getClassAsString(1)               // Int
  getClassAsString("hello")         // 'hello' is a String
  getClassAsString(List(1, 2, 3))   // List
  ```

### try/catch/finally

- Scala’s try/catch/finally control structure lets you catch exceptions. It’s similar to Java, but its syntax is consistent with match expressions:
  ```scala
  try
    writeTextToFile(text)
  catch
    case ioe: IOException => println("Got an IOException.")
    case nfe: NumberFormatException => println("Got a NumberFormatException.")
  finally
    println("Clean up your resources here.")
  ```

### while loops

- Snippet:

  ```scala
  var x = 1

  while
    x < 3
  do
    println(x)
    x += 1
  ```

### OOP Domain Modeling

- When writing code in an OOP style, your two main tools for data encapsulation are traits and classes.
- Scala traits can be used as simple interfaces, but they can also contain abstract and concrete methods and fields, and they can have parameters, just like classes.
- As an example of how to use traits as interfaces, here are three traits that define well-organized and modular behaviors for animals like dogs and cats:

  ```scala
  trait Speaker:
    def speak(): String  // has no body, so it’s abstract

  trait TailWagger:
    def startTail(): Unit = println("tail is wagging")
    def stopTail(): Unit = println("tail is stopped")

  trait Runner:
    def startRunning(): Unit = println("I’m running")
    def stopRunning(): Unit = println("Stopped running")
  ```

- Given those traits, here’s a Dog class that extends all of those traits while providing a behavior for the abstract speak method:
  ```scala
  class Dog(name: String) extends Speaker, TailWagger, Runner:
    def speak(): String = "Woof!"
  ```
- Similarly, here’s a Cat class that implements those same traits while also overriding two of the concrete methods it inherits:
  ```scala
  class Cat(name: String) extends Speaker, TailWagger, Runner:
    def speak(): String = "Meow"
    override def startRunning(): Unit = println("Yeah ... I don’t run")
    override def stopRunning(): Unit = println("No need to stop")
  ```
- Scala classes are used in OOP-style programming. Here’s an example of a class that models a “person.” In OOP fields are typically mutable, so firstName and lastName are both declared as var parameters:

  ```scala
  class Person(var firstName: String, var lastName: String):
    def printFullName() = println(s"$firstName $lastName")

  val p = Person("John", "Stephens")
  println(p.firstName)   // "John"
  p.lastName = "Legend"
  p.printFullName()      // "John Legend"
  ```

- Notice that the class declaration creates a constructor:

```scala
val p = Person("John", "Stephens")
```

### FP Domain Modeling

- When writing code in an FP style, you’ll use these concepts:
  - Algebraic Data Types to define the data
  - Traits for functionality on the data.
- For instance, a pizza has three main attributes:

  - Crust size
  - Crust type
  - Toppings

  ```scala
  enum CrustSize:
    case Small, Medium, Large

  enum CrustType:
    case Thin, Thick, Regular

  enum Topping:
    case Cheese, Pepperoni, BlackOlives, GreenOlives, Onions
  ```

- Usage:

  ```scala
  import CrustSize.*
  val currentCrustSize = Small

  // enums in a `match` expression
  currentCrustSize match
    case Small => println("Small crust size")
    case Medium => println("Medium crust size")
    case Large => println("Large crust size")

  // enums in an `if` statement
  if currentCrustSize == Small then println("Small crust size")
  ```

- A product type is an algebraic data type (ADT) that only has one shape, for example a singleton object, represented in Scala by a case object; or an immutable structure with accessible fields, represented by a case class.
- This code demonstrates several case class features:

  ```scala
  // define a case class
  case class Person(
    name: String,
    vocation: String
  )

  // create an instance of the case class
  val p = Person("Reginald Kenneth Dwight", "Singer")

  // a good default toString method
  p                // : Person = Person(Reginald Kenneth Dwight,Singer)

  // can access its fields, which are immutable
  p.name           // "Reginald Kenneth Dwight"
  p.name = "Joe"   // error: can’t reassign a val field

  // when you need to make a change, use the `copy` method
  // to “update as you copy”
  val p2 = p.copy(name = "Elton John")
  p2               // : Person = Person(Elton John,Singer)
  ```
