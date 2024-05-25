def countRedBeads(blueBeads: Int): Int =
  if blueBeads == 0 then return 0
  else if blueBeads == 1 then return 0

  return (blueBeads - 1) * 2

  