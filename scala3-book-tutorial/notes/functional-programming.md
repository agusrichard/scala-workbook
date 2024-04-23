# Functional Programming

**Sources:**
- https://docs.scala-lang.org/scala3/book/fp-intro.html
- https://docs.scala-lang.org/scala3/book/fp-what-is-fp.html
- https://docs.scala-lang.org/scala3/book/fp-pure-functions.html
- https://docs.scala-lang.org/scala3/book/fp-functions-are-values.html

## Introduction
- Scala lets you write code in an object-oriented programming (OOP) style, a functional programming (FP) style, and also in a hybrid style—using both approaches in combination. As stated by Martin Odersky, the creator of Scala, the essence of Scala is a fusion of functional and object-oriented programming in a typed setting

## What is Functional Programming?
- Functional programming is a programming paradigm where programs are constructed by applying and composing functions. It is a declarative programming paradigm in which function definitions are trees of expressions that each return a value, rather than a sequence of imperative statements which change the state of the program.
- In functional programming, functions are treated as first-class citizens, meaning that they can be bound to names (including local identifiers), passed as arguments, and returned from other functions, just as any other data type can. This allows programs to be written in a declarative and composable style, where small functions are combined in a modular manner.
- It can also be helpful to know that experienced functional programmers have a strong desire to see their code as math, that combining pure functions together is like combining a series of algebraic equations.
- When you write functional code you feel like a mathematician, and once you understand the paradigm, you want to write pure functions that always return values—not exceptions or null values—so you can combine (compose) them together to create solutions. The feeling that you’re writing math-like equations (expressions) is the driving desire that leads you to use only pure functions and immutable values, because that’s what you use in algebra and other forms of math.
- Functional programming is a large topic, and there’s no simple way to condense the entire topic into one chapter, but hopefully the following sections will provide an overview of the main topics, and show some of the tools Scala provides for writing functional code.

## Immutable Values
- In pure functional programming, only immutable values are used. In Scala this means:
  - All variables are created as val fields
  - Only immutable collections classes are used, such as List, Vector, and the immutable Map and Set classes
- When it comes to using collections, one answer is that you don’t mutate an existing collection; instead, you apply a function to an existing collection to create a new collection. This is where higher-order functions like map and filter come in.
- For example, imagine that you have a list of names—a List[String]—that are all in lowercase, and you want to find all the names that begin with the letter "j", and then you want to capitalize those names. In FP you write this code:
  ```scala
  val a = List("jane", "jon", "mary", "joe")
  val b = a.filter(_.startsWith("j"))
          .map(_.capitalize)
  ```
- As shown, you don’t mutate the original list a. Instead, you apply filtering and transformation functions to a to create a new collection, and assign that result to the new immutable variable b.
- Similarly, in FP you don’t create classes with mutable var constructor parameters. Instead, you typically create case classes, whose constructor parameters are val by default:
  ```scala
  case class Person(firstName: String, lastName: String)

  val reginald = Person("Reginald", "Dwight")
  ```
- Then, when you need to make a change to the data, you use the copy method that comes with a case class to “update the data as you make a copy,” like this:
  ```scala
  val elton = reginald.copy(
    firstName = "Elton",   // update the first name
    lastName = "John"      // update the last name
  )
  ```

## Pure Functions
- Another feature that Scala offers to help you write functional code is the ability to write pure functions. A pure function can be defined like this:
  - A function f is pure if, given the same input x, it always returns the same output f(x)
  - The function’s output depends only on its input variables and its implementation
  - It only computes the output and does not modify the world around it
- This implies:
  - It doesn’t modify its input parameters
  - It doesn’t mutate any hidden state
  - It doesn’t have any “back doors”: It doesn’t read data from the outside world (including the console, web services, databases, files, etc.), or write data to the outside world
- As a result of this definition, any time you call a pure function with the same input value(s), you’ll always get the same result. For example, you can call a double function an infinite number of times with the input value 2, and you’ll always get the result 4.

### Examples of pure functions
- abs
- ceil
- max
- isEmpty
- length
- substring
- drop, filter, map
- Note: In Scala, functions and methods are almost completely interchangeable, so even though we use the common industry term “pure function,” this term can be used to describe both functions and methods. If you’re interested in how methods can be used like functions

### Examples of impure functions
- println – methods that interact with the console, files, databases, web services, sensors, etc., are all impure.
- currentTimeMillis – date and time related methods are all impure because their output depends on something other than their input parameters
- sys.error – exception throwing methods are impure because they do not simply return a result
- Impure functions often do one or more of these things:
  - Read from hidden state, i.e., they access variables and data not explicitly passed into the function as input parameters
  - Write to hidden state
  - Mutate the parameters they’re given, or mutate hidden variables, such as fields in their containing class
  - Perform some sort of I/O with the outside world
- In general, you should watch out for functions with a return type of Unit. Because those functions do not return anything, logically the only reason you ever call it is to achieve some side effect. In consequence, often the usage of those functions is impure.

