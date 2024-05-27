# Interacting with Java

**Sources:**
- https://docs.scala-lang.org/scala3/book/interacting-with-java.html

## How to use Java collections in Scala
- When you’re writing Scala code and an API either requires or produces a Java collection class (from the java.util package), then it is valid to directly use or create the collection as you would in Java.
- However, for idiomatic usage in Scala, such as for loops over the collection, or to apply higher-order functions such as map and filter, you can create a proxy that behaves like a Scala collection.
- Here’s an example of how this works. Given this API that returns java.util.List[String]:
    ```java
    public interface Foo {
      static java.util.List<String> getStrings() {
        return List.of("a", "b", "c");
      }
    }
    ```
- You can convert that Java list to a Scala Seq, using the conversion utilities in the Scala scala.jdk.CollectionConverters object:
  ```scala 3
  import scala.jdk.CollectionConverters.*
  import scala.collection.mutable

  def testList() =
    println("Using a Java List in Scala")
    val javaList: java.util.List[String] = Foo.getStrings()
    val scalaSeq: mutable.Seq[String] = javaList.asScala
    for s <- scalaSeq do println(s)
  ```
- In the above code javaList.asScala creates a wrapper that adapts a java.util.List to Scala’s mutable.Seq collection.

## How to use Java Optional in Scala
- When you are interacting with an API that uses the java.util.Optional class in your Scala code, it is fine to construct and use as in Java.
- However, for idiomatic usage in Scala, such as use with for, you can convert it to a Scala Option.
  ```java
  public interface Bar {
    static java.util.Optional<String> optionalString() {
      return Optional.of("hello");
    }
  }
  ```
- First import all members from the scala.jdk.OptionConverters object, and then use the toScala method to convert the Optional value to a Scala Option:
  ```scala 3
  import java.util.Optional
  import scala.jdk.OptionConverters.*

  val javaOptString: Optional[String] = Bar.optionalString
  val scalaOptString: Option[String] = javaOptString.toScala
  ```

## Extending Java interfaces in Scala
- If you need to use Java interfaces in your Scala code, extend them just as though they are Scala traits. For example, given these three Java interfaces:
  ```java
  public interface Animal {
    void speak();
  }

  public interface Wagging {
    void wag();
  }

  public interface Running {
    // an implemented method
    default void run() {
      System.out.println("I’m running");
    }
  }
  ```
- you can create a Dog class in Scala just as though you were using traits. Because run has a default implementation, you only need to implement the speak and wag methods:
  ```scala 3
  class Dog extends Animal, Wagging, Running:
    def speak = println("Woof")
    def wag = println("Tail is wagging")

  def useJavaInterfaceInScala =
    val d = Dog()
    d.speak
    d.wag
    d.run
  ```
- Also notice that in Scala, Java methods defined with empty parameter lists can be called either as in Java, .wag(), or you can choose to not use parentheses .wag.

## How to use Scala collections in Java
- When you need to use a Scala collection class in your Java code, use the methods of Scala’s scala.jdk.javaapi.CollectionConverters object in your Java code to make the conversions work.
- For example, suppose that a Scala API returns a List[String] like this:
  ```scala 3
  object Baz:
    val strings: List[String] = List("a", "b", "c")
  ```
- You can access that Scala List in your Java code like this:
  ```java
  import scala.jdk.javaapi.CollectionConverters;

  // access the `strings` method with `Baz.strings()`
  scala.collection.immutable.List<String> xs = Baz.strings();

  java.util.List<String> listOfStrings = CollectionConverters.asJava(xs);

  for (String s: listOfStrings) {
    System.out.println(s);
  }
  ```
- That code can be shortened, but the full steps are shown to demonstrate how the process works. Be sure to notice that while Baz has a field named strings, from Java the field appears as a method, so must be called with parentheses .strings().

## How to use Scala Option in Java
- When you need to use a Scala Option in your Java code, you can convert the Option to a Java Optional value using the toJava method of the Scala scala.jdk.javaapi.OptionConverters object.
- For example, suppose that a Scala API returns an Option[String] like this:
  ```scala 3
  object Qux:
    val optString: Option[String] = Option("hello")
  ```
