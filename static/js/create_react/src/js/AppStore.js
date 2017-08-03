import { autorun, computed, observable } from "mobx"


class Theme {
  @observable id
  @observable name
  @observable description

  constructor(id, name, description)
  {
    this.id = id
    this.name = name
    this.description = description
  }
}

class Category {
  @observable id
  @observable name
  @observable theme
  @observable description
  @observable applications
  //@observable rank

  constructor(id, name, theme, description, applications){
    this.id = id;
    this.name = name;
    this.theme = theme;
    this.description = description;
    this.applications = applications;
    //this.rank = rank;
  }
}

class AppStore {
  @observable categoryList = []
  @observable currentTheme = null

  loadApps() {
    var qs = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=', 2);
            if (p.length == 1)
                b[p[0]] = "";
            else
                b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'));

    fetch('/api/category/').then(function(response) {
      return response.json()
    }).then(function(json) {
      var arr = Object.values(json);
      arr.sort(function(a, b) {
        return a.rank - b.rank;
      });
      for (var obj in arr) {
        let newCategory = new Category(arr[obj].id, arr[obj].name, arr[obj].theme, arr[obj].description, arr[obj].applications)
        this.categoryList.push(newCategory);
      }
    }.bind(this)).catch(function(ex) {
      console.log('parsing failed', ex)
    });
    let themeNum = qs["theme"];
    console.log('themeNum', themeNum)
    fetch(`/api/theme/${themeNum}`).then(function(response) {
      return response.json()
    }).then(function(json) {
      var arr = Object.values(json);
      console.log('themeArr', arr);
      /* single entry array for loop */
      for (var obj in arr) {
        let newTheme = new Theme(arr[obj].id, arr[obj].name, arr[obj].description)
        this.currentTheme = newTheme;
      }
    }.bind(this)).catch(function(ex) {
      console.log('parsing failed', ex)
    });

  }



}


var store = window.store = new AppStore
export default store

// autorun(() => {
//   console.log(store.filter);
//   console.log(store.todos[0]);
// })
