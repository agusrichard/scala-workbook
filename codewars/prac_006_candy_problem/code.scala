def candies(xs: Seq[Int]): Int =
  if xs.isEmpty then return -1
  if xs.length == 1 then return -1

  val max = xs.max
  val remainder = for x <- xs yield max - x

  remainder.sum