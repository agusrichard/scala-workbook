package math

import org.scalatest.funsuite.AnyFunSuite

class MathUtilsTests extends  AnyFunSuite:

  test("add is adding") {
    val result = MathUtils.add(1, 2)
    assert(result == 3)
  }