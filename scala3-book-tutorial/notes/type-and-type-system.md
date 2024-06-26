# Type and Type System

**Sources**
- https://docs.scala-lang.org/scala3/book/types-introduction.html
- https://docs.scala-lang.org/scala3/book/types-inferred.html

## Introduction
- Scala is a unique language in that it’s statically typed, but often feels flexible and dynamic. For instance, thanks to type inference you can write code like this without explicitly specifying the variable types:
  ```scala
  val a = 1
  val b = 2.0
  val c = "Hi!"
  ```
- And thanks to new features, like union types in Scala 3, you can also write code like the following that expresses very concisely which values are expected as arguments and which types are returned:
  ```scala
  def isTruthy(a: Boolean | Int | String): Boolean = ???
  def dogCatOrWhatever(): Dog | Plant | Car | Sun = ???
  ```

## Inferred Types
- As with other statically typed programming languages, in Scala you can declare a type when creating a new variable:
  ```scala
  val x: Int = 1
  val y: Double = 1
  ```
- However, in Scala you generally don’t have to declare the type when defining value binders:
  ```scala
  val a = 1
  val b = List(1, 2, 3)
  val m = Map(1 -> "one", 2 -> "two")
  ```
- When you do this, Scala infers the types.
- Indeed, most variables are defined this way, and Scala’s ability to automatically infer types is one feature that makes it feel like a dynamically typed language.

## Generics
- Generic classes (or traits) take a type as a parameter within square brackets [...]. The Scala convention is to use a single letter (like A) to name those type parameters. The type can then be used inside the class as needed for method instance parameters, or on return types:
  ```scala
  // here we declare the type parameter A
  //          v
  class Stack[A]:
    private var elements: List[A] = Nil
    //                         ^
    //  Here we refer to the type parameter
    //          v
    def push(x: A): Unit =
      elements = elements.prepended(x)
    def peek: A = elements.head
    def pop(): A =
      val currentTop = peek
      elements = elements.tail
      currentTop
  ```
- This implementation of a Stack class takes any type as a parameter. The beauty of generics is that you can now create a Stack[Int], Stack[String], and so on, allowing you to reuse your implementation of a Stack for arbitrary element types. This is how you create and use a Stack[Int]:
  ```scala
  val stack = Stack[Int]
  stack.push(1)
  stack.push(2)
  println(stack.pop())  // prints 2
  println(stack.pop())  // prints 1
  ```

## Intersection Types
- Used on types, the & operator creates a so called intersection type. The type A & B represents values that are both of the type A and of the type B at the same time. For instance, the following example uses the intersection type Resettable & Growable[String]:
  ```scala
  trait Resettable:
    def reset(): Unit

  trait Growable[A]:
    def add(a: A): Unit

  def f(x: Resettable & Growable[String]): Unit =
    x.reset()
    x.add("first")
  ```
- In the method f in this example, the parameter x is required to be both a Resettable and a Growable[String].
- The members of an intersection type A & B are all the members of A and all the members of B. Therefore, as shown, Resettable & Growable[String] has member methods reset and add.
- Intersection types can be useful to describe requirements structurally. That is, in our example f, we directly express that we are happy with any value for x as long as it’s a subtype of both Resettable and Growable. We did not have to create a nominal helper trait like the following:
  ```scala
  trait Both[A] extends Resettable, Growable[A]
  def f(x: Both[String]): Unit
  ```
- There is an important difference between the two alternatives of defining f: While both allow f to be called with instances of Both, only the former allows passing instances that are subtypes of Resettable and Growable[String], but not of Both[String].
- Note that & is commutative: A & B is the same type as B & A.


## Union Types
- Used on types, the | operator creates a so-called union type. The type A | B represents values that are either of the type A or of the type B.
- In the following example, the help method accepts a parameter named id of the union type Username | Password, that can be either a Username or a Password:
  ```scala
  case class Username(name: String)
  case class Password(hash: Hash)

  def help(id: Username | Password) =
    val user = id match
      case Username(name) => lookupName(name)
      case Password(hash) => lookupPassword(hash)
    // more code here ...
  ```
