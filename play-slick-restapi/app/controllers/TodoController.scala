package controllers

import javax.inject._
import play.api.mvc._
import play.api.libs.json._
import models.Todo
import repositories.TodoRepository

import scala.concurrent.{ExecutionContext, Future}

@Singleton
class TodoController @Inject()(val controllerComponents: ControllerComponents, todoRepository: TodoRepository)(implicit ec: ExecutionContext) extends BaseController {
  def getTodos: Action[AnyContent] = Action.async( {
    todoRepository.list().map { todos =>
      Ok(Json.toJson(todos))
    }
  })

  def createTodo: Action[JsValue] = Action.async(parse.json) { request =>
    request.body.validate[Todo].fold(
      _ => Future.successful(BadRequest(Json.obj("error" -> "Invalid todo data"))),
      user => {
        todoRepository.create(user).map { createdUser =>
          Created(Json.toJson(createdUser))
        }
      }
    )
  }

  def getTodo(id: Int): Action[AnyContent] = Action.async {
    todoRepository.get(id).map {
      case Some(todo) => Ok(Json.toJson(todo))
      case None => NotFound(Json.obj("error" -> "Todo not found"))
    }
  }

  def updateTodo(id: Int): Action[JsValue] = Action.async(parse.json) { request =>
    request.body.validate[Todo].fold(
      _ => Future.successful(BadRequest(Json.obj("error" -> "Invalid todo data"))),
      todo => {
        todoRepository.update(id, todo).map {
          case 0 => NotFound(Json.obj("error" -> "Todo not found"))
          case _ => Ok(Json.toJson(todo))
        }
      }
    )
  }

  def deleteTodo(id: Int): Action[AnyContent] = Action.async {
    todoRepository.delete(id).map {
      case 0 => NotFound(Json.obj("error" -> "Todo not found"))
      case _ => NoContent
    }
  }
}
