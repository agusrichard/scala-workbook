import scala.io.StdIn.readLine

object ControlStructuresDetail {
  def main(args: Array[String]): Unit = {
    print("Please enter x: ")
    val x = readLine().toInt

    if x < 0 then
      println("x is negative")
    else if x == 0 then
      println("x is zero")
    else
      println("x is positive")

    val isNegative = if x < 0 then true else false
    println(s"isNegative is ${isNegative}")
    println(compare(10, -1))

    val ints = 0 to 10
    println(ints)
    for i <- ints do
      println(i)

    for
      i <- ints
      j <- ints.map(_i => _i * 2)
      if i % 2 == 0
    do
      println(s"(${i}, ${j})")

    val list = for i <- (0 to 9) yield i
    println(list)

    val anotherList = generateMultiply((0 to 9), 5)
    println(anotherList)

    var i = 0
    while i < 10 do
      println(i*2)
      i += 1

    val day = x match
      case 0 => "Sunday"
      case 1 => "Monday"
      case 2 => "Tuesday"
      case 3 => "Wednesday"
      case 4 => "Thursday"
      case 5 => "Friday"
      case 6 => "Saturday"
      case _ => "invalid day"

    x match
      case 1 => println("One is a good one")
      case y if y == 2 || x == 3 => println("2 and 3 are here")
      case _ => println("Another thing")

    val tup = (1, 2, 3, 4, 5)
    tup match
      case (_, b, _, _, _) if b == 2 => println("B is two")
      case (a, _, _, _, e) if a == 1 || e == 5 => println("One or Five")
      case _ => println("other")
  }

  def compare(a: Int, b: Int): Int =
    if a < b then
      -1
    else if a == b then
      0
    else
      1

  def generateMultiply(list: IndexedSeq[Int], factor: Int): IndexedSeq[Int] =
    for x <- list yield
      val y = x * factor
      val z = y % 2
      z
}
