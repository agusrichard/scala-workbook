# Scala for Python Developers

**Sources:**
- https://docs.scala-lang.org/scala3/book/scala-for-python-devs.html

## Comments:
  ```python
  # a comment
  ```
  ```scala 3
  // a comment
  /* ... */
  /** ... */
  ```

## Variable assignment
- Create integer and string variables
  ```python
  x = 1
  x = "Hi"
  y = """foo
         bar
         baz"""
  ```
  ```scala 3
  val x = 1
  val x = "Hi"
  val y = """foo
             bar
             baz"""
  ```
- Lists:
  ```python
  x = [1,2,3]
  ```
  ```scala 3
  val x = List(1,2,3)
  ```
- Dictionary/Map:
```python
x = {
  "Toy Story": 8.3,
  "Forrest Gump": 8.8,
  "Cloud Atlas": 7.4
}
```
```scala 3

val x = Map(
  "Toy Story" -> 8.3,
  "Forrest Gump" -> 8.8,
  "Cloud Atlas" -> 7.4
)
```
- Set
  ```python
  x = {1,2,3}
  ```
  ```scala 3
  val x = Set(1,2,3)
  ```
- Set
  ```python
  x = (11, "Eleven")
  ```
  ```scala 3
  val x = (11, "Eleven")

  // Mutable
  var x = 1
  x += 1
  ```
- However, the rule of thumb in Scala is to always use val unless the variable specifically needs to be mutated.

## FP style records
- Scala case classes are similar to Python frozen dataclasses.
- Constructor definition:
  ```python
  from dataclasses import dataclass, replace

  @dataclass(frozen=True)
  class Person:
    name: str
    age: int
  ```
  ```scala 3
  case class Person(name: String, age: Int)
  ```
- Create and use an instance:
  ```python
  p = Person("Alice", 42)
  p.name   # Alice
  p2 = replace(p, age=43)
  ```
  ```scala 3
  val p = Person("Alice", 42)
  p.name   // Alice
  val p2 = p.copy(age = 43)
  ```
  
## OOP style classes and methods
- OOP style class, primary constructor:
  ```python
  class Person(object):
    def __init__(self, name):
      self.name = name

    def speak(self):
      print(f'Hello, my name is {self.name}')
  ```
  ```scala 3
  class Person (var name: String):
    def speak() = println(s"Hello, my name is $name")
  ```
- Create and use an instance:
  ```python
  p = Person("John")
  p.name   # John
  p.name = 'Fred'
  p.name   # Fred
  p.speak()
  ```
  ```scala 3
  val p = Person("John")
  p.name   // John
  p.name = "Fred"
  p.name   // Fred
  p.speak()
  ```
- One-line method:
  ```python
  def add(a, b): return a + b
  ```
  ```scala 3
  def add(a: Int, b: Int): Int = a + b
  ```
- Multiline method:
  ```python
  def walkThenRun():
    print('walk')
    print('run')
  ```
  ```scala 3
  def walkThenRun() =
    println("walk")
    println("run")
  ```
  
## Interfaces, traits, and inheritance
- If you’re familiar with Java 8 and newer, Scala traits are similar to those Java interfaces. Traits are used all the time in Scala, while Python interfaces (Protocols) and abstract classes are used much less often. Therefore, rather than attempt to compare the two, this example shows how to use Scala traits to build a small solution to a simulated math problem:
  ```scala 3
  trait Adder:
    def add(a: Int, b: Int) = a + b

  trait Multiplier:
    def multiply(a: Int, b: Int) = a * b

  // create a class from the traits
  class SimpleMath extends Adder, Multiplier
  val sm = new SimpleMath
  sm.add(1,1)        // 2
  sm.multiply(2,2)   // 4
  ```
  
## Control structures
- if statement, one line:
  ```python
  if x == 1: print(x)
  ```
  ```scala 3
  if x == 1 then println(x)
  ```
- if statement, multiline:
  ```python
  if x == 1:
    print("x is 1, as you can see:")
    print(x)
  ```
  ```scala 3
  if x == 1 then
    println("x is 1, as you can see:")
    println(x)
  ```
