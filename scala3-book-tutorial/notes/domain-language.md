# Domain Language

**Source:**

- https://docs.scala-lang.org/scala3/book/domain-modeling-intro.html
- https://docs.scala-lang.org/scala3/book/domain-modeling-tools.html
- https://docs.scala-lang.org/scala3/book/domain-modeling-oop.html
- https://docs.scala-lang.org/scala3/book/domain-modeling-fp.html

## Tools

### Classes

- As with other languages, a class in Scala is a template for the creation of object instances. Here are some examples of classes:
  ```scala
  class Person(var name: String, var vocation: String)
  class Book(var title: String, var author: String, var year: Int)
  class Movie(var name: String, var director: String, var year: Int)
  ```
- All the parameters of our example classes are defined as var fields, which means they are mutable: you can read them, and also modify them. If you want them to be immutable—read only—create them as val fields instead, or use a case class.
- No need to use `new` keyword to create a new instance.
- Snippet:
  ```scala
  val p = Person("Robert Allen Zimmerman", "Harmonica Player")
  p.name       // "Robert Allen Zimmerman"
  p.vocation   // "Harmonica Player"
  p.name = "Bob Dylan"
  p.vocation = "Musician"
  ```

#### Fields and methods

- Classes can also have methods and additional fields that are not part of constructors. They are defined in the body of the class. The body is initialized as part of the default constructor:

  ```scala
  class Person(var firstName: String, var lastName: String):

    println("initialization begins")
    val fullName = firstName + " " + lastName

    // a class method
    def printFullName: Unit =
      // access the `fullName` field, which is created above
      println(fullName)

    printFullName
    println("initialization ends")
  ```

#### Default parameter values

- As a quick look at a few other features, class constructor parameters can also have default values:
  ```scala
  class Socket(val timeout: Int = 5_000, val linger: Int = 5_000):
    override def toString = s"timeout: $timeout, linger: $linger"
  ```
- A great thing about this feature is that it lets consumers of your code create classes in a variety of different ways, as though the class had alternate constructors:

  ```scala
  val s = Socket()                  // timeout: 5000, linger: 5000
  val s = Socket(2_500)             // timeout: 2500, linger: 5000
  val s = Socket(10_000, 10_000)    // timeout: 10000, linger: 10000
  val s = Socket(timeout = 10_000)  // timeout: 10000, linger: 5000
  val s = Socket(linger = 10_000)   // timeout: 5000, linger: 10000

  // option 1
  val s = Socket(10_000, 10_000)

  // option 2
  val s = Socket(
    timeout = 10_000,
    linger = 10_000
  )
  ```

#### Auxiliary constructors

- One way to handle this situation in an OOP style is with this code:

  ```scala
  import java.time.*

  // [1] the primary constructor
  class Student(
    var name: String,
    var govtId: String
  ):
    private var _applicationDate: Option[LocalDate] = None
    private var _studentId: Int = 0

    // [2] a constructor for when the student has completed
    // their application
    def this(
      name: String,
      govtId: String,
      applicationDate: LocalDate
    ) =
      this(name, govtId)
      _applicationDate = Some(applicationDate)

    // [3] a constructor for when the student is approved
    // and now has a student id
    def this(
      name: String,
      govtId: String,
      studentId: Int
    ) =
      this(name, govtId)
      _studentId = studentId

  val s1 = Student("Mary", "123")
  val s2 = Student("Mary", "123", LocalDate.now)
  val s3 = Student("Mary", "123", 456)
  ```

### Objects

- An object is a class that has exactly one instance. It’s initialized lazily when its members are referenced, similar to a lazy val.
- Objects in Scala allow grouping methods and fields under one namespace, similar to how you use static members on a class in Java, Javascript (ES6), or @staticmethod in Python.
- Declaring an object is similar to declaring a class. Here’s an example of a “string utilities” object that contains a set of methods for working with strings:

  ```scala
  object StringUtils:
    def truncate(s: String, length: Int): String = s.take(length)
    def containsWhitespace(s: String): Boolean = s.matches(".*\\s.*")
    def isNullOrEmpty(s: String): Boolean = s == null || s.trim.isEmpty

  StringUtils.truncate("Chuck Bartowski", 5)  // "Chuck"

  import StringUtils.*
  truncate("Chuck Bartowski", 5)       // "Chuck"
  containsWhitespace("Sarah Walker")   // true
  isNullOrEmpty("John Casey")          // false

  import StringUtils.{truncate, containsWhitespace}
  truncate("Charles Carmichael", 7)       // "Charles"
  containsWhitespace("Captain Awesome")   // true
  isNullOrEmpty("Morgan Grimes")          // Not found: isNullOrEmpty (error)

  object MathConstants:
    val PI = 3.14159
    val E = 2.71828

  println(MathConstants.PI)   // 3.14159
  ```