- This code is a flexible and type-safe solution. If you attempt to pass in a type other than a Username or Password, the compiler flags it as an error:
  ```
  help("hi")   // error: Found: ("hi" : String)
              //        Required: Username | Password
  ```
- As shown, union types can be used to represent alternatives of several different types, without requiring those types to be part of a custom-crafted class hierarchy, or requiring explicit wrapping.
- Without union types, it would require pre-planning of the class hierarchy, like the following example illustrates:
  ```scala
  trait UsernameOrPassword
  case class Username(name: String) extends UsernameOrPassword
  case class Password(hash: Hash) extends UsernameOrPassword
  def help(id: UsernameOrPassword) = ...
  ```
- Another alternative is to define a separate enumeration type like:
  ```scala
  enum UsernameOrPassword:
    case IsUsername(u: Username)
    case IsPassword(p: Password)
  ```
- The enumeration UsernameOrPassword represents a tagged union of Username and Password. However, this way of modeling the union requires explicit wrapping and unwrapping and, for instance, Username is not a subtype of UsernameOrPassword.
- The compiler assigns a union type to an expression only if such a type is explicitly given. For instance, given these values:
  ```scala
  val name = Username("Eve")     // name: Username = Username(Eve)
  val password = Password(123)   // password: Password = Password(123)
  ```
- This REPL example shows how a union type can be used when binding a variable to the result of an if/else expression:
  ```scala
  scala> val a = if true then name else password
  val a: Object = Username(Eve)

  scala> val b: Password | Username = if true then name else password
  val b: Password | Username = Username(Eve)
  ```
- The type of a is Object, which is a supertype of Username and Password, but not the least supertype, Password | Username. If you want the least supertype you have to give it explicitly, as is done for b.
- Union types are duals of intersection types. And like & with intersection types, | is also commutative: A | B is the same type as B | A.


## Algebraic Data Types

### Enumerations
- An enumeration is used to define a type consisting of a set of named values:
  ```scala
  enum Color:
    case Red, Green, Blue

  // The above is the shorthand of this
  enum Color:
  case Red   extends Color
  case Green extends Color
  case Blue  extends Color
  ```
- Enums can be parameterized:
  ```scala
  enum Color(val rgb: Int):
    case Red   extends Color(0xFF0000)
    case Green extends Color(0x00FF00)
    case Blue  extends Color(0x0000FF)
  ```
- Enums can also have custom definitions:
  ```scala
  enum Planet(mass: Double, radius: Double):

    private final val G = 6.67300E-11
    def surfaceGravity = G * mass / (radius * radius)
    def surfaceWeight(otherMass: Double) =  otherMass * surfaceGravity

    case Mercury extends Planet(3.303e+23, 2.4397e6)
    case Venus   extends Planet(4.869e+24, 6.0518e6)
    case Earth   extends Planet(5.976e+24, 6.37814e6)
    // 5 or 6 more planets ...
  ```
- Like classes and case classes, you can also define a companion object for an enum:
  ```scala
  object Planet:
    def main(args: Array[String]) =
      val earthWeight = args(0).toDouble
      val mass = earthWeight / Earth.surfaceGravity
      for (p <- values)
        println(s"Your weight on $p is ${p.surfaceWeight(mass)}")
  ```

### Algebraic Datatypes (ADTs)
- The enum concept is general enough to also support algebraic data types (ADTs) and their generalized version (GADTs). Here’s an example that shows how an Option type can be represented as an ADT:
  ```scala
  enum Option[+T]:
    case Some(x: T)
    case None
  ```
- This example creates an Option enum with a covariant type parameter T consisting of two cases, Some and None. Some is parameterized with a value parameter x; this is a shorthand for writing a case class that extends Option. Since None is not parameterized, it’s treated as a normal enum value.
- The extends clauses that were omitted in the previous example can also be given explicitly:
  ```scala
  enum Option[+T]:
    case Some(x: T) extends Option[T]
    case None       extends Option[Nothing]
  ```
- As with normal enum values, the cases of an enum are defined in the enums companion object, so they’re referred to as Option.Some and Option.None (unless the definitions are “pulled out” with an import):
  ```scala
  scala> Option.Some("hello")
  val res1: t2.Option[String] = Some(hello)

  scala> Option.None
  val res2: t2.Option[Nothing] = None
  ```
