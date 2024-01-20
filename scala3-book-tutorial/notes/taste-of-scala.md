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

### Scala methods

- Scala classes, case classes, traits, enums, and objects can all contain methods. The syntax of a simple method looks like this::
  ```scala
  def methodName(param1: Type1, param2: Type2): ReturnType =
    // the method body
    // goes here
  ```
- Examples:

  ```scala
  def sum(a: Int, b: Int): Int = a + b
  def concatenate(s1: String, s2: String): String = s1 + s2

  def sum(a: Int, b: Int) = a + b
  def concatenate(s1: String, s2: String) = s1 + s2

  val x = sum(1, 2)
  val y = concatenate("foo", "bar")

  def getStackTraceAsString(t: Throwable): String =
  val sw = new StringWriter
  t.printStackTrace(new PrintWriter(sw))
  sw.toString

  def makeConnection(url: String, timeout: Int = 5000): Unit =
  println(s"url=$url, timeout=$timeout")

  makeConnection("https://localhost")         // url=http://localhost, timeout=5000
  makeConnection("https://localhost", 2500)   // url=http://localhost, timeout=2500

  makeConnection(
    url = "https://localhost",
    timeout = 2500
  )
  ```

- The extension keyword declares that you’re about to define one or more extension methods on the parameter that’s put in parentheses. As shown with this example, the parameter s of type String can then be used in the body of your extension methods.
- This next example shows how to add a makeInt method to the String class. Here, makeInt takes a parameter named radix. The code doesn’t account for possible string-to-integer conversion errors, but skipping that detail, the examples show how it works:

  ```scala
  extension (s: String)
    def makeInt(radix: Int): Int = Integer.parseInt(s, radix)

  "1".makeInt(2)      // Int = 1
  "10".makeInt(2)     // Int = 2
  "100".makeInt(2)    // Int = 4
  ```

### FIRST-CLASS FUNCTIONS

- Scala has most features you’d expect in a functional programming language, including:
  - Lambdas (anonymous functions)
  - Higher-order functions (HOFs)
  - Immutable collections in the standard library
- These two examples are equivalent, and show how to multiply each number in a list by 2 by passing a lambda into the map method:
  ```scala
  val a = List(1, 2, 3).map(i => i * 2)   // List(2,4,6)
  val b = List(1, 2, 3).map(_ * 2)        // List(2,4,6)
  ```
- Those examples are also equivalent to the following code, which uses a double method instead of a lambda:

  ```scala
  def double(i: Int): Int = i * 2

  val a = List(1, 2, 3).map(i => double(i))   // List(2,4,6)
  val b = List(1, 2, 3).map(double)           // List(2,4,6)
  ```

- When you work with immutable collections like List, Vector, and the immutable Map and Set classes, it’s important to know that these functions don’t mutate the collection they’re called on; instead, they return a new collection with the updated data. As a result, it’s also common to chain them together in a “fluent” style to solve problems.
- For instance, this example shows how to filter a collection twice, and then multiply each element in the remaining collection:

  ```scala
  // a sample list
  val nums = (1 to 10).toList   // List(1,2,3,4,5,6,7,8,9,10)

  // methods can be chained together as needed
  val x = nums.filter(_ > 3)
              .filter(_ < 7)
              .map(_ * 10)

  // result: x == List(40, 50, 60)
  ```

### SINGLETON OBJECTS

- In Scala, the object keyword creates a Singleton object. Put another way, an object defines a class that has exactly one instance.
- Objects have several uses:
  - They are used to create collections of utility methods.
  - A companion object is an object that has the same name as the class it shares a file with. In this situation, that class is also called a companion class.
  - They’re used to implement traits to create modules.
- Because an object is a Singleton, its methods can be accessed like static methods in a Java class. For example, this StringUtils object contains a small collection of string-related methods:

  ```scala
  object StringUtils:
    def isNullOrEmpty(s: String): Boolean = s == null || s.trim.isEmpty
    def leftTrim(s: String): String = s.replaceAll("^\\s+", "")
    def rightTrim(s: String): String = s.replaceAll("\\s+$", "")

  val x = StringUtils.isNullOrEmpty("")    // true
  val x = StringUtils.isNullOrEmpty("a")   // false
  ```

- A companion class or object can access the private members of its companion. Use a companion object for methods and values which aren’t specific to instances of the companion class.
- This example demonstrates how the area method in the companion class can access the private calculateArea method in its companion object:

  ```scala
  import scala.math.*

  class Circle(radius: Double):
    import Circle.*
    def area: Double = calculateArea(radius)

  object Circle:
    private def calculateArea(radius: Double): Double =
      Pi * pow(radius, 2.0)

  val circle1 = Circle(5.0)
  circle1.area   // Double = 78.53981633974483
  ```

- Objects can also be used to implement traits to create modules. This technique takes two traits and combines them to create a concrete object:

  ```scala
  trait AddService:
    def add(a: Int, b: Int) = a + b

  trait MultiplyService:
    def multiply(a: Int, b: Int) = a * b

  // implement those traits as a concrete object
  object MathService extends AddService, MultiplyService

  // use the object
  import MathService.*
  println(add(1,1))        // 2
  println(multiply(2,2))   // 4
  ```

### Creating lists

