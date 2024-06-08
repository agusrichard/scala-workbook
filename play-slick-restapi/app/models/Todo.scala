package models

import play.api.libs.json._
import java.time.LocalDateTime


case class Todo(id: Option[Int], time: LocalDateTime, description: String)

object Todo {
  implicit val todoFormat: OFormat[Todo] = Json.format[Todo]
}
