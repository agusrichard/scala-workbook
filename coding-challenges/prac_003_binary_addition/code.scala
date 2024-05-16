import scala.util.control.Breaks._
import scala.math._

def addBinary(a: Int, b: Int): String =
  val result = a + b
  convert(result)

def convert(a: Int): String =
  var result = ""
  var next = a
  breakable {
    while true do
      val remainder = next % 2
      next = floorDiv(next, 2)

      result = remainder.toString + result

      if next == 0 then
        break()
  }

  result
