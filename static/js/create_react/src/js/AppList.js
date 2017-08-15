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

  changeTheme(e) {
    console.log('e', e);
    this.props.store.changeCurrentTheme(e);

  }

  render() {
    const { categoryList, currentThemeNum, appList, isLoading, themeList } = this.props.store;
    //const todoList = filteredTodos.map((todo, i) => (<li key={todo.id}><input type="checkbox" value={todo.complete } onChange={this.toggleComplete.bind(this, todo)} checked={todo.complete}/>{todo.value} </li>));
    


    const currentList = (isLoading) ? <li>Loading...</li> : categoryList.map((category, i) => {
        if (category.theme === currentThemeNum) {
          console.log('category.applications', category.applications)

          const fullArray = category.applications.map((app, i) => {
            if (app != undefined) {
              if (appList[app]) {
                const app1 = appList[app]
                console.log('appList[app] OKAY', app1);
                return app1
              }
              else {
                fetch(`/api/application/${app}`).then(function(response) {
                  return response.json()
                }).then(function(json) {
                  app1 = json
                  return app1
                  //<li key={app1.id}>App #{app1.name}</li>
                }.bind(this)).catch(function(ex) {
                  console.log('parsing failed', ex)
                });
              }
            }
          })
          console.log('fullarray', fullArray);
          fullArray.sort(function(a, b) {
            return a.rankApp - b.rankApp;
          });

          const objects = fullArray.map((app, i) => {
              return <li key={app.id}><a href={app.url}><div className="col-md-2 col-sm-3 col-xs-9" ><div className="bubble"><img className="img-div" src={app.screenshot}/><div className="center-text">{app.name}</div></div></div></a></li>
          })
          return <li key={category.id}><div className="row category"><div className="cat-name">{category.name}</div><ul className="app-ul">{objects}</ul></div></li>
      } else {
        return null;
      }
    });
    const themeOutput = themeList.map((theme, i) => {
      console.log('theme', theme);
        if (theme.id == currentThemeNum) {
            return <button key={theme.id} type="button" className="btn btn-primary themeBtn active" >{theme.name}</button>
        }
        else {
          let hello = theme.id
          return <button key={theme.id} type="button" className="btn btn-default themeBtn" onClick={() => {this.props.store.post(hello)}}>{theme.name}</button>
        }
    });
    console.log('themeList pretest', themeList);
    console.log('currentList', currentList);
    return (
            <div className="container-fluid">
              <div className="row">
                <h1>Applications</h1>
                <h2>Theme</h2>
              </div>
              <div className="row">
                { themeOutput }
              </div>

              <div className="row">
                  <ul className="categories-ul">{ currentList }</ul>
              </div>
            </div>

          )
  }
}
