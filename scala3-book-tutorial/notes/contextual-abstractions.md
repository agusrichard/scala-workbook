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