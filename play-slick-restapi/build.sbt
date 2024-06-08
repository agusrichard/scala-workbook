name := """play-slick-restapi"""

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.13.14"

libraryDependencies ++= Seq(
  guice,
  "com.typesafe.play" %% "play-slick" % "5.3.0",
  "com.typesafe.play" %% "play-slick-evolutions" % "5.3.0",
  "com.typesafe.slick" %% "slick" % "3.5.0",
  "com.typesafe.slick" %% "slick-hikaricp" % "3.5.1",
  "org.postgresql" % "postgresql" % "42.7.3",
  "org.scalatestplus.play" %% "scalatestplus-play" % "7.0.1" % Test
)

// Adds additional packages into Twirl
//TwirlKeys.templateImports += "com.example.controllers._"

// Adds additional packages into conf/routes
// play.sbt.routes.RoutesKeys.routesImport += "com.example.binders._"
