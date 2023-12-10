# SCALA FEATURES

Source: https://docs.scala-lang.org/scala3/book/scala-features.html

### High-level features

- Scala is considered a high-level language in at least two ways.
- Second, with the use of lambdas and higher-order functions, you write your code at a very high level. As the functional programming saying goes, in Scala you write what you want, not how to achieve it. That is, we don’t write imperative code like this:
- Imperative way:

  ```scala
  import scala.collection.mutable.ListBuffer

  def double(ints: List[Int]): List[Int] =
    val buffer = new ListBuffer[Int]()
    for i <- ints do
      buffer += i * 2
    buffer.toList

  val oldNumbers = List(1, 2, 3)
  val newNumbers = double(oldNumbers)
  ```

- Descriptive:
  ```scala
  val newNumbers = oldNumbers.map(_ * 2)
  ```
- Concise syntax

  ```scala
  val nums = List(1,2,3)
  val p = Person("Martin", "Odersky")

  nums.map(i => i * 2)   // long form
  nums.map(_ * 2)        // short form

  nums.filter(i => i > 1)
  nums.filter(_ > 1)

  trait Animal:
    def speak(): Unit

  trait HasTail:
    def wagTail(): Unit

  class Dog extends Animal, HasTail:
    def speak(): Unit = println("Woof")
    def wagTail(): Unit = println("⎞⎜⎛  ⎞⎜⎛")
  ```
