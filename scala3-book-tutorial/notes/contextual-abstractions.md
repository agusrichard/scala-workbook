# Contextual Abstractions

**Sources:**
- https://docs.scala-lang.org/scala3/book/ca-contextual-abstractions-intro.html


## Extension Methods
- Extension methods let you add methods to a type after the type is defined, i.e., they let you add new methods to closed classes.
- For example, imagine that someone else has created a Circle class:
  ```scala
  case class Circle(x: Double, y: Double, radius: Double)
  ```
- Now imagine that you need a circumference method, but you can’t modify their source code. Before the concept of term inference was introduced into programming languages, the only thing you could do was write a method in a separate class or object like this:
  ```scala
  object CircleHelpers:
    def circumference(c: Circle): Double = c.radius * math.Pi * 2
  ```
- Then you’d use that method like this:
  ```scala
  val aCircle = Circle(2, 3, 5)

  // without extension methods
  CircleHelpers.circumference(aCircle)
  ```
- But with extension methods you can create a circumference method to work on Circle instances:
  ```scala
  extension (c: Circle)
    def circumference: Double = c.radius * math.Pi * 2
  ```
- In this code:
  - Circle is the type that the extension method circumference will be added to
  - The c: Circle syntax lets you reference the variable c in your extension method(s)
- Then in your code you use circumference just as though it was originally defined in the Circle class:

### Import extension method
- Imagine, that circumference is defined in package lib, you can import it by
  ```scala
  import lib.circumference

  aCircle.circumference
  ```
- The compiler also supports you if the import is missing by showing a detailed compilation error message such as the following:
  ```
  value circumference is not a member of Circle, but could be made available as an extension method.

  The following import might fix the problem:

    import lib.circumference
  ```
- The extension keyword declares that you’re about to define one or more extension methods on the type that’s put in parentheses. To define multiple extension methods on a type, use this syntax:
  ```scala
  extension (c: Circle)
    def circumference: Double = c.radius * math.Pi * 2
    def diameter: Double = c.radius * 2
    def area: Double = math.Pi * c.radius * c.radius
  ```

## Context Parameters
- When designing a system, often context information like configuration or settings need to be provided to the different components of your system. One common way to achieve this is by passing the configuration as additional argument to your methods.
- In the following example, we define a case class Config to model some website configuration and pass it around in the different methods.
  ```scala
  case class Config(port: Int, baseUrl: String)

  def renderWebsite(path: String, config: Config): String =
    "<html>" + renderWidget(List("cart"), config)  + "</html>"

  def renderWidget(items: List[String], config: Config): String = ???

  val config = Config(8080, "docs.scala-lang.org")
  renderWebsite("/home", config)
  ```
- Let us assume that the configuration does not change throughout most of our code base. Passing config to each and every method call (like renderWidget) becomes very tedious and makes our program more difficult to read, since we need to ignore the config argument.

### Marking parameters as contextual
- We can mark some parameters of our methods as contextual.
  ```scala
  def renderWebsite(path: String)(using config: Config): String =
      "<html>" + renderWidget(List("cart")) + "</html>"
      //                                  ^
      //                   no argument config required anymore

  def renderWidget(items: List[String])(using config: Config): String = ???
  ```
- By starting a parameter section with the keyword using in Scala 3 or implicit in Scala 2, we tell the compiler that at the call-site it should automatically find an argument with the correct type. The Scala compiler thus performs term inference.
- In our call to renderWidget(List("cart")) the Scala compiler will see that there is a term of type Config in scope (the config) and automatically provide it to renderWidget. So the program is equivalent to the one above.
- In fact, since we do not need to refer to config in our implementation of renderWebsite anymore, we can even omit its name in the signature in Scala 3:
  ```scala
  //        no need to come up with a parameter name
  //                             vvvvvvvvvvvvv
  def renderWebsite(path: String)(using Config): String =
      "<html>" + renderWidget(List("cart")) + "</html>"
  ```

### Explicitly providing contextual arguments
- We have seen how to abstract over contextual parameters and that the Scala compiler can provide arguments automatically for us. But how can we specify which configuration to use for our call to renderWebsite?
  ```scala
  renderWebsite("/home")(using config)
  ```
- Explicitly providing contextual parameters can be useful if we have multiple different values in scope that would make sense, and we want to make sure that the correct one is passed to the function.

