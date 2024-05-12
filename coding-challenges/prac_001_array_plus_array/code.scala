def arrayPlusArray(xs: Seq[Int], ys: Seq[Int]): Int = {
  var result = 0
  for x <- xs do result += x

  for y <- ys do result += y

  result
}
