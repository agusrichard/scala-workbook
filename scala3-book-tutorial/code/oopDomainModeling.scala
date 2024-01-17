trait Speak:
    def speak(): String

trait TailWagger:
    def startTail(): Unit = println("Tail is wagging")
    def stopTail(): Unit = println("Tail is stopped")

trait Runner:
    def startRunning(): Unit = println("I'm running")
    def stopRunning(): Unit = println("Stopped running")

class Dog(name: String) extends Speak, TailWagger, Runner:
    def speak(): String = "Woof"

class Cat(name: String) extends Speak, TailWagger, Runner:
    def speak(): String = "Meow"
    override def startTail(): Unit = println("I don't wag my tail")
    override def stopTail(): Unit = println("I said I don't wag my tail")

@main def oopDomainModeling() = 
    println("Damara Astiningtyas")
    val d = Dog("Sekar")
    val c = Cat("Saskia")
    d.startTail()
    d.stopTail()
    c.startTail()
    c.stopTail()