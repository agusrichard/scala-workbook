import scala.io.StdIn.readLine

@main def helloInteractive() =
  print("Give me some number: ")
  val num = readLine().toInt

  if num < 0 then
    println("\nIt's negative sir")
  else if num == 0 then
    println("You're giving me nothing")
  else
    println("Affirmative")

  for
    i <- 0 to num
    if i % 2 == 0
  do
    println(i)
