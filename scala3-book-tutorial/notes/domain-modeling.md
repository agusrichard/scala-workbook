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

### Introduction

Scala provides all the necessary tools for object-oriented design:

- Traits let you specify (abstract) interfaces, as well as concrete implementations.
- Mixin Composition gives you the tools to compose components from smaller parts.
- Classes can implement the interfaces specified by traits.
- Instances of classes can have their own private state.
- Subtyping lets you use an instance of one class where an instance of a superclass is expected.
- Access modifiers lets you control which members of a class can be accessed by which part of the code.

### Traits

- They can serve to describe abstract interfaces like:

  ```scala
  trait Showable:
    def show: String

  trait Showable:
    def show: String
    def showHtml = "<p>" + show + "</p>"
  ```

- Odersky and Zenger present the service-oriented component model and view:
  - abstract members as required services: they still need to be implemented by a subclass.
  - concrete members as provided services: they are provided to the subclass.
- We can already see this with our example of Showable: defining a class Document that extends Showable, we still have to define show, but are provided with showHtml:
  ```scala
  class Document(text: String) extends Showable:
    def show = text
  ```
- Abstract methods are not the only thing that can be left abstract in a trait. A trait can contain:
  - abstract methods (def m(): T)
  - abstract value definitions (val x: T)
  - abstract type members (type T), potentially with bounds (type T <: S)
  - abstract givens (given t: T) SCALA 3 ONLY

### Mixin Composition

- Scala also provides a powerful way to compose multiple traits: a feature which is often referred to as mixin composition.
- Let us assume the following two (potentially independently defined) traits:

  ```scala
  trait GreetingService:
    def translate(text: String): String
    def sayHello = translate("Hello")

  trait TranslationService:
    def translate(text: String): String = "..."
  ```

- To compose the two services, we can simply create a new trait extending them:
  ```scala
  trait ComposedService extends GreetingService, TranslationService
  ```
- Abstract members in one trait (such as translate in GreetingService) are automatically matched with concrete members in another trait. This not only works with methods as in this example, but also with all the other abstract members mentioned above (that is, types, value definitions, etc.).

### Classes

- Traits are great to modularize components and describe interfaces (required and provided). But at some point we’ll want to create instances of them. When designing software in Scala, it’s often helpful to only consider using classes at the leafs of your inheritance model:
  | Traits | T1, T2, T3 |
  |-----------------|----------------------|
  | Composed traits| S1 extends T1, T2, S2 extends T2, T3 |
  | Classes | C extends S1, T3 |
  | Instances | C() |
- This is even more the case in Scala 3, where traits now can also take parameters, further eliminating the need for classes.

- Like traits, classes can extend multiple traits (but only one super class):
  ```scala
  class MyService(name: String) extends ComposedService, Showable:
  def show = s"$name says $sayHello"
  ```
- We can create an instance of MyService as follows:
  ```scala
  val s1: MyService = MyService("Service 1")
  ```
- Through the means of subtyping, our instance s1 can be used everywhere that any of the extended traits is expected:
  ```scala
  val s2: GreetingService = s1
  val s3: TranslationService = s1
  val s4: Showable = s1
  // ... and so on ...
  ```
- As mentioned before, it is possible to extend another class:
  ```scala
  class Person(name: String)
  class SoftwareDeveloper(name: String, favoriteLang: String)
    extends Person(name)
  ```

#### Open Classes SCALA 3 ONLY

- In Scala 3 extending non-abstract classes in other files is restricted. In order to allow this, the base class needs to be marked as open:
  ```scala
  open class Person(name: String)
  ```
- Marking classes with open is a new feature of Scala 3. Having to explicitly mark classes as open avoids many common pitfalls in OO design. In particular, it requires library designers to explicitly plan for extension and for instance document the classes that are marked as open with additional extension contracts.

### Instances and Private Mutable State

- Like in other languages with support for OOP, traits and classes in Scala can define mutable fields:

  ```scala
  class Counter:
    // can only be observed by the method `count`
    private var currentCount = 0

    def tick(): Unit = currentCount += 1
    def count: Int = currentCount

  val c1 = Counter()
  c1.count // 0
  c1.tick()
  c1.tick()
  c1.count // 2
  ```

- Access Modifiers: By default, all member definitions in Scala are publicly visible. To hide implementation details, it’s possible to define members (methods, fields, types, etc.) to be private or protected. This way you can control how they are accessed or overridden. Private members are only visible to the class/trait itself and to its companion object. Protected members are also visible to subclasses of the class.

### Advanced Example: Service Oriented Design