### But impure functions are needed …
- Write the core of your application using pure functions, and then write an impure “wrapper” around that core to interact with the outside world. As someone once said, this is like putting a layer of impure icing on top of a pure cake.
- It’s important to note that there are ways to make impure interactions with the outside world feel more pure. For instance, you’ll hear about using an IO Monad to deal with input and output. These topics are beyond the scope of this document, so to keep things simple it can help to think that FP applications have a core of pure functions that are wrapped with other functions to interact with the outside world.

### Writing pure functions
- To write pure functions in Scala, just write them using Scala’s method syntax (though you can also use Scala’s function syntax, as well). For instance, here’s a pure function that doubles the input value it’s given:
  ```scala
  def double(i: Int): Int = i * 2

  def sum(xs: List[Int]): Int = xs match
    case Nil => 0
    case head :: tail => head + sum(tail)
  ```

### Key points
- A pure function is a function that depends only on its declared inputs and its implementation to produce its output. It only computes its output and does not depend on or modify the outside world.
- A second key point is that every real-world application interacts with the outside world. Therefore, a simplified way to think about functional programs is that they consist of a core of pure functions that are wrapped with other functions that interact with the outside world.

## Functions are Values
- While every programming language ever created probably lets you write pure functions, a second important Scala FP feature is that you can create functions as values, just like you create String and Int values.
- This feature has many benefits, the most common of which are (a) you can define methods to accept function parameters, and (b) you can pass functions as parameters into methods. You’ve seen this in multiple places in this book, whenever methods like map and filter are demonstrated:
  ```scala
  val nums = (1 to 10).toList

  val doubles = nums.map(_ * 2)           // double each value
  val lessThanFive = nums.filter(_ < 5)   // List(1,2,3,4)
  ```
- Anonymous functions are also known as lambdas.
- In addition to passing anonymous functions into filter and map, you can also supply them with methods:
  ```scala
  // two methods
  def double(i: Int): Int = i * 2
  def underFive(i: Int): Boolean = i < 5

  // pass those methods into filter and map
  val doubles = nums.filter(underFive).map(double)
  ```
- Technically, a function that takes another function as an input parameter is known as a Higher-Order Function. (If you like humor, as someone once wrote, that’s like saying that a class that takes an instance of another class as a constructor parameter is a Higher-Order Class.)

### Functions, anonymous functions, and methods
- Functions like these are called “anonymous” because they don’t have names. If you want to give one a name, just assign it to a variable:
  ```scala
  val double = (i: Int) => i * 2
  ```
- In most scenarios it doesn’t matter if double is a function or a method; Scala lets you treat them the same way. Behind the scenes, the Scala technology that lets you treat methods just like functions is known as Eta Expansion.
- This ability to seamlessly pass functions around as variables is a distinguishing feature of functional programming languages like Scala. And as you’ve seen in the map and filter examples throughout this book, the ability to pass functions into other functions helps you create code that is concise and still readable—expressive.
- If you’re not comfortable with the process of passing functions as parameters into other functions, here are a few more examples you can experiment with:
  ```scala
  List("bob", "joe").map(_.toUpperCase)   // List(BOB, JOE)
  List("bob", "joe").map(_.capitalize)    // List(Bob, Joe)
  List("plum", "banana").map(_.length)    // List(4, 6)

  val fruits = List("apple", "pear")
  fruits.map(_.toUpperCase)       // List(APPLE, PEAR)
  fruits.flatMap(_.toUpperCase)   // List(A, P, P, L, E, P, E, A, R)

  val nums = List(5, 1, 3, 11, 7)
  nums.map(_ * 2)         // List(10, 2, 6, 22, 14)
  nums.filter(_ > 3)      // List(5, 11, 7)
  nums.takeWhile(_ < 6)   // List(5, 1, 3)
  nums.sortWith(_ < _)    // List(1, 3, 5, 7, 11)
  nums.sortWith(_ > _)    // List(11, 7, 5, 3, 1)

  nums.takeWhile(_ < 6).sortWith(_ < _)   // List(1, 3, 5)
  ```


## Functional Error Handling
- Functional programming is like writing a series of algebraic equations, and because algebra doesn’t have null values or throw exceptions, you don’t use these features in FP. This brings up an interesting question: In the situations where you might normally use a null value or exception in OOP code, what do you do?
- Scala’s solution is to use constructs like the Option/Some/None classes. This lesson provides an introduction to using these techniques.
- Two notes before we jump in:
  - The Some and None classes are subclasses of Option.
  - Instead of repeatedly saying “Option/Some/None,” the following text generally just refers to “Option” or “the Option classes.”

### A first example
- Imagine that you want to write a method that makes it easy to convert strings to integer values, and you want an elegant way to handle the exception that’s thrown when your method gets a string like "Hello" instead of "1". A first guess at such a method might look like this:
  ```scala
  def makeInt(s: String): Int =
    try
      Integer.parseInt(s.trim)
    catch
      case e: Exception => 0
  ```
