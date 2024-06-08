package models

import slick.jdbc.PostgresProfile.api._
import java.time.LocalDateTime

class TodoTable(tag: Tag) extends Table[Todo](tag, "todos") {
  def id = column[Int]("id", O.PrimaryKey, O.AutoInc)
  def time = column[LocalDateTime]("time")
  def description = column[String]("description")

  override def * = (id.?, time, description) <> ((Todo.apply _).tupled, Todo.unapply)
}

object TodoTable {
  val todos = TableQuery[TodoTable]
}