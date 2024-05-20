# Scala Tools

**Sources:**
- https://docs.scala-lang.org/scala3/book/tools-sbt.html

## Building Scala projects with sbt
- Creating a “Hello, world” project
  ```shell
  $ mkdir hello
  $ cd hello
  ```
- In the directory hello, create a subdirectory project:
  ```shell
  $ mkdir project
  ```
- Create a file named build.properties in the directory project, with the following content:
  ```text
  sbt.version=1.6.1
  ```
- Then create a file named build.sbt in the project root directory that contains this line:
  ```text
  scalaVersion := "3.4.2"
  ```
- Now create a file named something like Hello.scala—the first part of the name doesn’t matter—with this line:
  ```scala 3
  @main def helloWorld = println("Hello, world")
  ```
- You should have a project structure like the following:
  ```text
  $ tree
  .
  ├── build.sbt
  ├── Hello.scala
  └── project
      └── build.properties
  ```
- You should see output that looks like this, including the "Hello, world" from your program:
  ```shell
  $ sbt run
  [info] welcome to sbt 1.5.4 (AdoptOpenJDK Java 11.x)
  [info] loading project definition from project ...
  [info] loading settings for project from build.sbt ...
  [info] compiling 1 Scala source to target/scala-3.0.0/classes ...
  [info] running helloWorld
  Hello, world
  [success] Total time: 2 s
  ```
- The sbt launcher—the sbt command-line tool—loads the version of sbt set in the file project/build.properties, which loads the version of the Scala compiler set in the file build.sbt, compiles the code in the file Hello.scala, and runs the resulting bytecode.
- When you look at your directory, you’ll see that sbt has a directory named target. These are working directories that sbt uses.

### Using sbt with larger projects
- For a little project, that’s all that sbt requires to run. For larger projects that require many source code files, dependencies, or sbt plugins, you’ll want to create an organized directory structure. The rest of this section demonstrates the structure that sbt uses.

### The sbt directory structure
- Like Maven, sbt uses a standard project directory structure. A nice benefit of that is that once you’re comfortable with its structure, it makes it easy to work on other Scala/sbt projects.
- The first thing to know is that underneath the root directory of your project, sbt expects a directory structure that looks like this:
  ```text
  .
  ├── build.sbt
  ├── project/
  │   └── build.properties
  ├── src/
  │   ├── main/
  │   │   ├── java/
  │   │   ├── resources/
  │   │   └── scala/
  │   └── test/
  │       ├── java/
  │       ├── resources/
  │       └── scala/
  └── target/
  ```
- You can also add a lib directory under the root directory if you want to add unmanaged dependencies—JAR files—to your project.
- If you’re going to create a project that has Scala source code files and tests, but won’t be using any Java source code files, and doesn’t need any “resources”—such as embedded images, configuration files, etc.—this is all you really need under the src directory:
  ```text
  .
  └── src/
      ├── main/
      │   └── scala/
      └── test/
          └── scala/
  ```

### “Hello, world” with an sbt directory structure
- Creating this directory structure is simple. There are tools to do this for you, but assuming that you’re using a Unix/Linux system, you can use these commands to create your first sbt project directory structure:
  ```shell
  $ mkdir HelloWorld
  $ cd HelloWorld
  $ mkdir -p src/{main,test}/scala
  $ mkdir project target
  ```
  
### Creating a first build.sbt file
- For a little project like this, the build.sbt file only needs a scalaVersion entry, but we’ll add three lines that you commonly see:
  ```text
  name := "HelloWorld"
  version := "0.1"
  scalaVersion := "3.4.2"
  ```

### A “Hello, world” program
- In large projects, all of your Scala source code files will go under the src/main/scala and src/test/scala directories, but for a little sample project like this, you can put your source code file in the root directory of your project. Therefore, create a file named HelloWorld.scala in the root directory with these contents:
  ```scala 3
  @main def helloWorld = println("Hello, world")
  ```
- Now, use the sbt run command to compile and run your project:
- The first time you run sbt it downloads everything it needs, and that can take a few moments to run, but after that it gets much faster.
- Also, once you get this first step working, you’ll find that it’s much faster to run sbt interactively. To do that, first run the sbt command by itself:
  ```text
  $ sbt

  [info] welcome to sbt
  [info] loading settings for project ...
  [info] loading project definition ...
  [info] loading settings for project root from build.sbt ...
  [info] sbt server started at
         local:///${HOME}/.sbt/1.0/server/7d26bae822c36a31071c/sock
  sbt:hello-world> _
  ```
- Then inside this sbt shell, execute its run command:
  ```text
  sbt:hello-world> run

  [info] running helloWorld 
  Hello, world
  [success] Total time: 0 s
  ```