- As with other enumeration uses, ADTs can define additional methods. For instance, here’s Option again, with an isDefined method and an Option(...) constructor in its companion object:
  ```scala
  enum Option[+T]:
    case Some(x: T)
    case None

    def isDefined: Boolean = this match
      case None => false
      case Some(_) => true

  object Option:
    def apply[T >: Null](x: T): Option[T] =
      if (x == null) None else Some(x)
  ```
- Enumerations and ADTs share the same syntactic construct, so they can be seen simply as two ends of a spectrum, and it’s perfectly possible to construct hybrids. For instance, the code below gives an implementation of Color, either with three enum values or with a parameterized case that takes an RGB value:
  ```scala
  enum Color(val rgb: Int):
    case Red   extends Color(0xFF0000)
    case Green extends Color(0x00FF00)
    case Blue  extends Color(0x0000FF)
    case Mix(mix: Int) extends Color(mix)
  ```
- So far all the enumerations that we defined consisted of different variants of values or case classes. Enumerations can also be recursive, as illustrated in the below example of encoding natural numbers:
  ```scala
  enum Nat:
    case Zero
    case Succ(n: Nat)
  ```
- For example the value Succ(Succ(Zero)) represents the number 2 in an unary encoding. Lists can be defined in a very similar way:
  ```scala
  enum List[+A]:
    case Nil
    case Cons(head: A, tail: List[A])
  ```

### Generalized Algebraic Datatypes (GADTs)
- The above notation for enumerations is very concise and serves as the perfect starting point for modeling your data types. Since we can always be more explicit, it is also possible to express types that are much more powerful: generalized algebraic datatypes (GADTs).
- Here is an example of a GADT where the type parameter (T) specifies the contents stored in the box:
  ```scala
  enum Box[T](contents: T):
    case IntBox(n: Int) extends Box[Int](n)
    case BoolBox(b: Boolean) extends Box[Boolean](b)
  ```
- Pattern matching on the particular constructor (IntBox or BoolBox) recovers the type information:
  ```scala
  def extract[T](b: Box[T]): T = b match
    case IntBox(n)  => n + 1
    case BoolBox(b) => !b
  ```

### Desugaring Enumerations
- Conceptually, enums can be thought of as defining a sealed class together with its companion object. Let’s look at the desugaring of our Color enum above:
  ```scala
  sealed abstract class Color(val rgb: Int) extends scala.reflect.Enum
  object Color:
    case object Red extends Color(0xFF0000) { def ordinal = 0 }
    case object Green extends Color(0x00FF00) { def ordinal = 1 }
    case object Blue extends Color(0x0000FF) { def ordinal = 2 }
    case class Mix(mix: Int) extends Color(mix) { def ordinal = 3 }

    def fromOrdinal(ordinal: Int): Color = ordinal match
      case 0 => Red
      case 1 => Green
      case 2 => Blue
      case _ => throw new NoSuchElementException(ordinal.toString)
  ```
- While enums could be manually encoded using other constructs, using enumerations is more concise and also comes with a few additional utilities (such as the fromOrdinal method).

## Variance
- Type parameter variance controls the subtyping of parameterized types (like classes or traits).
- To explain variance, let us assume the following type definitions:
  ```scala
  trait Item { def productNumber: String }
  trait Buyable extends Item { def price: Int }
  trait Book extends Buyable { def isbn: String }
  ```
- Let us also assume the following parameterized types:
  ```scala
  // an example of an invariant type
  trait Pipeline[T]:
    def process(t: T): T

  // an example of a covariant type
  trait Producer[+T]:
    def make: T

  // an example of a contravariant type
  trait Consumer[-T]:
    def take(t: T): Unit
  ```

### Invariant Types
- By default, types like Pipeline are invariant in their type argument (T in this case). This means that types like Pipeline[Item], Pipeline[Buyable], and Pipeline[Book] are in no subtyping relationship to each other.
- And rightfully so! Assume the following method that consumes two values of type Pipeline[Buyable], and passes its argument b to one of them, based on the price:
  ```scala
  def oneOf(
    p1: Pipeline[Buyable],
    p2: Pipeline[Buyable],
    b: Buyable
  ): Buyable =
    val b1 = p1.process(b)
    val b2 = p2.process(b)
    if b1.price < b2.price then b1 else b2
  ```
