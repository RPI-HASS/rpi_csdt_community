import React from "react"
import {observer} from "mobx-react"

@observer
export default class AppList extends React.Component {
  filter(e) {
    this.props.store.filter = e.target.value
  }

  createNew(e) {
    if (e.which === 13) {
      this.props.store.createTodo(e.target.value)
      e.target.value = ""
    }
  }

  toggleComplete(todo) {
    todo.complete = !todo.complete
  }

  render() {
    const { filter, clearComplete, filteredTodos, todos } = this.props.store;
    //const todoList = filteredTodos.map((todo, i) => (<li key={todo.id}><input type="checkbox" value={todo.complete } onChange={this.toggleComplete.bind(this, todo)} checked={todo.complete}/>{todo.value} </li>));
    return (
            <div><h1>todos</h1>
            <div><input className = "create" onKeyPress = {this.createNew.bind(this)} /></div>
            <input className="filter" value={filter} onChange={this.filter.bind(this)}/>
            <ul>{ todoList } </ul>
            <a href="#" onClick ={this.props.store.clearComplete} >Clear Complete</a>
          </div>

          )
  }
}
