package repositories

import models.{Todo, TodoTable}
import javax.inject.{ Inject, Singleton }
import play.api.db.slick.DatabaseConfigProvider
import slick.jdbc.JdbcProfile

import scala.concurrent.{ Future, ExecutionContext }

@Singleton
class TodoRepository @Inject() (dbConfigProvider: DatabaseConfigProvider)(implicit ec: ExecutionContext) {
  private val dbConfig = dbConfigProvider.get[JdbcProfile]

  import dbConfig._
  import profile.api._

  private val todos = TodoTable.todos

  def list(): Future[Seq[Todo]] = db.run {
    todos.result
  }

  def create(todo: Todo): Future[Todo] = db.run {
    val insertQuery = todos returning todos.map(_.id) into ((todo, id) => todo.copy(id = Some(id)))
    insertQuery += todo
  }

  def get(id: Int): Future[Option[Todo]] = db.run {
    todos.filter(_.id === id).result.headOption
  }

  def update(id: Int, todo: Todo): Future[Int] = db.run {
    val updatedTodo = todo.copy(id = Some(id))
    todos.filter(_.id === id).update(updatedTodo)
  }

  def delete(id: Int): Future[Int] = db.run {
    todos.filter(_.id === id).delete
  }
}
