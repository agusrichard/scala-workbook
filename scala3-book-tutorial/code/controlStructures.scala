import scala.util.Try
import scala.io.StdIn.readLine

@main def controlStructures() =
    println("Please enter x: ")
    val input = readLine()
    val x = input.toInt

    if x < 0 then
        println("negative")
    else if x == 0 then
        println("zero")
    else
        println("positive")

    val y = if x > 17 then "You're old enough" else "You're too young"
    println(s"What are you? $y")

    val ints = List(1,2,3,4,5)
    for i <- ints do
        println(i)

    var counter = 0
    while counter < 10
    do 
        println(counter)
        counter += 1

    for
        i <- 1 to 3
        j <- 'a' to 'c'
        if i == 2
        if j == 'b'
    do
        println(s"i = $i, j = $j")   // prints: "i = 2, j = b"

    val doubles: List[Int] = List(2, 4, 6, 8, 10)
    println(doubles)