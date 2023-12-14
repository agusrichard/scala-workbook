# WHY SCALA 3?

Source: https://docs.scala-lang.org/scala3/book/why-scala-3.html

## 1) FP/OOP fusion

- Snippets:

  ```scala
  val x = List(1, 2, 3)

  val xs = List(1, 2, 3, 4, 5)

  xs.map(_ + 1)         // List(2, 3, 4, 5, 6)
  xs.filter(_ < 3)      // List(1, 2)
  xs.find(_ > 3)        // Some(4)
  xs.takeWhile(_ < 3)   // List(1, 2)
  ```

## 2) A dynamic feel

- Snippets:

  ```scala
  val a = 1
  val b = "Hello, world"
  val c = List(1,2,3,4,5)
  val stuff = ("fish", 42, 1_234.5)

  list.filter(_ < 4)
  list.map(_ * 2)
  list.filter(_ < 4)
      .map(_ * 2)

  def add(a: Int, b: Int) = a + b

  // union type parameter
  def help(id: Username | Password) =
    val user = id match
      case Username(name) => lookupName(name)
      case Password(hash) => lookupPassword(hash)
    // more code here ...

  // union type value
  val b: Password | Username = if (true) name else password
  ```

## 3) Concise syntax

- Scala is a low ceremony, “concise but still readable” language.
- Snippets:

  ```scala
  val a = 1
  val b = "Hello, world"
  val c = List(1,2,3)

  trait Tail:
    def wagTail(): Unit
    def stopTail(): Unit

  enum Topping:
    case Cheese, Pepperoni, Sausage, Mushrooms, Onions

  class Dog extends Animal, Tail, Legs, RubberyNose

  case class Person(
    firstName: String,
    lastName: String,
    age: Int
  )

  list.filter(_ < 4)
  list.map(_ * 2)
  ```

## 4) Implicits, simplified

## 5) Seamless Java integration

## 6) Client & server

## 7) Standard library methods

- Snippets:

  ```scala
  List.range(1, 3)                          // List(1, 2)
  List.range(start = 1, end = 6, step = 2)  // List(1, 3, 5)
  List.fill(3)("foo")                       // List(foo, foo, foo)
  List.tabulate(3)(n => n * n)              // List(0, 1, 4)
  List.tabulate(4)(n => n * n)              // List(0, 1, 4, 9)

  val a = List(10, 20, 30, 40, 10)          // List(10, 20, 30, 40, 10)
  a.distinct                                // List(10, 20, 30, 40)
  a.drop(2)                                 // List(30, 40, 10)
  a.dropRight(2)                            // List(10, 20, 30)
  a.dropWhile(_ < 25)                       // List(30, 40, 10)
  a.filter(_ < 25)                          // List(10, 20, 10)
  a.filter(_ > 100)                         // List()
  a.find(_ > 20)                            // Some(30)
  a.head                                    // 10
  a.headOption                              // Some(10)
  a.init                                    // List(10, 20, 30, 40)
  a.intersect(List(19,20,21))               // List(20)
  a.last                                    // 10
  a.lastOption                              // Some(10)
  a.map(_ * 2)                              // List(20, 40, 60, 80, 20)
  a.slice(2, 4)                             // List(30, 40)
  a.tail                                    // List(20, 30, 40, 10)
  a.take(3)                                 // List(10, 20, 30)
  a.takeRight(2)                            // List(40, 10)
  a.takeWhile(_ < 30)                       // List(10, 20)
  a.filter(_ < 30).map(_ * 10)              // List(100, 200, 100)

  val fruits = List("apple", "pear")
  fruits.map(_.toUpperCase)                 // List(APPLE, PEAR)
  fruits.flatMap(_.toUpperCase)             // List(A, P, P, L, E, P, E, A, R)

  val nums = List(10, 5, 8, 1, 7)
  nums.sorted                               // List(1, 5, 7, 8, 10)
  nums.sortWith(_ < _)                      // List(1, 5, 7, 8, 10)
  nums.sortWith(_ > _)                      // List(10, 8, 7, 5, 1)
  ```
