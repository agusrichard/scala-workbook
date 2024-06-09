def nbYear(p0: Int, percent: Double, aug: Int, p: Int): Int = {
  var year = 0
  var current = p0
  while current < p do
    current = current + (current * (percent * 0.01)).toInt + aug
    year += 1

  year
}

nbYear(1500, 5.0, 100, 5000)
nbYear(1500000, 2.5, 10000, 2000000)
(2.2 / 2).toInt