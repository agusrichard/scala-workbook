def multiplyList(nums: List[Int], multiplier: Int): List[Int] =
  nums.map(_ * multiplier)

@main def methods() =
  println(multiplyList(List(1, 2, 3, 4, 5), 10))