- In the following, we illustrate some advanced features of Scala and show how they can be used to structure larger software components. The examples are adapted from the paper “Scalable Component Abstractions” by Martin Odersky and Matthias Zenger. Don’t worry if you don’t understand all the details of the example; it’s primarily intended to demonstrate how to use several type features to construct larger components.
- Our goal is to define a software component with a family of types that can be refined later in implementations of the component. Concretely, the following code defines the component SubjectObserver as a trait with two abstract type members, S (for subjects) and O (for observers):

  ```scala
  trait SubjectObserver:

    type S <: Subject
    type O <: Observer

    trait Subject:
      self: S =>
        private var observers: List[O] = List()
        def subscribe(obs: O): Unit =
          observers = obs :: observers
        def publish() =
          for obs <- observers do obs.notify(this)

    trait Observer:
      def notify(sub: S): Unit
  ```

#### Abstract Type Members

- The declaration type S <: Subject says that within the trait SubjectObserver we can refer to some unknown (that is, abstract) type that we call S. However, the type is not completely unknown: we know at least that it is some subtype of the trait Subject. All traits and classes extending SubjectObserver are free to choose any type for S as long as the chosen type is a subtype of Subject. The <: Subject part of the declaration is also referred to as an upper bound on S.

#### Nested Traits

- Within trait SubjectObserver, we define two other traits. Let us begin with trait Observer, which only defines one abstract method notify that takes an argument of type S. As we will see momentarily, it is important that the argument has type S and not type Subject.

- The second trait, Subject, defines one private field observers to store all observers that subscribed to this particular subject. Subscribing to a subject simply stores the object into this list. Again, the type of parameter obs is O, not Observer.

#### Self-type Annotations

- Finally, you might have wondered what the self: S => on trait Subject is supposed to mean. This is called a self-type annotation. It requires subtypes of Subject to also be subtypes of S. This is necessary to be able to call obs.notify with this as an argument, since it requires a value of type S. If S was a concrete type, the self-type annotation could be replaced by trait Subject extends S.

#### Implementing the Component

- We can now implement the above component and define the abstract type members to be concrete types:

  ```scala
  object SensorReader extends SubjectObserver:
    type S = Sensor
    type O = Display

    class Sensor(val label: String) extends Subject:
      private var currentValue = 0.0
      def value = currentValue
      def changeValue(v: Double) =
        currentValue = v
        publish()

    class Display extends Observer:
      def notify(sub: Sensor) =
        println(s"${sub.label} has value ${sub.value}")
  ```

- Specifically, we define a singleton object SensorReader that extends SubjectObserver. In the implementation of SensorReader, we say that type S is now defined as type Sensor, and type O is defined to be equal to type Display. Both Sensor and Display are defined as nested classes within SensorReader, implementing the traits Subject and Observer, correspondingly.
- Besides, being an example of a service oriented design, this code also highlights many aspects of object-oriented programming:
  - The class Sensor introduces its own private state (currentValue) and encapsulates modification of the state behind the method changeValue.
  - The implementation of changeValue uses the method publish defined in the extended trait.
  - The class Display extends the trait Observer, and implements the missing method notify.

#### Using the Component

- Finally, the following code illustrates how to use our SensorReader component:

  ```scala
  import SensorReader.*

  // setting up a network
  val s1 = Sensor("sensor1")
  val s2 = Sensor("sensor2")
  val d1 = Display()
  val d2 = Display()
  s1.subscribe(d1)
  s1.subscribe(d2)
  s2.subscribe(d1)

  // propagating updates through the network
  s1.changeValue(2)
  s2.changeValue(3)

  // prints:
  // sensor1 has value 2.0
  // sensor1 has value 2.0
  // sensor2 has value 3.0
  ```

## FP Modeling

### Introduction

- In FP, the data and the operations on that data are two separate things; you aren’t forced to encapsulate them together like you do with OOP.
- The concept is similar to numerical algebra. When you think about whole numbers whose values are greater than or equal to zero, you have a set of possible values that looks like this:
  ```text
  0, 1, 2 ... Int.MaxValue
  ```
- Ignoring the division of whole numbers, the possible operations on those values are:
  ```text
  +, -, *
  ```
- In FP, business domains are modeled in a similar way:
  - You describe your set of values (your data)
  - You describe operations that work on those values (your functions)
- As we will see, reasoning about programs in this style is quite different from the object-oriented programming. Data in FP simply is: Separating functionality from your data lets you inspect your data without having to worry about behavior.

### Modeling the Data

- In Scala, describing the data model of a programming problem is simple:
  - If you want to model data with different alternatives, use the enum construct, (or case object in Scala 2).
  - If you only want to group things (or need more fine-grained control) use case classes

#### Describing Alternatives

- Data that simply consists of different alternatives, like crust size, crust type, and toppings, is precisely modelled in Scala by an enumeration.

  ```scala
  enum CrustSize:
    case Small, Medium, Large

  enum CrustType:
    case Thin, Thick, Regular

  enum Topping:
    case Cheese, Pepperoni, BlackOlives, GreenOlives, Onions
  ```

