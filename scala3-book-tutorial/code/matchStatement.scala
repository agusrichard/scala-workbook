def tellMeOddity(num: Int) =
    val reminder = num % 2
    reminder match
        case 0 => "Number is even"
        case _ => "Number is odd"
    


@main def matchStatement() =
    val result = tellMeOddity(10)
    println(result)

    