- Now, recall that we have the following subtyping relationship between our types:
  ```scala
  Book <: Buyable <: Item
  ```
- We cannot pass a Pipeline[Book] to the method oneOf because in its implementation, we call p1 and p2 with a value of type Buyable. A Pipeline[Book] expects a Book, which can potentially cause a runtime error. We cannot pass a Pipeline[Item] because calling process on it only promises to return an Item; however, we are supposed to return a Buyable.
- Why Invariant? In fact, type Pipeline needs to be invariant since it uses its type parameter T both as an argument and as a return type. For the same reason, some types in the Scala collection library—like Array or Set—are also invariant.

### Covariant Types
- In contrast to Pipeline, which is invariant, the type Producer is marked as covariant by prefixing the type parameter with a +. This is valid, since the type parameter is only used in a return position.
- Marking it as covariant means that we can pass (or return) a Producer[Book] where a Producer[Buyable] is expected. And in fact, this is sound. The type of Producer[Buyable].make only promises to return a Buyable. As a caller of make, we will be happy to also accept a Book, which is a subtype of Buyable—that is, it is at least a Buyable.
- This is illustrated by the following example, where the function makeTwo expects a Producer[Buyable]:
  ```scala
  def makeTwo(p: Producer[Buyable]): Int =
    p.make.price + p.make.price
  ```
- It is perfectly fine to pass a producer for books:
  ```scala
  val bookProducer: Producer[Book] = ???
  makeTwo(bookProducer)
  ```
- You will encounter covariant types a lot when dealing with immutable containers, like those that can be found in the standard library (such as List, Seq, Vector, etc.). For example, List and Vector are approximately defined as:
  ```scala
  class List[+A] ...
  class Vector[+A] ...
  ```
- This way, you can use a List[Book] where a List[Buyable] is expected. This also intuitively makes sense: If you are expecting a collection of things that can be bought, it should be fine to give you a collection of books. They have an additional ISBN method in our example, but you are free to ignore these additional capabilities.

### Contravariant Types
- In contrast to the type Producer, which is marked as covariant, the type Consumer is marked as contravariant by prefixing the type parameter with a -. This is valid, since the type parameter is only used in an argument position.
- Marking it as contravariant means that we can pass (or return) a Consumer[Item] where a Consumer[Buyable] is expected. That is, we have the subtyping relationship Consumer[Item] <: Consumer[Buyable]. Remember, for type Producer, it was the other way around, and we had Producer[Buyable] <: Producer[Item].
- And in fact, this is sound. The method Consumer[Item].take accepts an Item. As a caller of take, we can also supply a Buyable, which will be happily accepted by the Consumer[Item] since Buyable is a subtype of Item—that is, it is at least an Item.
- Contravariant types are much less common than covariant types. As in our example, you can think of them as “consumers.” The most important type that you might come across that is marked contravariant is the one of functions:
  ```scala
  trait Function[-A, +B]:
    def apply(a: A): B
  ```
- Its argument type A is marked as contravariant A—it consumes values of type A. In contrast, its result type B is marked as covariant—it produces values of type B.
- Here are some examples that illustrate the subtyping relationships induced by variance annotations on functions:
  ```scala
  val f: Function[Buyable, Buyable] = b => b

  // OK to return a Buyable where a Item is expected
  val g: Function[Buyable, Item] = f

  // OK to provide a Book where a Buyable is expected
  val h: Function[Book, Buyable] = f
  ```

## Opaque Types

### Abstraction Overhead
- Let us assume we want to define a module that offers arithmetic on numbers, which are represented by their logarithm. This can be useful to improve precision when the numerical values involved tend to be very large, or close to zero. Since it is important to distinguish “regular” double values from numbers stored as their logarithm, we introduce a class Logarithm:
  ```scala
  class Logarithm(protected val underlying: Double):
    def toDouble: Double = math.exp(underlying)
    def + (that: Logarithm): Logarithm =
      // here we use the apply method on the companion
      Logarithm(this.toDouble + that.toDouble)
    def * (that: Logarithm): Logarithm =
      new Logarithm(this.underlying + that.underlying)

  object Logarithm:
    def apply(d: Double): Logarithm = new Logarithm(math.log(d))
  ```
