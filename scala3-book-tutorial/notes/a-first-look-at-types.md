# A FIRST LOOK AT TYPES

Source: https://docs.scala-lang.org/scala3/book/first-look-at-types.html

## All values have a type

- The diagram below illustrates a subset of the type hierarchy.
  ![](https://docs.scala-lang.org/resources/images/scala3-book/hierarchy.svg)

## Scala type hierarchy

- Any is the supertype of all types, also called the top type. It defines certain universal methods such as equals, hashCode, and toString.
- The top-type Any has a subtype Matchable, which is used to mark all types that we can perform pattern matching on.
- We will not go into details here, but in summary, it means that we cannot pattern match on values of type Any, but only on values that are a subtype of Matchable.
- Matchable has two important subtypes: AnyVal and AnyRef.
- AnyVal represents value types. There are a couple of predefined value types, and they are non-nullable: Double, Float, Long, Int, Short, Byte, Char, Unit, and Boolean. Unit is a value type which carries no meaningful information. There is exactly one instance of Unit which we can refer to as: ().
- AnyRef represents reference types. All non-value types are defined as reference types. Every user-defined type in Scala is a subtype of AnyRef. If Scala is used in the context of a Java runtime environment, AnyRef corresponds to java.lang.Object.
- In statement-based languages, void is used for methods that don’t return anything. If you write methods in Scala that have no return value, such as the following method, Unit is used for the same purpose:
  ```scala
  def printIt(a: Any): Unit = println(a)
  ```
- Here’s an example that demonstrates that strings, integers, characters, boolean values, and functions are all instances of Any and can be treated just like every other object:

  ```scala
  val list: List[Any] = List(
    "a string",
    732,  // an integer
    'c',  // a character
    '\'', // a character with a backslash escape
    true, // a boolean value
    () => "an anonymous function returning a string"
  )

  list.foreach(element => println(element))
  ```

## Scala’s “value types”

- As shown above, Scala’s numeric types extend AnyVal, and they’re all full-blown objects. These examples show how to declare variables of these numeric types:
  ```scala
  val b: Byte = 1
  val i: Int = 1
  val l: Long = 1
  val s: Short = 1
  val d: Double = 2.0
  val f: Float = 3.0
  ```
- In the first four examples, if you don’t explicitly specify a type, the number 1 will default to an Int, so if you want one of the other data types—Byte, Long, or Short—you need to explicitly declare those types, as shown.
- Numbers with a decimal (like 2.0) will default to a Double, so if you want a Float you need to declare a Float, as shown in the last example.
- Because Int and Double are the default numeric types, you typically create them without explicitly declaring the data type:
  ```scala
  val i = 123   // defaults to Int
  val x = 1.0   // defaults to Double
  ```
- In your code you can also append the characters L, D, and F (and their lowercase equivalents) to numbers to specify that they are Long, Double, or Float values:
  ```scala
  val x = 1_000L   // val x: Long = 1000
  val y = 2.2D     // val y: Double = 2.2
  val z = -3.3F    // val z: Float = -3.3
  ```
- You may also use hexadecimal notation to format integer numbers (normally Int, but which also support the L suffix to specify that they are Long):
  ```scala
  val a = 0xACE    // val a: Int = 2766
  val b = 0xfd_3aL // val b: Long = 64826
  ```
- Scala supports many different ways to format the same floating point number, e.g.
  ```scala
  val q = .25      // val q: Double = 0.25
  val r = 2.5e-1   // val r: Double = 0.25
  val s = .0025e2F // val s: Float = 0.25
  ```
- Scala also has String and Char types, which you can generally declare with the implicit form:
  ```scala
  val s = "Bill"
  val c = 'a'
  ```
- As shown, enclose strings in double-quotes—or triple-quotes for multiline strings—and enclose a character in single-quotes.

## Strings

- Scala strings are similar to Java strings though unlike Java (at least before Java 15), it’s easy to create multiline strings with triple quotes:
  ```scala
  val quote = """The essence of Scala:
                Fusion of functional and object-oriented
                programming in a typed setting."""
  ```
- When spacing is important, put a | symbol in front of all lines after the first line, and call the stripMargin method after the string:
  ```scala
  val quote = """The essence of Scala:
                |Fusion of functional and object-oriented
                |programming in a typed setting.""".stripMargin
  ```

## BigInt and BigDecimal

- When you need really large numbers, use the BigInt and BigDecimal types:
  ```scala
  val a = BigInt(1_234_567_890_987_654_321L)
  val b = BigDecimal(123_456.789)
  ```
- Where Double and Float are approximate decimal numbers, BigDecimal is used for precise arithmetic, such as when working with currency.
- A great thing about BigInt and BigDecimal is that they support all the operators you’re used to using with numeric types:
  ```scala
  val b = BigInt(1234567890)   // scala.math.BigInt = 1234567890
  val c = b + b                // scala.math.BigInt = 2469135780
  val d = b * b                // scala.math.BigInt = 1524157875019052100
  ```

## Type casting

- Value types can be cast in the following way:
  ![](https://docs.scala-lang.org/resources/images/tour/type-casting-diagram.svg)
- Example:

  ```scala
  val b: Byte = 127
  val i: Int = b  // 127

  val face: Char = '☺'
  val number: Int = face  // 9786
  ```

- You can only cast to a type if there is no loss of information. Otherwise, you need to be explicit about the cast:
  ```scala
  val x: Long = 987654321
  val y: Float = x.toFloat  // 9.8765434E8 (note that `.toFloat` is required because the cast results in precision loss)
  val z: Long = y  // Error
  ```

## Nothing and null

- Nothing is a subtype of all types, also called the bottom type. There is no value that has the type Nothing.
- A common use is to signal non-termination, such as a thrown exception, program exit, or an infinite loop—i.e., it is the type of an expression which does not evaluate to a value, or a method that does not return normally.
- Null is a subtype of all reference types (i.e. any subtype of AnyRef). It has a single value identified by the keyword literal null.
- In the meantime, null should almost never be used in Scala code.
