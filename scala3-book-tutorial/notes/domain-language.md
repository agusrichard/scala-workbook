# Domain Language

**Source:**

- https://docs.scala-lang.org/scala3/book/domain-modeling-intro.html
- https://docs.scala-lang.org/scala3/book/domain-modeling-tools.html

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