- To give you a taste of how these work, here are some examples that use the List class, which is an immutable, linked-list class. These examples show different ways to create a populated List:

  ```scala
  val a = List(1, 2, 3)           // a: List[Int] = List(1, 2, 3)

  // Range methods
  val b = (1 to 5).toList         // b: List[Int] = List(1, 2, 3, 4, 5)
  val c = (1 to 10 by 2).toList   // c: List[Int] = List(1, 3, 5, 7, 9)
  val e = (1 until 5).toList      // e: List[Int] = List(1, 2, 3, 4)
  val f = List.range(1, 5)        // f: List[Int] = List(1, 2, 3, 4)
  val g = List.range(1, 10, 3)    // g: List[Int] = List(1, 4, 7)
  ```

### List methods

- Once you have a populated list, the following examples show some of the methods you can call on it. Notice that these are all functional methods, meaning that they don’t mutate the collection they’re called on, but instead return a new collection with the updated elements. The result that’s returned by each expression is shown in the comment on each line:

  ```scala
  // a sample list
  val a = List(10, 20, 30, 40, 10)      // List(10, 20, 30, 40, 10)

  a.drop(2)                             // List(30, 40, 10)
  a.dropWhile(_ < 25)                   // List(30, 40, 10)
  a.filter(_ < 25)                      // List(10, 20, 10)
  a.slice(2,4)                          // List(30, 40)
  a.tail                                // List(20, 30, 40, 10)
  a.take(3)                             // List(10, 20, 30)
  a.takeWhile(_ < 30)                   // List(10, 20)

  // flatten
  val a = List(List(1,2), List(3,4))
  a.flatten                             // List(1, 2, 3, 4)

  // map, flatMap
  val nums = List("one", "two")
  nums.map(_.toUpperCase)               // List("ONE", "TWO")
  nums.flatMap(_.toUpperCase)           // List('O', 'N', 'E', 'T', 'W', 'O')
  ```

- These examples show how the “foldLeft” and “reduceLeft” methods are used to sum the values in a sequence of integers:

  ```scala
  val firstTen = (1 to 10).toList            // List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

  firstTen.reduceLeft(_ + _)                 // 55
  firstTen.foldLeft(100)(_ + _)              // 155 (100 is a “seed” value)
  ```

### Tuples

- Example:

```scala
case class Person(name: String)
val t = (11, "eleven", Person("Eleven"))
t(0)   // 11
t(1)   // "eleven"
t(2)   // Person("Eleven")

val (num, str, person) = t

// result:
// val num: Int = 11
// val str: String = eleven
// val person: Person = Person(Eleven)
```

### CONTEXTUAL ABSTRACTIONS

- Under certain circumstances, you can omit some parameters of method calls that are considered repetitive. Those parameters are called Context Parameters because they are inferred by the compiler from the context surrounding the method call.
- For instance, consider a program that sorts a list of addresses by two criteria: the city name and then street name.

  ```scala
  val addresses: List[Address] = ...

  addresses.sortBy(address => (address.city, address.street))
  ```

- The sortBy method takes a function that returns, for every address, the value to compare it with the other addresses. In this case, we pass a function that returns a pair containing the city name and the street name.
- Note that we only indicate what to compare, but not how to perform the comparison. How does the sorting algorithm know how to compare pairs of String?
- Actually, the sortBy method takes a second parameter—a context parameter—that is inferred by the compiler. It does not appear in the above example because it is supplied by the compiler.
- This second parameter implements the how to compare. It is convenient to omit it because we know Strings are generally compared using the lexicographic order. However, it is also possible to pass it explicitly:

  ```scala
  addresses.sortBy(address => (address.city, address.street))(using Ordering.Tuple2(Ordering.String, Ordering.String))
  ```

- in Scala 3 using in an argument list to sortBy signals passing the context parameter explicitly, avoiding ambiguity.
- In this case, the Ordering.Tuple2(Ordering.String, Ordering.String) instance is exactly the one that is otherwise inferred by the compiler. In other words both examples produce the same program.
- Contextual Abstractions are used to avoid repetition of code. They help developers write pieces of code that are extensible and concise at the same time.

### TOPLEVEL DEFINITIONS

- In Scala 3, all kinds of definitions can be written at the “top level” of your source code files. For instance, you can create a file named MyCoolApp.scala and put these contents into it:

  ```scala
  import scala.collection.mutable.ArrayBuffer

  enum Topping:
    case Cheese, Pepperoni, Mushrooms

  import Topping.*
  class Pizza:
    val toppings = ArrayBuffer[Topping]()

  val p = Pizza()

  extension (s: String)
    def capitalizeAllWords = s.split(" ").map(_.capitalize).mkString(" ")

  val hwUpper = "hello, world".capitalizeAllWords

  type Money = BigDecimal

  // more definitions here as desired ...

  @main def myApp =
    p.toppings += Cheese
    println("show me the code".capitalizeAllWords)
  ```

### Replaces package objects

- When you place a definition in a package named foo, you can then access that definition under all other packages under foo, such as within the foo.bar package in this example:

  ```scala
  package foo {
    def double(i: Int) = i * 2
  }

  package foo {
    package bar {
      @main def fooBarMain =
        println(s"${double(1)}")   // this works
    }
  }
  ```

- Curly braces are used in this example to put an emphasis on the package nesting.
- The benefit of this approach is that you can place definitions under a package named com.acme.myapp, and then those definitions can be referenced within com.acme.myapp.model, com.acme.myapp.controller, etc.