- if, else if, else:
  ```python
  if x < 0:
    print("negative")
  elif x == 0:
    print("zero")
  else:
    print("positive")
  ```
  ```scala 3
  if x < 0 then
    println("negative")
  else if x == 0 then
    println("zero")
  else
    println("positive")
  ```
- Returning a value from if:
```python
min_val = a if a < b else b
```
```scala 3
val minValue = if a < b then a else b
```
- if as the body of a method:
  ```python
  def min(a, b):
    return a if a < b else b
  ```
  ```scala 3
  def min(a: Int, b: Int): Int =
    if a < b then a else b
  ```
- while loop:
  ```python
  i = 1
  while i < 3:
    print(i)
    i += 1
  ```
  ```scala 3
  var i = 1
  while i < 3 do
    println(i)
    i += 1
  ```
- for loop with range:
  ```python
  for i in range(0,3):
    print(i)
  ```
  ```scala 3
  // preferred
  for i <- 0 until 3 do println(i)

  // also available
  for (i <- 0 until 3) println(i)

  // multiline syntax
  for
    i <- 0 until 3
  do
    println(i)
  ```
- for loop with a list:
  ```python
  for i in ints: print(i)

  for i in ints:
    print(i)
  ```
  ```scala 3
  for i <- ints do println(i)
  ```
- for loop, multiple lines:
  ```python
  for i in ints:
    x = i * 2
    print(f"i = {i}, x = {x}")
  ```
  ```scala 3
  for
    i <- ints
  do
    val x = i * 2
    println(s"i = $i, x = $x")
  ```
- Multiple “range” generators:
  ```python
  for i in range(1,3):
    for j in range(4,6):
      for k in range(1,10,3):
        print(f"i = {i}, j = {j}, k = {k}")
  ```
  ```scala 3
  for
    i <- 1 to 2
    j <- 4 to 5
    k <- 1 until 10 by 3
  do
    println(s"i = $i, j = $j, k = $k")
  ```
- Generator with guards (if expressions):
  ```python
  for i in range(1,11):
    if i % 2 == 0:
      if i < 5:
        print(i)
  ```
  ```scala 3
  for
    i <- 1 to 10
    if i % 2 == 0
    if i < 5
  do
    println(i)
  ```
- Multiple if conditions per line:
  ```python
  for i in range(1,11):
    if i % 2 == 0 and i < 5:
      print(i)
  ```
  ```scala 3
  for
    i <- 1 to 10
    if i % 2 == 0 && i < 5
  do
    println(i)
  ```
- Comprehensions:
  ```python
  xs = [i * 10 for i in range(1, 4)]
  # xs: [10,20,30]
  ```
  ```scala 3
  val xs = for i <- 1 to 3 yield i * 10
  // xs: Vector(10, 20, 30)
  ```
- match expressions:
  ```python
  # From 3.10, Python supports structural pattern matching
  # You can also use dictionaries for basic “switch” functionality
  match month:
    case 1:
      monthAsString = "January"
    case 2:
      monthAsString = "February"
    case _:
      monthAsString = "Other"
  ```
  ```scala 3
  val monthAsString = month match
    case 1 => "January"
    case 2 => "February"
    _ => "Other"
  ```
- switch/match:
  ```python
  # Only from Python 3.10
  match i:
    case 1 | 3 | 5 | 7 | 9:
      numAsString = "odd"
    case 2 | 4 | 6 | 8 | 10:
      numAsString = "even"
    case _:
      numAsString = "too big"
  ```
  ```scala 3
  val numAsString = i match
    case 1 | 3 | 5 | 7 | 9 => "odd"
    case 2 | 4 | 6 | 8 | 10 => "even"
    case _ => "too big"
  ```
- try, catch, finally:
  ```python
  try:
    print(a)
  except NameError:
    print("NameError")
  except:
    print("Other")
  finally:
    print("Finally")
  ```
  ```scala 3
  try
    writeTextToFile(text)
  catch
    case ioe: IOException =>
      println(ioe.getMessage)
    case fnf: FileNotFoundException =>
      println(fnf.getMessage)
  finally
    println("Finally")
  ```


============
```python

```
```scala 3

```