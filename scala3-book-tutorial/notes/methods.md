# Methods:

**Source:**

- https://docs.scala-lang.org/scala3/book/methods-intro.html
- https://docs.scala-lang.org/scala3/book/methods-most.html

## METHOD FEATURES

### Defining Methods

- Scala methods have many features, including these:
  - Generic (type) parameters
  - Default parameter values
  - Multiple parameter groups
  - Context-provided parameters
  - By-name parameters
  - and more…
- Some of these features are demonstrated in this section, but when you’re defining a “simple” method that doesn’t use those features, the syntax looks like this:
  ```scala
  def methodName(param1: Type1, param2: Type2): ReturnType =
    // the method body
    // goes here
  end methodName   // this is optional
  ```
- In that syntax:
  - The keyword def is used to define a method
  - The Scala standard is to name methods using the camel case convention
  - Method parameters are always defined with their type
  - Declaring the method return type is optional
  - Methods can consist of many lines, or just one line
  - Providing the end methodName portion after the method body is also optional, and is only recommended for long methods
- Examples:
  ```scala
  def add(a: Int, b: Int): Int = a + b
  def add(a: Int, b: Int) = a + b
  ```

### Calling methods

- Invoking a method is straightforward: `val x = add(1, 2)   // 3`
- The Scala collections classes have dozens of built-in methods. These examples show how to call them:

  ```scala
  val x = List(1, 2, 3)

  x.size          // 3
  x.contains(1)   // true
  x.map(_ * 10)   // List(10, 20, 30)
  ```

### Multiline methods

- When a method is longer than one line, start the method body on the second line, indented to the right:

  ```scala
  def addThenDouble(a: Int, b: Int): Int =
    // imagine that this body requires multiple lines
    val sum = a + b
    sum * 2

  // In one line
  def addThenDouble(a: Int, b: Int): Int = (a + b) * 2
  ```

- Notice that there’s no need for a return statement at the end of the method. Because almost everything in Scala is an expression—meaning that each line of code returns (or evaluates to) a value—there’s no need to use return.
- As an example of a real-world multiline method, this getStackTraceAsString method converts its Throwable input parameter into a well-formatted String:
  ```scala
  def getStackTraceAsString(t: Throwable): String =
    val sw = StringWriter()
    t.printStackTrace(PrintWriter(sw))
    sw.toString
  ```

### Default parameter values

- Method parameters can have default values. In this example, default values are given for both the timeout and protocol parameters:
  ```scala
  def makeConnection(timeout: Int = 5_000, protocol: String = "http") =
    println(f"timeout = ${timeout}%d, protocol = ${protocol}%s")
    // more code here ...
  ```
- Because the parameters have default values, the method can be called in these ways:
  ```scala
  makeConnection()                 // timeout = 5000, protocol = http
  makeConnection(2_000)            // timeout = 2000, protocol = http
  makeConnection(3_000, "https")   // timeout = 3000, protocol = https
  ```

### Named parameters

- If you prefer, you can also use the names of the method parameters when calling a method. For instance, makeConnection can also be called in these ways:
  ```scala
  makeConnection(timeout=10_000)
  makeConnection(protocol="https")
  makeConnection(timeout=10_000, protocol="https")
  makeConnection(protocol="https", timeout=10_000)
  ```
- Without help from an IDE that code can be hard to read, but this code is much more clear and obvious:
  ```scala
  engage(
    speedIsSet = true,
    directionIsSet = true,
    picardSaidMakeItSo = true,
    turnedOffParkingBrake = false
  )
  ```

### A suggestion about methods that take no parameters

- When a method takes no parameters, it’s said to have an arity level of arity-0. Similarly, when a method takes one parameter it’s an arity-1 method. When you create arity-0 methods:
  - If the method performs side effects, such as calling println, declare the method with empty parentheses
  - If the method does not perform side effects—such as getting the size of a collection, which is similar to accessing a field on the collection—leave the parentheses off
- For example, this method performs a side effect, so it’s declared with empty parentheses:

  ```scala
  def speak() = println("hi")

  speak     // error: "method speak must be called with () argument"
  speak()   // prints "hi"
  ```

### Using if as a method body

- Because if/else expressions return a value, they can be used as the body of a method. Here’s a method named isTruthy that implements the Perl definitions of true and false:
  ```scala
  def isTruthy(a: Any) =
    if a == 0 || a == "" || a == false then
      false
    else
      true
  ```

### Using match as a method body

- A match expression can also be used as the entire method body, and often is. Here’s another version of isTruthy, written with a match expression :
  ```scala
  def isTruthy(a: Matchable) = a match
    case 0 | "" | false => false
    case _ => true
  ```

### Controlling visibility in classes

- In classes, objects, traits, and enums, Scala methods are public by default, so the Dog instance created here can access the speak method:

  ```scala
  class Dog:
    def speak() = println("Woof")

  val d = new Dog
  d.speak()   // prints "Woof"
  ```

- Methods can also be marked as private. This makes them private to the current class, so they can’t be called nor overridden in subclasses:

  ```scala
  class Animal:
    private def breathe() = println("I’m breathing")

  class Cat extends Animal:
    // this method won’t compile
    override def breathe() = println("Yo, I’m totally breathing")
  ```

- If you want to make a method private to the current class and also allow subclasses to call it or override it, mark the method as protected, as shown with the speak method in this example:

  ```scala
  class Animal:
    private def breathe() = println("I’m breathing")
    def walk() =
      breathe()
      println("I’m walking")
    protected def speak() = println("Hello?")

  class Cat extends Animal:
    override def speak() = println("Meow")

  val cat = new Cat
  cat.walk()
  cat.speak()
  cat.breathe()   // won’t compile because it’s private
  ```

