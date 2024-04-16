# Scala Collections

**Sources:**
- https://docs.scala-lang.org/scala3/book/collections-intro.html
- https://docs.scala-lang.org/scala3/book/collections-classes.html

## Collection Types

### Three main categories of collections
- Sequences are a sequential collection of elements and may be indexed (like an array) or linear (like a linked list)
- Maps contain a collection of key/value pairs, like a Java Map, Python dictionary, or Ruby Hash
- Sets are an unordered collection of unique elements

#### Collections hierarchy
- This first figure shows the collections types in package scala.collection. These are all high-level abstract classes or traits, which generally have immutable and mutable implementations.
  ![](https://docs.scala-lang.org/resources/images/tour/collections-diagram-213.svg)
- This figure shows all collections in package scala.collection.immutable:
  ![](https://docs.scala-lang.org/resources/images/tour/collections-immutable-diagram-213.svg)
- And this figure shows all collections in package scala.collection.mutable:
  ![](https://docs.scala-lang.org/resources/images/tour/collections-mutable-diagram-213.svg)

### Common collections
- In Scala, a buffer—such as ArrayBuffer and ListBuffer—is a sequence that can grow and shrink.
- In the sections that follow, whenever the word immutable is used, it’s safe to assume that the type is intended for use in a functional programming (FP) style. With these types you don’t modify the collection; you apply functional methods to the collection to create a new result.

### Choosing a sequence
- When choosing a sequence—a sequential collection of elements—you have two main decisions:
  - Should the sequence be indexed (like an array), allowing rapid access to any element, or should it be implemented as a linear linked list?
  - Do you want a mutable or immutable collection?
- For example, if you need an immutable, indexed collection, in general you should use a Vector. Conversely, if you need a mutable, indexed collection, use an ArrayBuffer.
- List and Vector are often used when writing code in a functional style. ArrayBuffer is commonly used when writing code in an imperative style. ListBuffer is used when you’re mixing styles, such as building a list.


### List
- The List type is a linear, immutable sequence. This just means that it’s a linked-list that you can’t modify.
- Any time you want to add or remove List elements, you create a new List from an existing List.

#### Creating Lists
- This is how you create an initial List:
  ```scala
  val ints = List(1, 2, 3)
  val names = List("Joel", "Chris", "Ed")

  // another way to construct a List
  val namesAgain = "Joel" :: "Chris" :: "Ed" :: Nil
  ```
- You can also declare the List’s type, if you prefer, though it generally isn’t necessary:
  ```scala
  val ints: List[Int] = List(1, 2, 3)
  val names: List[String] = List("Joel", "Chris", "Ed")
  ```
- One exception is when you have mixed types in a collection; in that case you may want to explicitly specify its type:
  ```scala
  val things: List[String | Int | Double] = List(1, "two", 3.0) // with union types
  val thingsAny: List[Any] = List(1, "two", 3.0)                // with any
  ```

#### Adding elements to a List
- When working with a List, prepend one element with ::, and prepend another List with :::, as shown here:
```scala
val a = List(1, 2, 3)

val b = 0 :: a              // List(0, 1, 2, 3)
val c = List(-1, 0) ::: a   // List(-1, 0, 1, 2, 3)
```
- You can also append elements to a List, but because List is a singly-linked list, you should generally only prepend elements to it; appending elements to it is a relatively slow operation, especially when you work with large sequences.
- Tip: If you want to prepend and append elements to an immutable sequence, use Vector instead.
- Because List is a linked-list, you shouldn’t try to access the elements of large lists by their index value. For instance, if you have a List with one million elements in it, accessing an element like myList(999_999) will take a relatively long time, because that request has to traverse all those elements. If you have a large collection and want to access elements by their index, use a Vector or ArrayBuffer instead.

#### How to remember the method names
- These days IDEs help us out tremendously, but one way to remember those method names is to think that the : character represents the side that the sequence is on, so when you use +: you know that the list needs to be on the right, like this:
  ```scala
  0 +: a

  // Similarly, when you use :+ you know the list needs to be on the left:
  a :+ 4
  ```
- Also, a good thing about these symbolic method names is that they’re consistent. The same method names are used with other immutable sequences, such as Seq and Vector. You can also use non-symbolic method names to append and prepend elements, if you prefer.

#### How to loop over lists
- How:
  ```scala
  val names = List("Joel", "Chris", "Ed")
  for name <- names do println(name)
  ```

#### A little bit of history
- For those interested in a little bit of history, the Scala List is similar to the List from the Lisp programming language, which was originally specified in 1958. Indeed, in addition to creating a List like this:
  ```scala
  val ints = List(1, 2, 3)
  val list = 1 :: 2 :: 3 :: Nil
  ```
- This works because a List is a singly-linked list that ends with the Nil element, and :: is a List method that works like Lisp’s “cons” operator.

#### Aside: The LazyList
- The Scala collections also include a LazyList, which is a lazy immutable linked list. It’s called “lazy”—or non-strict—because it computes its elements only when they are needed.
  ```scala
  val x = LazyList.range(1, Int.MaxValue)
  x.take(1)      // LazyList(<not computed>)
  x.take(5)      // LazyList(<not computed>)
  x.map(_ + 1)   // LazyList(<not computed>)
  ```
- In all of those examples, nothing happens. Indeed, nothing will happen until you force it to happen, such as by calling its foreach method:


### Vector
- Vector is an indexed, immutable sequence. The “indexed” part of the description means that it provides random access and update in effectively constant time, so you can access Vector elements rapidly by their index value, such as accessing listOfPeople(123_456_789).
- Here are a few ways you can create a Vector:
  ```scala
  val nums = Vector(1, 2, 3, 4, 5)

  val strings = Vector("one", "two")

  case class Person(name: String)
  val people = Vector(
    Person("Bert"),
    Person("Ernie"),
    Person("Grover")
  )
  ```
- Because Vector is immutable, you can’t add new elements to it. Instead, you create a new sequence by appending or prepending elements to an existing Vector. These examples show how to append and prepend elements to a Vector:
  ```scala
  val a = Vector(1,2,3)         // Vector(1, 2, 3)
  val b = a :+ 4                // Vector(1, 2, 3, 4)
  val c = a ++ Vector(4, 5)     // Vector(1, 2, 3, 4, 5)

  val a = Vector(1,2,3)         // Vector(1, 2, 3)
  val b = 0 +: a                // Vector(0, 1, 2, 3)
  val c = Vector(-1, 0) ++: a   // Vector(-1, 0, 1, 2, 3)
  ```
- In addition to fast random access and updates, Vector provides fast append and prepend times, so you can use these features as desired.
- Finally, you use a Vector in a for loop just like a List, ArrayBuffer, or any other sequence:
  ```scala
  scala> val names = Vector("Joel", "Chris", "Ed")
  val names: Vector[String] = Vector(Joel, Chris, Ed)

  scala> for name <- names do println(name)
  Joel
  Chris
  Ed
  ```

### ArrayBuffer
- Use ArrayBuffer when you need a general-purpose, mutable indexed sequence in your Scala applications. It’s mutable, so you can change its elements, and also resize it. Because it’s indexed, random access of elements is fast.

#### Creating an ArrayBuffer
- To use an ArrayBuffer, first import it:
  ```scala
  import scala.collection.mutable.ArrayBuffer
  ```
- If you need to start with an empty ArrayBuffer, just specify its type:
  ```scala
  var strings = ArrayBuffer[String]()
  var ints = ArrayBuffer[Int]()
  var people = ArrayBuffer[Person]()
  ```
- If you know the approximate size your ArrayBuffer eventually needs to be, you can create it with an initial size:
  ```scala
  // ready to hold 100,000 ints
  val buf = new ArrayBuffer[Int](100_000)
  ```
- To create a new ArrayBuffer with initial elements, just specify its initial elements, just like a List or Vector:
  ```scala
  val nums = ArrayBuffer(1, 2, 3)
  val people = ArrayBuffer(
    Person("Bert"),
    Person("Ernie"),
    Person("Grover")
  )
  ```

#### Changing elements to an ArrayBuffer
- Snippet:
  ```scala
  val nums = ArrayBuffer(1, 2, 3)   // ArrayBuffer(1, 2, 3)
  nums += 4                         // ArrayBuffer(1, 2, 3, 4)
  nums ++= List(5, 6)               // ArrayBuffer(1, 2, 3, 4, 5, 6)

  val a = ArrayBuffer.range('a', 'h')   // ArrayBuffer(a, b, c, d, e, f, g)
  a -= 'a'                              // ArrayBuffer(b, c, d, e, f, g)
  a --= Seq('b', 'c')                   // ArrayBuffer(d, e, f, g)
  a --= Set('d', 'e')                   // ArrayBuffer(f, g)

  val a = ArrayBuffer.range(1,5)        // ArrayBuffer(1, 2, 3, 4)
  a(2) = 50                             // ArrayBuffer(1, 2, 50, 4)
  a.update(0, 10)                       // ArrayBuffer(10, 2, 50, 4)
  ```

### Maps
- A Map is an iterable collection that consists of pairs of keys and values. Scala has both mutable and immutable Map types, and this section demonstrates how to use the immutable Map.

#### Creating an immutable Map
- Snippet:
  ```scala
  val states = Map(
    "AK" -> "Alaska",
    "AL" -> "Alabama",
    "AZ" -> "Arizona"
  )

  for (k, v) <- states do println(s"key: $k, value: $v")
  ```

#### Accessing Map elements
- Snippet:
  ```scala
  val ak = states("AK")   // ak: String = Alaska
  val al = states("AL")   // al: String = Alabama
  ```

#### Adding elements to a Map
- Snippet:
  ```scala
  val a = Map(1 -> "one")    // a: Map(1 -> one)
  val b = a + (2 -> "two")   // b: Map(1 -> one, 2 -> two)
  val c = b ++ Seq(
    3 -> "three",
    4 -> "four"
  )
  // c: Map(1 -> one, 2 -> two, 3 -> three, 4 -> four)
  ```

#### Removing elements from a Map
```scala
val a = Map(
  1 -> "one",
  2 -> "two",
  3 -> "three",
  4 -> "four"
)

val b = a - 4       // b: Map(1 -> one, 2 -> two, 3 -> three)
val c = a - 4 - 3   // c: Map(1 -> one, 2 -> two)
```

#### Updating Map elements
```scala
val a = Map(
  1 -> "one",
  2 -> "two",
  3 -> "three"
)

val b = a.updated(3, "THREE!")   // b: Map(1 -> one, 2 -> two, 3 -> THREE!)
val c = a + (2 -> "TWO...")      // c: Map(1 -> one, 2 -> TWO..., 3 -> three)
```

#### Traversing a Map
  ```scala
  val states = Map(
    "AK" -> "Alaska",
    "AL" -> "Alabama",
    "AZ" -> "Arizona"
  )

  for (k, v) <- states do println(s"key: $k, value: $v")
  ```


### Working with Sets
- The Scala Set is an iterable collection with no duplicate elements.
- Scala has both mutable and immutable Set types. This section demonstrates the immutable Set.


#### Creating a Set
```scala
val nums = Set[Int]()
val letters = Set[Char]()

val nums = Set(1, 2, 3, 3, 3)           // Set(1, 2, 3)
val letters = Set('a', 'b', 'c', 'c')   // Set('a', 'b', 'c')
```

#### Adding elements to a Set
```scala
val a = Set(1, 2)                // Set(1, 2)
val b = a + 3                    // Set(1, 2, 3)
val c = b ++ Seq(4, 1, 5, 5)     // HashSet(5, 1, 2, 3, 4)
```
- Notice that when you attempt to add duplicate elements, they’re quietly dropped.

#### Deleting elements from a Set
  ```scala
  val a = Set(1, 2, 3, 4, 5)   // HashSet(5, 1, 2, 3, 4)
  val b = a - 5                // HashSet(1, 2, 3, 4)
  val c = b -- Seq(3, 4)       // HashSet(1, 2)
  ```

### Range
- The Scala Range is often used to populate data structures and to iterate over for loops. These REPL examples demonstrate how to create ranges:
  ```scala
  1 to 5         // Range(1, 2, 3, 4, 5)
  1 until 5      // Range(1, 2, 3, 4)
  1 to 10 by 2   // Range(1, 3, 5, 7, 9)
  'a' to 'c'     // NumericRange(a, b, c)

  val x = (1 to 5).toList     // List(1, 2, 3, 4, 5)
  val x = (1 to 5).toBuffer   // ArrayBuffer(1, 2, 3, 4, 5)

  for i <- 1 to 3 do println(i)

  Vector.range(1, 5)       // Vector(1, 2, 3, 4)
  List.range(1, 10, 2)     // List(1, 3, 5, 7, 9)
  Set.range(1, 10)         // HashSet(5, 1, 6, 9, 2, 7, 3, 8, 4)
  ```
- When you’re running tests, ranges are also useful for generating test collections:
  ```scala
  val evens = (0 to 10 by 2).toList     // List(0, 2, 4, 6, 8, 10)
  val odds = (1 to 10 by 2).toList      // List(1, 3, 5, 7, 9)
  val doubles = (1 to 5).map(_ * 2.0)   // Vector(2.0, 4.0, 6.0, 8.0, 10.0)

  // create a Map
  val map = (1 to 3).map(e => (e,s"$e")).toMap
      // map: Map[Int, String] = Map(1 -> "1", 2 -> "2", 3 -> "3")
  ```