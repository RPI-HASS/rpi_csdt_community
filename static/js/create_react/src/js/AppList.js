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

  renderApplication(app) {

  }

  render() {
    const { categoryList, currentThemeNum, currentTheme, appList, themeList } = this.props.store;
    //const todoList = filteredTodos.map((todo, i) => (<li key={todo.id}><input type="checkbox" value={todo.complete } onChange={this.toggleComplete.bind(this, todo)} checked={todo.complete}/>{todo.value} </li>));
    console.log('currentThemeNum', currentThemeNum);
    console.log('appList', appList);
    const currentList = categoryList.map((category, i) => {
        if (category.theme === currentThemeNum) {
          console.log('category.applications', category.applications)

          const fullArray = category.applications.map((app, i) => {
            if (app != undefined) {
              if (appList[app]) {
                console.log('inside loop app', app);
                console.log('applist[app]', appList[app]);
                return appList[app];
              }
              else {
                console.log('no appList')
              }
            }
          })
          console.log('fullarray', fullArray);
          fullArray.sort(function(a, b) {
            return a.rank - b.rank;
          });

          const objects = fullArray.map((app, i) => {
              return <li key={app.id}><img src={app.screenshot} />{app.name}</li>
          })
          return <li key={category.id}>{category.name}<ul>{objects}</ul></li>
      } else {
        return null;
      }
    });
    console.log('themeList', themeList);
    const currentThemeList = themeList.map((theme, i) => {
      console.log('theme', theme);
      if (theme != undefined ) {
        return <li><button value={theme.name} >{theme.name}</button></li>
      }
    });

    console.log('currentTheme', currentTheme);
    return (
            <div>
              <h1>Categories</h1>

              <ul>{currentThemeList}</ul>

              <ul>{ currentList }</ul>

          </div>

          )
  }
}