- The protected setting means:
  - The method (or field) can be accessed by other instances of the same class
  - It is not visible by other code in the current package
  - It is available to subclasses

### Objects can contain methods

- Earlier you saw that traits and classes can have methods. The Scala object keyword is used to create a singleton class, and an object can also contain methods. This is a nice way to group a set of “utility” methods. For instance, this object contains a collection of methods that work on strings:

  ```scala
  object StringUtils:

    /**
    * Returns a string that is the same as the input string, but
    * truncated to the specified length.
    */
    def truncate(s: String, length: Int): String = s.take(length)

    /**
      * Returns true if the string contains only letters and numbers.
      */
    def lettersAndNumbersOnly_?(s: String): Boolean =
      s.matches("[a-zA-Z0-9]+")

    /**
    * Returns true if the given string contains any whitespace
    * at all. Assumes that `s` is not null.
    */
    def containsWhitespace(s: String): Boolean =
      s.matches(".*\\s.*")

  end StringUtils
  ```

### Extension methods

- There are many situations where you would like to add functionality to closed classes. For example, imagine that you have a Circle class, but you can’t change its source code. It could be defined like this in a third-party library:
  ```scala
  case class Circle(x: Double, y: Double, radius: Double)
  ```
- When you want to add methods to this class, you can define them as extension methods, like this:
  ```scala
  extension (c: Circle)
    def circumference: Double = c.radius * math.Pi * 2
    def diameter: Double = c.radius * 2
    def area: Double = math.Pi * c.radius * c.radius
  ```
- Now when you have a Circle instance named aCircle, you can call those methods like this:
  ```scala
  aCircle.circumference
  aCircle.diameter
  aCircle.area
  ```

## MAIN METHODS IN SCALA 3

### Writing one line programs

- Scala 3 offers a new way to define programs that can be invoked from the command line: Adding a @main annotation to a method turns it into entry point of an executable program:
  ```scala
  @main def hello() = println("Hello, World")
  ```
- To run this program, save the line of code in a file named as e.g. Hello.scala—the filename doesn’t have to match the method name—and run it with scala:
  ```scala
  $ scala Hello.scala
  Hello, World
  ```
- A @main annotated method can be written either at the top-level (as shown), or inside a statically accessible object. In either case, the name of the program is in each case the name of the method, without any object prefixes.

### Command line arguments

- With this approach your @main method can handle command line arguments, and those arguments can have different types. For example, given this @main method that takes an Int, a String, and a varargs String\* parameter:

  ```scala
  @main def happyBirthday(age: Int, name: String, others: String*) =
    val suffix = (age % 100) match
      case 11 | 12 | 13 => "th"
      case _ => (age % 10) match
        case 1 => "st"
        case 2 => "nd"
        case 3 => "rd"
        case _ => "th"

    val sb = StringBuilder(s"Happy $age$suffix birthday, $name")
    for other <- others do sb.append(" and ").append(other)
    println(sb.toString)
  ```

- When you compile that code, it creates a main program named happyBirthday that’s called like this:
  ```scala
  $ scala happyBirthday 23 Lisa Peter
  Happy 23rd Birthday, Lisa and Peter!
  ```
- As shown, the @main method can have an arbitrary number of parameters.
- For each parameter type there must be a given instance of the scala.util.CommandLineParser.FromString type class that converts an argument String to the required parameter type.
- Also as shown, a main method’s parameter list can end in a repeated parameter like String\* that takes all remaining arguments given on the command line.
- The program implemented from an @main method checks that there are enough arguments on the command line to fill in all parameters, and that the argument strings can be converted to the required types. If a check fails, the program is terminated with an error message:

  ```scala
  $ scala happyBirthday 22
  Illegal command line after first argument: more arguments expected

  $ scala happyBirthday sixty Fred
  Illegal command line: java.lang.NumberFormatException: For input string: "sixty"
  ```

### User-defined types as parameters

- As mentioned up above, the compiler looks for a given instance of the scala.util.CommandLineParser.FromString typeclass for the type of the argument. For example, let’s say you have a custom Color type that you want to use as a parameter. You would do this like you see below:

  ```scala
  enum Color:
    case Red, Green, Blue

  given CommandLineParser.FromString[Color] with
    def fromString(value: String): Color = Color.valueOf(value)

  @main def run(color: Color): Unit =
    println(s"The color is ${color.toString}")
  ```

### The details

- The Scala compiler generates a program from an @main method f as follows:
  - It creates a class named f in the package where the @main method was found.
  - The class has a static method main with the usual signature of a Java main method: it takes an Array[String] as argument and returns Unit.
  - The generated main method calls method f with arguments converted using methods in the scala.util.CommandLineParser.FromString object.
- For instance, the happyBirthday method above generates additional code equivalent to the following class:
  ```scala
  final class happyBirthday {
    import scala.util.{CommandLineParser as CLP}
    <static> def main(args: Array[String]): Unit =
      try
        happyBirthday(
            CLP.parseArgument[Int](args, 0),
            CLP.parseArgument[String](args, 1),
            CLP.parseRemainingArguments[String](args, 2)*)
      catch {
        case error: CLP.ParseError => CLP.showError(error)
      }
  }
  ```

### Backwards Compatibility with Scala 2

- @main methods are the recommended way to generate programs that can be invoked from the command line in Scala 3. They replace the previous approach in Scala 2, which was to create an object that extends the App class:
- The previous functionality of App, which relied on the “magic” DelayedInit trait, is no longer available. App still exists in limited form for now, but it doesn’t support command line arguments and will be deprecated in the future.
- If programs need to cross-build between Scala 2 and Scala 3, it’s recommended to use an object with an explicit main method and a single Array[String] argument instead:
