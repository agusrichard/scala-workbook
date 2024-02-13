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
