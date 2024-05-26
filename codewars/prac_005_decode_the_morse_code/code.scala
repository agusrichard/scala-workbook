object MorseDecoder {
  import MorseCodes.morseCodes

  def decode(msg: String): String = {
    val words = msg.trim.split("   ") // split for words

    val decodedWords = for word <- words yield {
      val chars = word.split(" ") // split for characters
      val decodedChars = for char <- chars yield morseCodes(char)
      decodedChars.mkString
    }

    decodedWords.mkString(" ")
  }
}
