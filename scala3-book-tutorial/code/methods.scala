def multiplyList(nums: List[Int], multiplier: Int): List[Int] =
  nums.map(_ * multiplier)

def simpleSummation(nums: List[Int]): Int =
  var acc = 0
  for i <- nums do acc += i
  acc

@main def methods() =
  println(multiplyList(List(1, 2, 3, 4, 5), 10))
  println(simpleSummation(List(1,2,3,4,5)))