### Companion Objects

- An object that has the same name as a class, and is declared in the same file as the class, is called a “companion object.”
- Similarly, the corresponding class is called the object’s companion class. A companion class or object can access the private members of its companion.
- Companion objects are used for methods and values that are not specific to instances of the companion class. For instance, in the following example the class Circle has a member named area which is specific to each instance, and its companion object has a method named calculateArea that’s (a) not specific to an instance, and (b) is available to every instance:

  ```scala
  import scala.math.*

  class Circle(val radius: Double):
    def area: Double = Circle.calculateArea(radius)

  object Circle:
    private def calculateArea(radius: Double): Double = Pi * pow(radius, 2.0)

  val circle1 = Circle(5.0)
  circle1.area
  ```

#### Other uses

- As shown, they can be used to group “static” methods under a namespace
  These methods can be public or private
  If calculateArea was public, it would be accessed as Circle.calculateArea
- They can contain apply methods, which—thanks to some syntactic sugar—work as factory methods to construct new instances
- They can contain unapply methods, which are used to deconstruct objects, such as with pattern matching
- Here’s a quick look at how apply methods can be used as factory methods to create new objects:

  ```scala
  class Person:
    var name = ""
    var age = 0
    override def toString = s"$name is $age years old"

  object Person:

    // a one-arg factory method
    def apply(name: String): Person =
      var p = new Person
      p.name = name
      p

    // a two-arg factory method
    def apply(name: String, age: Int): Person =
      var p = new Person
      p.name = name
      p.age = age
      p

  end Person

  val joe = Person("Joe")
  val fred = Person("Fred", 29)

  //val joe: Person = Joe is 0 years old
  //val fred: Person = Fred is 29 years old
  ```

### Traits

- Traits can
  - Abstract methods and fields
  - Concrete methods and fields
- In a basic use, a trait can be used as an interface, defining only abstract members that will be implemented by other classes:

  ```scala
  trait Employee:
    def id: Int
    def firstName: String
    def lastName: String

  trait HasLegs:
    def numLegs: Int
    def walk(): Unit
    def stop() = println("Stopped walking")

  trait HasTail:
    def tailColor: String
    def wagTail() = println("Tail is wagging")
    def stopTail() = println("Tail is stopped")
  ```

- Notice how each trait only handles very specific attributes and behaviors: HasLegs deals only with legs, and HasTail deals only with tail-related functionality. Traits let you build small modules like this.
- Later in your code, classes can mix multiple traits to build larger components:
  ```scala
  class IrishSetter(name: String) extends HasLegs, HasTail:
    val numLegs = 4
    val tailColor = "Red"
    def walk() = println("I’m walking")
    override def toString = s"$name is a Dog"
  ```

### Abstract classes

- When you want to write a class, but you know it will have abstract members, you can either create a trait or an abstract class. In most situations you’ll use traits, but historically there have been two situations where it’s better to use an abstract class than a trait:
  - You want to create a base class that takes constructor arguments
  - The code will be called from Java code

#### A base class that takes constructor arguments

- Prior to Scala 3, when a base class needed to take constructor arguments, you’d declare it as an abstract class:

  ```scala
  abstract class Pet(name: String):
    def greeting: String
    def age: Int
    override def toString = s"My name is $name, I say $greeting, and I’m $age"

  class Dog(name: String, var age: Int) extends Pet(name):
    val greeting = "Woof"

  val d = Dog("Fido", 1)
  ```

- However, with Scala 3, traits can now have parameters, so you can now use traits in the same situation:

  ```scala
  trait Pet(name: String):
    def greeting: String
    def age: Int
    override def toString = s"My name is $name, I say $greeting, and I’m $age"

  class Dog(name: String, var age: Int) extends Pet(name):
    val greeting = "Woof"

  val d = Dog("Fido", 1)
  ```

- Traits are more flexible to compose—you can mix in multiple traits, but only extend one class—and should be preferred to classes and abstract classes most of the time. The rule of thumb is to use classes whenever you want to create instances of a particular type, and traits when you want to decompose and reuse behaviour.

### Enums (Scala 3 only)

