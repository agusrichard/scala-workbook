import java.io.File
import java.nio.file.{Files, Path, Paths}


object CreateCodeChallenge:
  val PATH = "./"

  def main(args: Array[String]): Unit =
    args match
      case Array(input) =>
        val codeChallengeName = getCodeChallengeName(input)
        createDirectory(codeChallengeName)
      case _: Array[?] => 
        println("Please provide a single string argument")

  def getListOfSubDirectories(): List[String] =
    val dir = new File(PATH)
    if dir.exists() && dir.isDirectory then
      dir.listFiles
        .filter(_.isDirectory)
        .map(_.getName)
        .toList
    else
      List.empty[String]

  def getCodeChallengeName(challengeName: String): String =
    val folders = getListOfSubDirectories()
    val codeFolders = folders.filter(_ contains "prac_")
    if codeFolders.length != 0 then
      val nums = codeFolders.map(x => Integer.parseInt(x, 2))
      val maxNum = nums.max+1
      val paddedNum = f"$maxNum%03d"
      val challengeNameConverted = challengeName.replaceAll(" ", "_")
      s"prac_${paddedNum}_${challengeNameConverted}"
    else
      val paddedNum = "001"
      println(challengeName)
      val challengeNameConverted = challengeName.replaceAll(" ", "_")
      s"prac_${paddedNum}_${challengeNameConverted}"

  def createDirectory(filename: String): Unit =
    val folderPath = Paths.get(PATH)
    val completePath = folderPath.resolve(filename)

    if !Files.exists(completePath) then
      Files.createDirectories(completePath)
      println("Directory created successfully")
    else
      println("Directory already exists")

    val filePath = completePath.resolve("code.scala")

    if !Files.exists(filePath) then
      Files.createFile(filePath)
      println("File is created successfully")
    else
      println("file already exists")