### Using project templates
- Manually creating the project structure can be tedious. Thankfully, sbt can create it for you, based on a template.
- To create a Scala 3 project from a template, run the following command in a shell:
  ```shell
  $ sbt new scala/scala3.g8
  ```
- Sbt will load the template, ask some questions, and create the project files in a subdirectory:
  ```text
  $ tree scala-3-project-template 
  scala-3-project-template
  ├── build.sbt
  ├── project
  │   └── build.properties
  ├── README.md
  └── src
      ├── main
      │   └── scala
      │       └── Main.scala
      └── test
          └── scala
              └── Test1.scala
  ```

## Using sbt with ScalaTest
- ScalaTest is one of the main testing libraries for Scala projects. In this section you’ll see the steps necessary to create a Scala/sbt project that uses ScalaTest.

### 1) Create the project directory structure
- As with the previous lesson, create an sbt project directory structure for a project named HelloScalaTest with the following commands:
  ```shell
  $ mkdir HelloScalaTest
  $ cd HelloScalaTest
  $ mkdir -p src/{main,test}/scala
  $ mkdir project
  ```

### 2) Create the build.properties and build.sbt files
- Next, create a build.properties file in the project/ subdirectory of your project with this line:
  ```text
  sbt.version=1.5.4
  ```
- Next, create a build.sbt file in the root directory of your project with these contents:
  ```text
  name := "HelloScalaTest"
  version := "0.1"
  scalaVersion := "3.4.2"

  libraryDependencies ++= Seq(
    "org.scalatest" %% "scalatest" % "3.2.9" % Test
  )
  ```
- The first three lines of this file are essentially the same as the first example. The libraryDependencies lines tell sbt to include the dependencies (JAR files) that are needed to include ScalaTest.

### 3) Create a Scala source code file
- Next, create a Scala program that you can use to demonstrate ScalaTest. First, create a directory under src/main/scala named math:
  ```shell
  $ mkdir src/main/scala/math
              ----
  ```
- Then, inside that directory, create a file named MathUtils.scala with these contents:
  ```scala 3
  package math

  object MathUtils:
    def double(i: Int) = i * 2
  ```

### 4) Create your first ScalaTest tests
- ScalaTest is very flexible, and offers several different ways to write tests. A simple way to get started is to write tests using the ScalaTest AnyFunSuite. To get started, create a directory named math under the src/test/scala directory:
  ```shell
  $ mkdir src/test/scala/math
              ----
  ```
- Next, create a file named MathUtilsTests.scala in that directory with the following contents:
  ```scala 3
  package math
    
  import org.scalatest.funsuite.AnyFunSuite

  class MathUtilsTests extends AnyFunSuite:

    // test 1
    test("'double' should handle 0") {
      val result = MathUtils.double(0)
      assert(result == 0)
    }

    // test 2
    test("'double' should handle 1") {
      val result = MathUtils.double(1)
      assert(result == 2)
    }
   
    test("test with Int.MaxValue") (pending)

  end MathUtilsTests
  ```
- This code demonstrates the ScalaTest AnyFunSuite approach. A few important points:
  - Your test class should extend AnyFunSuite
  - You create tests as shown, by giving each test a unique name
  - At the end of each test you should call assert to test that a condition has been satisfied
  - When you know you want to write a test, but you don’t want to write it right now, create the test as “pending,” with the syntax shown
- Using ScalaTest like this is similar to JUnit, so if you’re coming to Scala from Java, hopefully this looks similar.
- Now you can run these tests with the sbt test command. Skipping the first few lines of output, the result looks like this:
  ```shell
  sbt:HelloScalaTest> test

  [info] Compiling 1 Scala source ...
  [info] MathUtilsTests:
  [info] - 'double' should handle 0
  [info] - 'double' should handle 1
  [info] - test with Int.MaxValue (pending)
  [info] Total number of tests run: 2
  [info] Suites: completed 1, aborted 0
  [info] Tests: succeeded 2, failed 0, canceled 0, ignored 0, pending 1
  [info] All tests passed.
  [success] Total time: 1 s
  ```
- If everything works well, you’ll see output that looks like that. Welcome to the world of testing Scala applications with sbt and ScalaTest.

### Support for many types of tests
- This example demonstrates a style of testing that’s similar to xUnit Test-Driven Development (TDD) style testing, with a few benefits of the Behavior-Driven Development (BDD) style.
- As mentioned, ScalaTest is flexible and you can also write tests using other styles, such as a style similar to Ruby’s RSpec. You can also use mock objects, property-based testing, and use ScalaTest to test Scala.js code.