#### Describing Compound Data

- A pizza can be thought of as a compound container of the different attributes above. We can use a case class to describe that a Pizza consists of a crustSize, crustType, and potentially multiple toppings:

  ```scala
  import CrustSize.*
  import CrustType.*
  import Topping.*

  case class Pizza(
    crustSize: CrustSize,
    crustType: CrustType,
    toppings: Seq[Topping]
  )
  ```

- And that’s it. That’s the data model for an FP-style pizza system. This solution is very concise because it doesn’t require the operations on a pizza to be combined with the data model.
- The data model is easy to read, like declaring the design for a relational database. It is also very easy to create values of our data model and inspect them:
  ```scala
  val myFavPizza = Pizza(Small, Regular, Seq(Cheese, Pepperoni))
  println(myFavPizza.crustType) // prints Regular
  ```

#### More of the data model

- We might go on in the same way to model the entire pizza-ordering system. Here are a few other case classes that are used to model such a system:

  ```scala
  case class Address(
    street1: String,
    street2: Option[String],
    city: String,
    state: String,
    zipCode: String
  )

  case class Customer(
    name: String,
    phone: String,
    address: Address
  )

  case class Order(
    pizzas: Seq[Pizza],
    customer: Customer
  )
  ```

- In his book, Functional and Reactive Domain Modeling, Debasish Ghosh states that where OOP practitioners describe their classes as “rich domain models” that encapsulate data and behaviors, FP data models can be thought of as “skinny domain objects.” This is because—as this lesson shows—the data models are defined as case classes with attributes, but no behaviors, resulting in short and concise data structures.

### Modeling the Operations

- For instance, we can define a function that computes the price of a pizza.
  ```scala
  def pizzaPrice(p: Pizza): Double = p match
    case Pizza(crustSize, crustType, toppings) =>
      val base  = 6.00
      val crust = crustPrice(crustSize, crustType)
      val tops  = toppings.map(toppingPrice).sum
      base + crust + tops
  ```
- You can notice how the implementation of the function simply follows the shape of the data: since Pizza is a case class, we use pattern matching to extract the components and call helper functions to compute the individual prices.
  ```scala
  def toppingPrice(t: Topping): Double = t match
    case Cheese | Onions => 0.5
    case Pepperoni | BlackOlives | GreenOlives => 0.75
  ```
- Similarly, since Topping is an enumeration, we use pattern matching to distinguish between the different variants. Cheese and onions are priced at 50ct while the rest is priced at 75ct each.
  ```scala
  def crustPrice(s: CrustSize, t: CrustType): Double =
    (s, t) match
      // if the crust size is small or medium,
      // the type is not important
      case (Small | Medium, _) => 0.25
      case (Large, Thin) => 0.50
      case (Large, Regular) => 0.75
      case (Large, Thick) => 1.00
  ```
- An important point about all functions shown above is that they are pure functions: they do not mutate any data or have other side-effects (like throwing exceptions or writing to a file). All they do is simply receive values and compute the result.

### How to Organize Functionality

- There are several different ways to implement and organize behaviors:
  - Define your functions in companion objects
  - Use a modular programming style
  - Use a “functional objects” approach
  - Define the functionality in extension methods

#### Companion Object

- A companion object is an object that has the same name as a class, and is declared in the same file as the class.
- With this approach, in addition to the enumeration or case class you also define an equally named companion object that contains the behavior.

  ```scala
  case class Pizza(
    crustSize: CrustSize,
    crustType: CrustType,
    toppings: Seq[Topping]
  )

  // the companion object of case class Pizza
  object Pizza:
    // the implementation of `pizzaPrice` from above
    def price(p: Pizza): Double = ...

  enum Topping:
    case Cheese, Pepperoni, BlackOlives, GreenOlives, Onions

  // the companion object of enumeration Topping
  object Topping:
    // the implementation of `toppingPrice` above
    def price(t: Topping): Double = ...

  val pizza1 = Pizza(Small, Thin, Seq(Cheese, Onions))
  Pizza.price(pizza1)
  ```

- Grouping functionality this way has a few advantages:
  - It associates functionality with data and makes it easier to find for programmers (and the compiler).
  - It creates a namespace and for instance lets us use price as a method name without having to rely on overloading.
  - The implementation of Topping.price can access enumeration values like Cheese without having to import them.
- However, there are also a few tradeoffs that should be considered:
  - It tightly couples the functionality to your data model. In particular, the companion object needs to be defined in the same file as your case class.
  - It might be unclear where to define functions like crustPrice that could equally well be placed in a companion object of CrustSize or CrustType.

### Modules

- A second way to organize behavior is to use a “modular” approach. The book, Programming in Scala, defines a module as, “a ‘smaller program piece’ with a well-defined interface and a hidden implementation.” Let’s look at what this means.

