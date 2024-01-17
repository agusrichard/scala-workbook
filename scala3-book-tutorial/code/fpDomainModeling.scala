enum Sex:
    case Male, Female

case class Person(
    name: String,
    age: Int,
    sex: Sex,
    occupation: String
)

@main def fpDomainModeling() =
    val ara = Person("Damara Astiningtyas", 23, Sex.Female, "Student")
    println(ara)
    val rara = ara.copy(occupation = "Businesswoman")
    println(rara)