- Basic enumerations are used to define sets of constants, like the months in a year, the days in a week, directions like north/south/east/west, and more.
- As an example, these enumerations define sets of attributes related to pizzas:

  ```scala
  enum CrustSize:
    case Small, Medium, Large

  enum CrustType:
    case Thin, Thick, Regular

  enum Topping:
    case Cheese, Pepperoni, BlackOlives, GreenOlives, Onions

  import CrustSize.*
  val currentCrustSize = Small
  ```

- Enum values can be compared using equals (==), and also matched on:

  ```scala
  // if/then
  if currentCrustSize == Large then
    println("You get a prize!")

  // match
  currentCrustSize match
    case Small => println("small")
    case Medium => println("medium")
    case Large => println("large")
  ```

#### Additional Enum Features

- Enumerations can also be parameterized:
  ```scala
  enum Color(val rgb: Int):
    case Red   extends Color(0xFF0000)
    case Green extends Color(0x00FF00)
    case Blue  extends Color(0x0000FF)
  ```
- And they can also have members (like fields and methods):

  ```scala
  enum Planet(mass: Double, radius: Double):
    private final val G = 6.67300E-11
    def surfaceGravity = G * mass / (radius * radius)
    def surfaceWeight(otherMass: Double) =
      otherMass * surfaceGravity

    case Mercury extends Planet(3.303e+23, 2.4397e6)
    case Earth   extends Planet(5.976e+24, 6.37814e6)
    // more planets here ...
  ```

#### Compatibility with Java Enums

- If you want to use Scala-defined enums as Java enums, you can do so by extending the class java.lang.Enum (which is imported by default) as follows:
  ```scala
  enum Color extends Enum[Color] { case Red, Green, Blue }
  ```

### Case classes

- Case classes are used to model immutable data structures. Take the following example:
  ```scala
  case class Person(name: String, relation: String)
  val christina = Person("Christina", "niece")
  christina.name = "Fred"   // error: reassignment to val
  ```
- Since the fields of a case class are assumed to be immutable, the Scala compiler can generate many helpful methods for you:
  - An unapply method is generated, which allows you to perform pattern matching on a case class (that is, case Person(n, r) => ...).
  - A copy method is generated in the class, which is very useful to create modified copies of an instance.
  - equals and hashCode methods using structural equality are generated, allowing you to use instances of case classes in Maps.
  - A default toString method is generated, which is helpful for debugging.
- These additional features are demonstrated in the below example:

  ```scala
  // Case classes can be used as patterns
  christina match
    case Person(n, r) => println("name is " + n)

  // `equals` and `hashCode` methods generated for you
  val hannah = Person("Hannah", "niece")
  christina == hannah       // false

  // `toString` method
  println(christina)        // Person(Christina,niece)

  // built-in `copy` method
  case class BaseballTeam(name: String, lastWorldSeriesWin: Int)
  val cubs1908 = BaseballTeam("Chicago Cubs", 1908)
  val cubs2016 = cubs1908.copy(lastWorldSeriesWin = 2016)
  // result:
  // cubs2016: BaseballTeam = BaseballTeam(Chicago Cubs,2016)
  ```

#### Support for functional programming

- In FP, you try to avoid mutating data structures. It thus makes sense that constructor fields default to val. Since instances of case classes can’t be changed, they can easily be shared without fearing mutation or race conditions.
- Instead of mutating an instance, you can use the copy method as a template to create a new (potentially changed) instance. This process can be referred to as “update as you copy.”
- Having an unapply method auto-generated for you also lets case classes be used in advanced ways with pattern matching.

### Case objects

- Case objects are to objects what case classes are to classes: they provide a number of automatically-generated methods to make them more powerful.
- They’re particularly useful whenever you need a singleton object that needs a little extra functionality, such as being used with pattern matching in match expressions.
- Case objects are useful when you need to pass immutable messages around. For instance, if you’re working on a music player project, you’ll create a set of commands or messages like this:
  ```scala
  sealed trait Message
  case class PlaySong(name: String) extends Message
  case class IncreaseVolume(amount: Int) extends Message
  case class DecreaseVolume(amount: Int) extends Message
  case object StopPlaying extends Message
  ```
- Then in other parts of your code, you can write methods like this, which use pattern matching to handle the incoming message (assuming the methods playSong, changeVolume, and stopPlayingSong are defined somewhere else):
  ```scala
  def handleMessages(message: Message): Unit = message match
    case PlaySong(name)         => playSong(name)
    case IncreaseVolume(amount) => changeVolume(amount)
    case DecreaseVolume(amount) => changeVolume(-amount)
    case StopPlaying            => stopPlayingSong()
  ```

## OOP Modeling

## FP Modeling
