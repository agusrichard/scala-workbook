package controllers

import javax.inject.*
import play.api.*
import play.api.mvc.*
import play.api.libs.json.*

import scala.collection.mutable.ListBuffer
import models.{NewTodoListItem, TodoListItem}

@Singleton
class TodoListController @Inject()(val controllerComponents: ControllerComponents)
  extends BaseController {
  private val todoList = new ListBuffer[TodoListItem]()
  todoList += TodoListItem(1, "test", true)
  todoList += TodoListItem(2, "some other value", false)

  implicit val todoListJson: OFormat[TodoListItem] = Json.format[TodoListItem]
  implicit val newTodoListJson: OFormat[NewTodoListItem] = Json.format[NewTodoListItem]

  def getAll: Action[AnyContent] = Action {
    if (todoList.isEmpty) {
      NoContent
    } else {
      Ok(Json.toJson(todoList))
    }
  }

  def getById(itemId: Long): Action[AnyContent] = Action {
    val foundItem = todoList.find(_.id == itemId)
    foundItem match {
      case Some(item) => Ok(Json.toJson(item))
      case None => NotFound
    }
  }

  def addNewItem: Action[AnyContent] = Action { implicit request =>
    val content = request.body
    val jsonObject = content.asJson
    val todoListItem: Option[NewTodoListItem] =
      jsonObject.flatMap(
        Json.fromJson[NewTodoListItem](_).asOpt
      )

    todoListItem match {
      case Some(newItem) =>
        val nextId = todoList.map(_.id).max + 1
        val toBeAdded = TodoListItem(nextId, newItem.description, false)
        todoList += toBeAdded
        Created(Json.toJson(toBeAdded))
      case None =>
        BadRequest
    }
  }
}