### Given Instances (Implicit Definitions in Scala 2)
- We have seen that we can explicitly pass arguments as contextual parameters. However, if there is a single canonical value for a particular type, there is another preferred way to make it available to the Scala compiler: by marking it as given in Scala 3 or implicit in Scala 2.
  ```scala
  val config = Config(8080, "docs.scala-lang.org")

  // this is the type that we want to provide the
  // canonical value for
  //    vvvvvv
  given Config = config
  //             ^^^^^^
  // this is the value the Scala compiler will infer
  // as argument to contextual parameters of type Config
  ```
- In the above example we specify that whenever a contextual parameter of type Config is omitted in the current scope, the compiler should infer config as an argument.
- Having defined a canonical value for the type Config, we can call renderWebsite as follows:
```scala
  renderWebsite("/home")
  //                   ^
  //   again no argument
  ```

## Context Bounds

### Background
- For example, consider a method maxElement that returns the maximum value in a collection:
  ```scala
  def maxElement[A](as: List[A])(using ord: Ord[A]): A =
    as.reduceLeft(max(_, _)(using ord))
  ```
- The method maxElement takes a context parameter of type Ord[A] only to pass it on as an argument to the method max.
- For the sake of completeness, here are the definitions of max and Ord (note that in practice we would use the existing method max on List, but we made up this example for illustration purpose):
  ```scala
  /** Defines how to compare values of type `A` */
  trait Ord[A]:
    def greaterThan(a1: A, a2: A): Boolean

  /** Returns the maximum of two values */
  def max[A](a1: A, a2: A)(using ord: Ord[A]): A =
    if ord.greaterThan(a1, a2) then a1 else a2
  ```
- Note that the method max takes a context parameter of type Ord[A], like the method maxElement.

### Omitting context arguments
- Since ord is a context parameter in the method max, the compiler can supply it for us in the implementation of maxElement, when we call the method max:
  ```scala
  def maxElement[A](as: List[A])(using Ord[A]): A =
    as.reduceLeft(max(_, _))
  ```
- Note that, because we don’t need to explicitly pass it to the method max, we can leave out its name in the definition of the method maxElement. This is an anonymous context parameter.

### Context bounds
- Given that background, a context bound is a shorthand syntax for expressing the pattern of, “a context parameter applied to a type parameter.”
- Using a context bound, the maxElement method can be written like this:
  ```scala
  def maxElement[A: Ord](as: List[A]): A =
    as.reduceLeft(max(_, _))
  ```
- A bound like : Ord on a type parameter A of a method or class indicates a context parameter with type Ord[A]. Under the hood, the compiler transforms this syntax into the one shown in the Background section.

## Given Imports (Scala3)
- To make it more clear where givens in the current scope are coming from, a special form of the import statement is used to import given instances. The basic form is shown in this example:
  ```scala
  object A:
    class TC
    given tc: TC = ???
    def f(using TC) = ???

  object B:
    import A.*       // import all non-given members
    import A.given   // import the given instance
  ```
- In this code the import A.* clause of object B imports all members of A except the given instance, tc. Conversely, the second import, import A.given, imports only that given instance. The two import clauses can also be merged into one:
  ```scala
  object B:
    import A.{given, *}
  ```

## Type Classes
- A type class is an abstract, parameterized type that lets you add new behavior to any closed data type without using sub-typing. 

### The type class
- The first step in creating a type class is to declare a parameterized trait that has one or more abstract methods. Because Showable only has one method named show, it’s written like this:
  ```scala
  // a type class
  trait Showable[A]:
    extension (a: A) def show: String
  ```
- Notice that this approach is close to the usual object-oriented approach, where you would typically define a trait Show as follows:
  ```scala
  // a trait
  trait Show:
    def show: String
  ```
- There are a few important things to point out:
  - Type-classes like Showable take a type parameter A to say which type we provide the implementation of show for; in contrast, classic traits like Show do not.
  - To add the show functionality to a certain type A, the classic trait requires that A extends Show, while for type-classes we require to have an implementation of Showable[A].
  - In Scala 3, to allow the same method calling syntax in both Showable that mimics the one of Show, we define Showable.show as an extension method.

