# A TASTE OF SCALA

Source: https://docs.scala-lang.org/scala3/book/taste-intro.html

### Your First Scala Program

- Snippet:
  ```scala
  @main def hello() = println("Hello World")
  ```
- In this code, hello is a method. It’s defined with def, and declared to be a “main” method with the @main annotation. It prints the "Hello, World!" string to standard output (STDOUT) using the println method.
- Next, compile the code with scalac:
  ```shell
  $ scalac hello.scala
  ```

### Ask For User Input

- There are several ways to read input from a command-line, but a simple way is to use the readLine method in the scala.io.StdIn object.
- Snippet:

  ```scala
  import scala.io.StdIn.readLine

  @main def helloInteractive() =
      println("Please enter your name: ")
      val name = readLine()

      println("Hello, " + name + "!")

  ```

### THE REPL

- You start a REPL session by running the scala or scala3 command depending on your installation at your operating system command line, where you’ll see a “welcome” prompt like this: `$ scala`

A new year yuhuu
Now I'm fully certified
Good things always
Don't know
again
Back to work again man!
Just kidding, today's holiday
Let's start to work again