#### Creating a PizzaService interface

- The first thing to think about are the Pizzas “behaviors”. When doing this, you sketch a PizzaServiceInterface trait like this:

  ```scala
  trait PizzaServiceInterface:

    def price(p: Pizza): Double

    def addTopping(p: Pizza, t: Topping): Pizza
    def removeAllToppings(p: Pizza): Pizza

    def updateCrustSize(p: Pizza, cs: CrustSize): Pizza
    def updateCrustType(p: Pizza, ct: CrustType): Pizza
  ```

- When you write a pure interface like this, you can think of it as a contract that states, “all non-abstract classes that extend this trait must provide an implementation of these services.”

#### Creating a concrete implementation

- Now that you know what the PizzaServiceInterface looks like, you can create a concrete implementation of it by writing the body for all of the methods you defined in the interface:

  ```scala
  object PizzaService extends PizzaServiceInterface:

    def price(p: Pizza): Double =
      ... // implementation from above

    def addTopping(p: Pizza, t: Topping): Pizza =
      p.copy(toppings = p.toppings :+ t)

    def removeAllToppings(p: Pizza): Pizza =
      p.copy(toppings = Seq.empty)

    def updateCrustSize(p: Pizza, cs: CrustSize): Pizza =
      p.copy(crustSize = cs)

    def updateCrustType(p: Pizza, ct: CrustType): Pizza =
      p.copy(crustType = ct)

  end PizzaService
  ```

#### Functional Objects

- In the book, Programming in Scala, the authors define the term, “Functional Objects” as “objects that do not have any mutable state”. This is also the case for types in scala.collection.immutable. For example, methods on List do not mutate the interal state, but instead create a copy of the List as a result.
- You can think of this approach as a “hybrid FP/OOP design” because you:
  - Model the data using immutable case classes.
  - Define the behaviors (methods) in the same type as the data.
  - Implement the behavior as pure functions: They don’t mutate any internal state; rather, they return a copy.
- This really is a hybrid approach: like in an OOP design, the methods are encapsulated in the class with the data, but as typical for a FP design, methods are implemented as pure functions that don’t mutate the data
- Using this approach, you can directly implement the functionality on pizzas in the case class:

  ```scala
  case class Pizza(
    crustSize: CrustSize,
    crustType: CrustType,
    toppings: Seq[Topping]
  ):

    // the operations on the data model
    def price: Double =
      pizzaPrice(this) // implementation from above

    def addTopping(t: Topping): Pizza =
      this.copy(toppings = this.toppings :+ t)

    def removeAllToppings: Pizza =
      this.copy(toppings = Seq.empty)

    def updateCrustSize(cs: CrustSize): Pizza =
      this.copy(crustSize = cs)

    def updateCrustType(ct: CrustType): Pizza =
      this.copy(crustType = ct)
  ```

- Notice that unlike the previous approaches, because these are methods on the Pizza class, they don’t take a Pizza reference as an input parameter. Instead, they have their own reference to the current pizza instance as this.
- Now you can use this new design like this:
  ```scala
  Pizza(Small, Thin, Seq(Cheese))
    .addTopping(Pepperoni)
    .updateCrustType(Thick)
    .price
  ```

#### Extension Methods

- Finally, we show an approach that lies between the first one (defining functions in the companion object) and the last one (defining functions as methods on the type itself).
- Extension methods let us create an API that is like the one of functional object, without having to define functions as methods on the type itself. This can have multiple advantages:
- Our data model is again very concise and does not mention any behavior.
  - We can equip types with additional methods retroactively without having to change the original definition.
  - Other than companion objects or direct methods on the types, extension methods can be defined externally in another file.
- Let us revisit our example once more.

  ```scala
  case class Pizza(
    crustSize: CrustSize,
    crustType: CrustType,
    toppings: Seq[Topping]
  )

  extension (p: Pizza)
    def price: Double =
      pizzaPrice(p) // implementation from above

    def addTopping(t: Topping): Pizza =
      p.copy(toppings = p.toppings :+ t)

    def removeAllToppings: Pizza =
      p.copy(toppings = Seq.empty)

    def updateCrustSize(cs: CrustSize): Pizza =
      p.copy(crustSize = cs)

    def updateCrustType(ct: CrustType): Pizza =
      p.copy(crustType = ct)
  ```

### Summary of this Approach

- Defining a data model in Scala/FP tends to be simple: Just model variants of the data with enumerations and compound data with case classes. Then, to model the behavior, define functions that operate on values of your data model. We have seen different ways to organize your functions:
  - You can put your methods in companion objects
  - You can use a modular programming style, separating interface and implementation
  - You can use a “functional objects” approach and store the methods on the defined data type
  - You can use extension methods to equip your data model with functionality