- If the conversion works, this method returns the correct Int value, but if it fails, the method returns 0. This might be okay for some purposes, but it’s not really accurate. For instance, the method might have received "0", but it may have also received "foo", "bar", or an infinite number of other strings that will throw an exception. This is a real problem: How do you know when the method really received a "0", or when it received something else? The answer is that with this approach, there’s no way to know.

### Using Option/Some/None
- A common solution to this problem in Scala is to use a trio of classes known as Option, Some, and None. The Some and None classes are subclasses of Option, so the solution works like this:
  - You declare that makeInt returns an Option type
  - If makeInt receives a string it can convert to an Int, the answer is wrapped inside a Some
  - If makeInt receives a string it can’t convert, it returns a None
- Here’s the revised version of makeInt:
  ```scala
  def makeInt(s: String): Option[Int] =
    try
      Some(Integer.parseInt(s.trim))
    catch
      case e: Exception => None
  ```
- This code can be read as, “When the given string converts to an integer, return the Int wrapped inside a Some, such as Some(1). When the string can’t be converted to an integer, an exception is thrown and caught, and the method returns a None value.”
- These examples show how makeInt works:
  ```scala
  val a = makeInt("1")     // Some(1)
  val b = makeInt("one")   // None
  ```
- As shown, the string "1" results in a Some(1), and the string "one" results in a None. This is the essence of the Option approach to error handling. As shown, this technique is used so methods can return values instead of exceptions. In other situations, Option values are also used to replace null values.
- Two notes:
  - You’ll find this approach used throughout Scala library classes, and in third-party Scala libraries.
  - A key point of this example is that functional methods don’t throw exceptions; instead they return values like Option.

### Being a consumer of makeInt: Using a match expression
- One possible solution is to use a match expression:
  ```scala
  makeInt(x) match
    case Some(i) => println(i)
    case None => println("That didn’t work.")
  ```
- In this example, if x can be converted to an Int, the expression on the right-hand side of the first case clause is evaluated; if x can’t be converted to an Int, the expression on the right-hand side of the second case clause is evaluated.

### Being a consumer of makeInt: Using a for expression
- Another common solution is to use a for expression—i.e., the for/yield combination that was shown earlier in this book. For instance, imagine that you want to convert three strings to integer values, and then add them together. This is how you do that with a for expression and makeInt:
  ```scala
  val y = for
    a <- makeInt(stringA)
    b <- makeInt(stringB)
    c <- makeInt(stringC)
  yield
    a + b + c
  ```
- After that expression runs, y will be one of two things:
  - If all three strings convert to Int values, y will be a Some[Int], i.e., an integer wrapped inside a Some
  - If any of the three strings can’t be converted to an Int, y will be a None

### Thinking of Option as a container
- Mental models can often help us understand new situations, so if you’re not familiar with the Option classes, one way to think about them is as a container:
  - Some is a container with one item in it
  - None is a container, but it has nothing in it

### Using Option to replace null
- Getting back to null values, a place where a null value can silently creep into your code is with a class like this:
  ```scala
  class Address(
    var street1: String,
    var street2: String,
    var city: String,
    var state: String,
    var zip: String
  )
  ```
- While every address on Earth has a street1 value, the street2 value is optional. As a result, the street2 field can be assigned a null value:
  ```scala
  val santa = Address(
    "1 Main Street",
    null,               // <-- D’oh! A null value!
    "North Pole",
    "Alaska",
    "99705"
  )
  ```
- Historically, developers have used blank strings and null values in this situation, both of which are hacks to work around the root problem: street2 is an optional field. In Scala—and other modern languages—the correct solution is to declare up front that street2 is optional:
  ```scala
  class Address(
    var street1: String,
    var street2: Option[String],   // an optional value
    var city: String, 
    var state: String, 
    var zip: String
  )
  ```
- Now developers can write more accurate code like this:
  ```scala
  val santa = Address(
    "1 Main Street",
    None,           // 'street2' has no value
    "North Pole",
    "Alaska",
    "99705"
  )

  // or
  val santa = Address(
    "123 Main Street",
    Some("Apt. 2B"),
    "Talkeetna",
    "Alaska",
    "99676"
  )
  ```

### Option isn’t the only solution
- For example, a trio of classes known as Try/Success/Failure work in the same manner, but (a) you primarily use these classes when your code can throw exceptions, and (b) you want to use the Failure class because it gives you access to the exception message. For example, these Try classes are commonly used when writing methods that interact with files, databases, and internet services, as those functions can easily throw exceptions.

### A quick review
- Functional programmers don’t use null values
- A main replacement for null values is to use the Option classes
- Functional methods don’t throw exceptions; instead they return values like Option, Try, or Either
- Common ways to work with Option values are match and for expressions
- Options can be thought of as containers of one item (Some) and no items (None)
- Options can also be used for optional constructor or method parameters