- Then you can access that Scala Option in your Java code like this:
  ```java
  import java.util.Optional;
  import scala.Option;
  import scala.jdk.javaapi.OptionConverters;

  Option<String> scalaOptString = Qux.optString();
  Optional<String> javaOptString = OptionConverters.toJava(scalaOptString);
  ```
- That code can be shortened, but the full steps are shown to demonstrate how the process works. Be sure to notice that while Qux has a field named optString, from Java the field appears as a method, so must be called with parentheses .optString().

## How to use Scala traits in Java
- From Java 8 you can use a Scala trait just like a Java interface, even if the trait has implemented methods. For example, given these two Scala traits, one with an implemented method and one with only an interface:
  ```scala 3
  trait ScalaAddTrait:
    def sum(x: Int, y: Int) = x + y     // implemented

  trait ScalaMultiplyTrait:
    def multiply(x: Int, y: Int): Int   // abstract
  ```
- A Java class can implement both of those interfaces, and define the multiply method:
  ```java
  class JavaMath implements ScalaAddTrait, ScalaMultiplyTrait {
    public int multiply(int a, int b) {
      return a * b;
    }
  }

  JavaMath jm = new JavaMath();
  System.out.println(jm.sum(3,4));        // 7
  System.out.println(jm.multiply(3,4));   // 12
  ```
  
## How to handle Scala methods that throw exceptions in Java code
- When you’re writing Scala code using Scala programming idioms, you’ll never write a method that throws an exception. But if for some reason you have a Scala method that does throw an exception, and you want Java developers to be able to use that method, add the @throws annotation to your Scala method so Java consumers will know the exceptions it can throw.
- For example, this Scala exceptionThrower method is annotated to declare that it throws an Exception:
  ```scala 3
  object SExceptionThrower:
    @throws[Exception]
    def exceptionThrower =
      throw Exception("Idiomatic Scala methods don’t throw exceptions")
  ```
- As a result, you’ll need to handle the exception in your Java code. For instance, this code won’t compile because I don’t handle the exception:
  ```java
  // won’t compile because the exception isn’t handled
  public class ScalaExceptionsInJava {
    public static void main(String[] args) {
      SExceptionThrower.exceptionThrower();
    }
  }
  ```
- This is good—it’s what you want: the annotation tells the Java compiler that exceptionThrower can throw an exception. Now when you’re writing Java code you must handle the exception with a try block or declare that your Java method throws an exception.
- Conversely, if you leave the annotation off of the Scala exceptionThrower method, the Java code will compile. This is probably not what you want, because the Java code may not account for the Scala method throwing the exception.

## How to use Scala varargs parameters in Java
- When a Scala method has a varargs parameter and you want to use that method in Java, mark the Scala method with the @varargs annotation. For example, the printAll method in this Scala class declares a String* varargs field:
  ```scala 3
  import scala.annotation.varargs

  object VarargsPrinter:
    @varargs def printAll(args: String*): Unit = args.foreach(println)
  ```
- Because printAll is declared with the @varargs annotation, it can be called from a Java program with a variable number of parameters, as shown in this example:
  ```java
  public class JVarargs {
    public static void main(String[] args) {
      VarargsPrinter.printAll("Hello", "world");
    }
  }
  ```
  
## Create alternate names to use Scala methods in Java
- In Scala you might want to create a method name using a symbolic character:
  ```scala 3
  def +(a: Int, b: Int) = a + b
  ```
- That method name won’t work well in Java, but what you can do in Scala is provide an “alternate” name for the method with the targetName annotation, which will be the name of the method when used from Java:
  ```scala 3
  import scala.annotation.targetName

  object Adder:
    @targetName("add") def +(a: Int, b: Int) = a + b
  ```
- Now in your Java code you can use the aliased method name add:
  ```java
  int x = Adder.add(1,1);
  System.out.printf("x = %d\n", x);
  ```