### Implement concrete instances
- The next step is to determine what classes in your application Showable should work for, and then implement that behavior for them. For instance, to implement Showable for this Person class:
  ```scala
  case class Person(firstName: String, lastName: String)
  ```
- you’ll define a single canonical value of type Showable[Person], ie an instance of Showable for the type Person, as the following code example demonstrates:
  ```scala
  given Showable[Person] with
    extension (p: Person) def show: String =
      s"${p.firstName} ${p.lastName}"
  ```

### Using the type class
- Now you can use this type class like this:
  ```scala
  val person = Person("John", "Doe")
  println(person.show)
  ```
- Again, if Scala didn’t have a toString method available to every class, you could use this technique to add Showable behavior to any class that you want to be able to convert to a String.

### Writing methods that use the type class
- As with inheritance, you can define methods that use Showable as a type parameter:
  ```scala
  def showAll[A: Showable](as: List[A]): Unit =
    as.foreach(a => println(a.show))

  showAll(List(Person("Jane"), Person("Mary")))
  ```

### A type class with multiple methods
- Note that if you want to create a type class that has multiple methods, the initial syntax looks like this:
  ```scala
  trait HasLegs[A]:
    extension (a: A)
      def walk(): Unit
      def run(): Unit
  ```

## Multiversal Equality

### Allowing the comparison of class instances
- By default, in Scala 3 you can still create an equality comparison like this:
  ```scala
  case class Cat(name: String)
  case class Dog(name: String)
  val d = Dog("Fido")
  val c = Cat("Morris")

  d == c  // false, but it compiles
  ```
- But with Scala 3 you can disable such comparisons. By (a) importing scala.language.strictEquality or (b) using the -language:strictEquality compiler flag, this comparison no longer compiles:
  ```scala
  import scala.language.strictEquality

  val rover = Dog("Rover")
  val fido = Dog("Fido")
  println(rover == fido)   // compiler error

  // compiler error message:
  // Values of types Dog and Dog cannot be compared with == or !=
  ```

### Enabling comparisons
- There are two ways to enable this comparison using the Scala 3 CanEqual type class. For simple cases like this, your class can derive the CanEqual class:
  ```scala
  // Option 1
  case class Dog(name: String) derives CanEqual
  ```
- As you’ll see in a few moments, when you need more flexibility you can also use this syntax:
  ```scala
  // Option 2
  case class Dog(name: String)
  given CanEqual[Dog, Dog] = CanEqual.derived
  ```
- Either of those two approaches now let Dog instances to be compared to each other.

### A more real-world example
- In a more real-world example, imagine you have an online bookstore and want to allow or disallow the comparison of physical, printed books, and audiobooks. With Scala 3 you start by enabling multiversal equality as shown in the previous example:
  ```scala
  // [1] add this import, or this command line flag: -language:strictEquality
  import scala.language.strictEquality
  ```
- Then create your domain objects as usual:
  ```scala
  // [2] create your class hierarchy
  trait Book:
      def author: String
      def title: String
      def year: Int

  case class PrintedBook(
      author: String,
      title: String,
      year: Int,
      pages: Int
  ) extends Book

  case class AudioBook(
      author: String,
      title: String,
      year: Int,
      lengthInMinutes: Int
  ) extends Book
  ```
- Finally, use CanEqual to define which comparisons you want to allow:
  ```scala
  // [3] create type class instances to define the allowed comparisons.
  //     allow `PrintedBook == PrintedBook`
  //     allow `AudioBook == AudioBook`
  given CanEqual[PrintedBook, PrintedBook] = CanEqual.derived
  given CanEqual[AudioBook, AudioBook] = CanEqual.derived

  // [4a] comparing two printed books works as desired
  val p1 = PrintedBook("1984", "George Orwell", 1961, 328)
  val p2 = PrintedBook("1984", "George Orwell", 1961, 328)
  println(p1 == p2)         // true

  // [4b] you can’t compare a printed book and an audiobook
  val pBook = PrintedBook("1984", "George Orwell", 1961, 328)
  val aBook = AudioBook("1984", "George Orwell", 2006, 682)
  println(pBook == aBook)   // compiler error
  ```
- The last line of code results in this compiler error message:
  ```
  Values of types PrintedBook and AudioBook cannot be compared with == or !=
  ```