- The apply method on the companion object lets us create values of type Logarithm which we can use as follows:
  ```scala
  val l2 = Logarithm(2.0)
  val l3 = Logarithm(3.0)
  println((l2 * l3).toDouble) // prints 6.0
  println((l2 + l3).toDouble) // prints 4.999...
  ```

### Module Abstractions
- Let us consider another approach to implement the same library. This time instead of defining Logarithm as a class, we define it using a type alias. First, we define an abstract interface of our module:
  ```scala
  trait Logarithms:

    type Logarithm

    // operations on Logarithm
    def add(x: Logarithm, y: Logarithm): Logarithm
    def mul(x: Logarithm, y: Logarithm): Logarithm

    // functions to convert between Double and Logarithm
    def make(d: Double): Logarithm
    def extract(x: Logarithm): Double

    // extension methods to use `add` and `mul` as "methods" on Logarithm
    extension (x: Logarithm)
      def toDouble: Double = extract(x)
      def + (y: Logarithm): Logarithm = add(x, y)
      def * (y: Logarithm): Logarithm = mul(x, y)
  ```
- Now, let us implement this abstract interface by saying type Logarithm is equal to Double:
  ```scala
  object LogarithmsImpl extends Logarithms:

    type Logarithm = Double

    // operations on Logarithm
    def add(x: Logarithm, y: Logarithm): Logarithm = make(x.toDouble + y.toDouble)
    def mul(x: Logarithm, y: Logarithm): Logarithm = x + y

    // functions to convert between Double and Logarithm
    def make(d: Double): Logarithm = math.log(d)
    def extract(x: Logarithm): Double = math.exp(x)
  ```
- Within the implementation of LogarithmsImpl, the equation Logarithm = Double allows us to implement the various methods.
- However, this abstraction is slightly leaky. We have to make sure to only ever program against the abstract interface Logarithms and never directly use LogarithmsImpl. Directly using LogarithmsImpl would make the equality Logarithm = Double visible for the user, who might accidentally use a Double where a logarithmic double is expected. For example:
  ```scala
  import LogarithmsImpl.*
  val l: Logarithm = make(1.0)
  val d: Double = l // type checks AND leaks the equality!
  ```
- Having to separate the module into an abstract interface and implementation can be useful, but is also a lot of effort, just to hide the implementation detail of Logarithm. Programming against the abstract module Logarithms can be very tedious and often requires the use of advanced features like path-dependent types, as in the following example:
  ```scala
  def someComputation(L: Logarithms)(init: L.Logarithm): L.Logarithm = ...
  ```
- Type abstractions, such as type Logarithm erase to their bound (which is Any in our case). That is, although we do not need to manually wrap and unwrap the Double value, there will be still some boxing overhead related to boxing the primitive type Double.


### Opaque Types
- Instead of manually splitting our Logarithms component into an abstract part and into a concrete implementation, we can simply use opaque types in Scala 3 to achieve a similar effect:
  ```scala
  object Logarithms:
  //vvvvvv this is the important difference!
    opaque type Logarithm = Double

    object Logarithm:
      def apply(d: Double): Logarithm = math.log(d)

    extension (x: Logarithm)
      def toDouble: Double = math.exp(x)
      def + (y: Logarithm): Logarithm = Logarithm(math.exp(x) + math.exp(y))
      def * (y: Logarithm): Logarithm = x + y
  ```
- The fact that Logarithm is the same as Double is only known in the scope where Logarithm is defined, which in the above example corresponds to the object Logarithms. The type equality Logarithm = Double can be used to implement the methods (like * and toDouble).
- However, outside of the module the type Logarithm is completely encapsulated, or “opaque.” To users of Logarithm it is not possible to discover that Logarithm is actually implemented as a Double:
  ```scala
  import Logarithms.*
  val log2 = Logarithm(2.0)
  val log3 = Logarithm(3.0)
  println((log2 * log3).toDouble) // prints 6.0
  println((log2 + log3).toDouble) // prints 4.999...

  val d: Double = log2 // ERROR: Found Logarithm required Double
  ```
