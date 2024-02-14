# STRING INTERPOLATION

Source: https://docs.scala-lang.org/scala3/book/string-interpolation.html#the-f-interpolator-f-strings

## Introduction

- String interpolation provides a way to use variables inside strings. For instance:
  ```scala
  val name = "James"
  val age = 30
  println(s"$name is $age years old")   // "James is 30 years old"
  ```
- Scala provides three string interpolation methods out of the box: s, f and raw. Further, a string interpolator is a just special method so it is possible to define your own. For instance, some database libraries define a sql interpolator that returns a database query.

## The s Interpolator (s-Strings)

- Prepending s to any string literal allows the usage of variables directly in the string. You’ve already seen an example here:
  ```scala
  val name = "James"
  val age = 30
  println(s"$name is $age years old")   // "James is 30 years old"
  ```
- While it may seem obvious, it’s important to note here that string interpolation will not happen in normal string literals
  ```scala
  val name = "James"
  val age = 30
  println("$name is $age years old")   // "$name is $age years old"
  ```
- String interpolators can also take arbitrary expressions. For example:
  ```scala
  println(s"2 + 2 = ${2 + 2}")   // "2 + 2 = 4"
  val x = -1
  println(s"x.abs = ${x.abs}")   // "x.abs = 1"
  ```
- Other examples:

```scala
println(s"New offers starting at $$14.99")   // "New offers starting at $14.99"

println(s"""{"name":"James"}""")     // `{"name":"James"}`

println(s"""name: "$name",
           |age: $age""".stripMargin)
// name: "James"
// age: 30
```

## The f Interpolator (f-Strings)

- Prepending f to any string literal allows the creation of simple formatted strings, similar to printf in other languages. When using the f interpolator, all variable references should be followed by a printf-style format string, like %d. Let’s look at an example:
  ```scala
  val height = 1.9d
  val name = "James"
  println(f"$name%s is $height%2.2f meters tall")  // "James is 1.90 meters tall"
  ```
- The f interpolator is typesafe. If you try to pass a format string that only works for integers but pass a double, the compiler will issue an error. For example:

  ```scala
  val height: Double = 1.9d

  scala> f"$height%4d"
  -- Error: ----------------------------------------------------------------------
  1 |f"$height%4d"
    |   ^^^^^^
    |   Found: (height : Double), Required: Int, Long, Byte, Short, BigInt
  1 error found
  ```

- Finally, as in Java, use %% to get a literal % character in the output string:
  ```scala
  println(f"3/19 is less than 20%%")  // "3/19 is less than 20%"
  ```

### The raw Interpolator

- The raw interpolator is similar to the s interpolator except that it performs no escaping of literals within the string. Here’s an example processed string:
  ```scala
  scala> s"a\nb"
  res0: String =
  a
  b
  ```
- Here the s string interpolator replaced the characters \n with a return character. The raw interpolator will not do that.
  ```scala
  scala> raw"a\nb"
  res1: String = a\nb
  ```

## Advanced Usage

- Custom interpolator:

  ```scala
  extension (sc: StringContext)
    def p(args: Double*): Point = {
      // reuse the `s`-interpolator and then split on ','
      val pts = sc.s(args: _*).split(",", 2).map { _.toDoubleOption.getOrElse(0.0) }
      Point(pts(0), pts(1))
    }

  val x=12.0

  p"1, -2"        // Point(1.0, -2.0)
  p"${x/5}, $x"   // Point(2.4, 12.0)
  ```
