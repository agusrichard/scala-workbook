@main def stringInterpolation() =
    val ara = "Damara Astiningtyas"
    val richie = "Agus Richard Lubis"
    val verb = "Loves"
    val sentence = s"${ara} ${verb} ${richie}"
    println(sentence)
    val another = f"${richie} ${verb} ${ara}"
    println(another)