- Even though we abstracted over Logarithm, the abstraction comes for free: Since there is only one implementation, at runtime there will be no boxing overhead for primitive types like Double.

## Structural Types
- Here’s an example of a structural type Person:
  ```scala
  class Record(elems: (String, Any)*) extends Selectable:
    private val fields = elems.toMap
    def selectDynamic(name: String): Any = fields(name)

  type Person = Record {
    val name: String
    val age: Int
  }
  ```
- The Person type adds a refinement to its parent type Record that defines name and age fields. We say the refinement is structural since name and age are not defined in the parent type. But they exist nevertheless as members of class Person. For instance, the following program would print "Emma is 42 years old.":
  ```scala
  val person = Record(
    "name" -> "Emma",
    "age" -> 42
  ).asInstanceOf[Person]

  println(s"${person.name} is ${person.age} years old.")
  ```
- The parent type Record in this example is a generic class that can represent arbitrary records in its elems argument. This argument is a sequence of pairs of labels of type String and values of type Any. When you create a Person as a Record you have to assert with a typecast that the record defines the right fields of the right types. Record itself is too weakly typed, so the compiler cannot know this without help from the user. In practice, the connection between a structural type and its underlying generic representation would most likely be done by a database layer, and therefore would not be a concern of the end user.
- Record extends the marker trait scala.Selectable and defines a method selectDynamic, which maps a field name to its value. Selecting a structural type member is done by calling this method. The person.name and person.age selections are translated by the Scala compiler to:
  ```scala
  person.selectDynamic("name").asInstanceOf[String]
  person.selectDynamic("age").asInstanceOf[Int]
  ```
- To reinforce what you just saw, here’s another structural type named Book that represents a book that you might read from a database:
  ```scala
  type Book = Record {
    val title: String
    val author: String
    val year: Int
    val rating: Double
  }
  ```
- As with Person, this is how you create a Book instance:
  ```scala
  val book = Record(
    "title" -> "The Catcher in the Rye",
    "author" -> "J. D. Salinger",
    "year" -> 1951,
    "rating" -> 4.5
  ).asInstanceOf[Book]
  ```
- Besides selectDynamic, a Selectable class sometimes also defines a method applyDynamic. This can then be used to translate function calls of structural members. So, if a is an instance of Selectable, a structural call like a.f(b, c) translates to:
  ```scala
  a.applyDynamic("f")(b, c)
  ```

## Dependent Types
- A dependent function type describes function types, where the result type may depend on the function’s parameter values. The concept of dependent types, and of dependent function types is more advanced and you would typically only come across it when designing your own libraries or using advanced libraries.
- Let’s consider the following example of a heterogenous database that can store values of different types. The key contains the information about what’s the type of the corresponding value:
  ```scala
  trait Key { type Value }

  trait DB {
    def get(k: Key): Option[k.Value] // a dependent method
  }
  ```
- Given a key, the method get lets us access the map and potentially returns the stored value of type k.Value. We can read this path-dependent type as: “depending on the concrete type of the argument k, we return a matching value”.
- For example, we could have the following keys:
  ```scala
  object Name extends Key { type Value = String }
  object Age extends Key { type Value = Int }
  ```
- The following calls to method get would now type check:
  ```scala
  val db: DB = ...
  val res1: Option[String] = db.get(Name)
  val res2: Option[Int] = db.get(Age)
  ```
- Calling the method db.get(Name) returns a value of type Option[String], while calling db.get(Age) returns a value of type Option[Int]. The return type depends on the concrete type of the argument passed to get—hence the name dependent type.
- Let us assume we want to define a module that abstracts over the internal represention of numbers. This can be useful, for instance, to implement libraries for automatic derivation. We start by defining our module for numbers:
  ```scala
  trait Nums:
    // the type of numbers is left abstract
    type Num

    // some operations on numbers
    def lit(d: Double): Num
    def add(l: Num, r: Num): Num
    def mul(l: Num, r: Num): Num
  ```
- A program that uses our number abstraction now has the following type:
  ```scala
  type Prog = (n: Nums) => n.Num => n.Num

  val ex: Prog = nums => x => nums.add(nums.lit(0.8), x)
  ```