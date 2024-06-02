import java.io.File
import java.nio.file.{Files, Path, Paths}


val PATH = "./"

@main def CreateCodeChallenge(): Unit =
  print("Please provide code challenge name: ")
  val input = scala.io.StdIn.readLine()
  val codeChallengeName = getCodeChallengeName(input)
  createDirectory(codeChallengeName)

def getListOfSubDirectories(): List[String] =
  val dir = new File(PATH)
  if dir.exists() && dir.isDirectory then
    dir.listFiles
      .filter(_.isDirectory)
      .map(_.getName)
      .toList
  else
    List.empty[String]

def getNumberFromPath(filename: String): Int =
  val pattern = """\d+""".r
  val numericPart = pattern.findFirstIn(filename).getOrElse("0")
  numericPart.toInt

def getCodeChallengeName(challengeName: String): String =
  val folders = getListOfSubDirectories()
  val codeFolders = folders.filter(_ contains "prac_")
  if codeFolders.length != 0 then
    val nums = codeFolders.map(folderName => getNumberFromPath(folderName))
    val maxNum = nums.max+1
    val paddedNum = f"$maxNum%03d"
    val challengeNameConverted = challengeName.replaceAll(" ", "_")
    s"prac_${paddedNum}_${challengeNameConverted}"
  else
    val paddedNum = "001"
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

  val filePath = completePath.resolve("code.sc")

  if !Files.exists(filePath) then
    Files.createFile(filePath)
    println("File is created successfully")
  else
    println("file already exists")