- This is how multiversal equality catches illegal type comparisons at compile time.
- Enabling “PrintedBook == AudioBook”
  ```scala
  // allow `PrintedBook == AudioBook`, and `AudioBook == PrintedBook`
  given CanEqual[PrintedBook, AudioBook] = CanEqual.derived
  given CanEqual[AudioBook, PrintedBook] = CanEqual.derived
  ```
- Now you can compare physical books to audiobooks without a compiler error:
  ```scala
  println(pBook == aBook)   // false
  println(aBook == pBook)   // false
  ```
- While these comparisons are now allowed, they will always be false because their equals methods don’t know how to make these comparisons. Therefore, the solution is to override the equals methods for each class. For instance, when you override the equals method for AudioBook:
  ```scala
  case class AudioBook(
      author: String,
      title: String,
      year: Int,
      lengthInMinutes: Int
  ) extends Book:
      // override to allow AudioBook to be compared to PrintedBook
      override def equals(that: Any): Boolean = that match
          case a: AudioBook =>
              this.author == a.author
              && this.title == a.title
              && this.year == a.year
              && this.lengthInMinutes == a.lengthInMinutes
          case p: PrintedBook =>
              this.author == p.author && this.title == p.title
          case _ =>
              false
  ```
- You can now compare an AudioBook to a PrintedBook:
  ```scala
  println(aBook == pBook)   // true (works because of `equals` in `AudioBook`)
  println(pBook == aBook)   // false
  ```
- Currently, the PrintedBook book doesn’t have an equals method, so the second comparison returns false. To enable that comparison, just override the equals method in PrintedBook.

## Implicit Conversions
- Implicit conversions are a powerful Scala feature that allows users to supply an argument of one type as if it were another type, to avoid boilerplate.

### Example
- Consider for instance a method findUserById that takes a parameter of type Long:
  ```scala
  def findUserById(id: Long): Option[User]
  ```
- We omit the definition of the type User for the sake of brevity, it does not matter for our example.
- In Scala, it is possible to call the method findUserById with an argument of type Int instead of the expected type Long, because the argument will be implicitly converted into the type Long:
  ```scala
  val id: Int = 42
  findUserById(id) // OK
  ```
- This code does not fail to compile with an error like “type mismatch: expected Long, found Int” because there is an implicit conversion that converts the argument id to a value of type Long

### Defining an Implicit Conversion
- In Scala 3, an implicit conversion from type S to type T is defined by a given instance of type scala.Conversion[S, T]. For compatibility with Scala 2, it can also be defined by an implicit method (read more in the Scala 2 tab). For example, this code defines an implicit conversion from Int to Long:
  ```scala
  given int2long: Conversion[Int, Long] with
    def apply(x: Int): Long = x.toLong

  given Conversion[Int, Long] with
    def apply(x: Int): Long = x.toLong
  
  given Conversion[Int, Long] = (x: Int) => x.toLong
  ```
- In our example above, when we pass the argument id of type Int to the method findUserById, the implicit conversion int2long(id) is inserted.
- An example is to compare two strings "foo" < "bar". In this case, String has no member <, so the implicit conversion Predef.augmentString("foo") < "bar" is inserted. (scala.Predef is automatically imported into all Scala programs.)

### How Are Implicit Conversions Brought Into Scope?
- first, it looks into the current lexical scope
  - implicit conversions defined in the current scope or the outer scopes
  - imported implicit conversions
  - implicit conversions imported by a wildcard import (Scala 2 only)
- then, it looks into the companion objects associated with the argument type S or the expected type T. The companion objects associated with a type X are:
  - the companion object X itself
  - the companion objects associated with any of X’s inherited types
  - the companion objects associated with any type argument in X
  - if X is an inner class, the outer objects in which it is embedded
- For instance, consider an implicit conversion fromStringToUser defined in an object Conversions:
  ```scala
  object Conversions:
    given fromStringToUser: Conversion[String, User] = (name: String) => User(name)
  ```
- The following imports would equivalently bring the conversion into scope:
  ```scala
  import Conversions.fromStringToUser
  // or
  import Conversions._
  import Conversions.fromStringToUser
  // or
  import Conversions.given
  // or
  import Conversions.{given Conversion[String, User]}
  ```
- In the introductory example, the conversion from Int to Long does not require an import because it is defined in the object Int, which is the companion object of the type Int.