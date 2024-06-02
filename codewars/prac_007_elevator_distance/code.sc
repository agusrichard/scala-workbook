import scala.collection.mutable.ArrayBuffer

def elevatorDistance(xs: Seq[Int]): Int =
  val result = ArrayBuffer[Int]()
  xs.indices.iterator.takeWhile(i => i+1 <= xs.length-1).foreach(
    i => {
      val remainder = (xs(i + 1) - xs(i)).abs
      result.addOne(remainder)
    }
  )

  result.sum


elevatorDistance(Seq(5, 2, 8))
elevatorDistance(Seq(1, 2, 3))
elevatorDistance(Seq(7, 1, 7, 1))