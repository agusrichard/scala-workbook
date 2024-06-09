import scala.annotation.tailrec

def nbYear(p0: Int, percent: Double, aug: Int, p: Int): Int = {
  var year = 0
  var current = p0
  while current < p do
    current = current + (current * (percent * 0.01)).toInt + aug
    year += 1

  year
}

@tailrec
def nbYearTail(p0: Int, percent: Double, aug: Int, p: Int, year: Int): Int =
  if p0 > p then year
  else nbYearTail((p0 + (p0*(percent*0.01)).toInt+aug), percent, aug, p, year+1)

def nbYearRec(p0: Int, percent: Double, aug: Int, p: Int) =
  nbYearTail(p0, percent, aug, p, 0)


nbYear(1500, 5.0, 100, 5000)
nbYearRec(1500, 5.0, 100, 5000)
nbYear(1500000, 2.5, 10000, 2000000)
nbYearRec(1500000, 2.5, 10000, 2000000)