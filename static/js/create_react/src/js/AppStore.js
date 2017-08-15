import { autorun, computed, observable, action } from "mobx"


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
  @observable rankCat

  constructor(id, name, theme, description, applications, rankCat=100){
    this.id = id;
    this.name = name;
    this.theme = theme;
    this.description = description;
    this.applications = applications;
    this.rankCat = rankCat;
  }
}

class AppStore {
  @observable categoryList = []
  @observable currentTheme
  @observable currentThemeNum
  @observable themeList = []
  @observable appList = []
  @observable isLoading = true;

  constructor() {
    this.loadCategories();
  }

  post (id) {
    this.currentThemeNum = id
  }

  @action
  loadCategories() {
    this.isLoading = true;
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
    fetch(`/api/application/`).then(function(response) {
      return response.json()
    }).then(function(json) {
      var arr = Object.values(json);
      // arr.sort(function(a, b) {
      //   return a.rankApp - b.rankApp;
      // });
      let arr2 = [];
      for (var obj in arr) {
        arr2[arr[obj].id] = arr[obj];
      }
      this.appList = arr2;
      this.isLoading = false;
    }.bind(this)).catch(function(ex) {
      console.log('parsing failed', ex)
    });
    fetch('/api/category/').then(function(response) {
      return response.json()
    }).then(function(json) {
      var arr = Object.values(json);
      arr.sort(function(a, b) {
        return a.rankCat - b.rankCat;
      });
      for (var obj in arr) {
        let newCategory = new Category(arr[obj].id, arr[obj].name, arr[obj].theme, arr[obj].description, arr[obj].applications, arr[obj].rankCat)
        this.categoryList.push(newCategory);
      }
    }.bind(this)).catch(function(ex) {
      console.log('parsing failed', ex)
    });
    let themeNum = qs["theme"] || 1;
    fetch(`/api/theme/`).then(function(response) {
      return response.json()
    }).then(function(json) {
      var arr = Object.values(json);
      // When implemented, uncomment:
      // arr.sort(function(a, b) {
      //   return a.rank - b.rank;
      // });
      for (var obj in arr) {
        let newTheme = new Theme(arr[obj].id, arr[obj].name, arr[obj].description)
        this.themeList.push(newTheme);
      }
    }.bind(this)).catch(function(ex) {
      console.log('parsing failed', ex)
    });
    fetch(`/api/theme/${themeNum}`).then(function(response) {
      return response.json()
    }).then(function(json) {
      let newTheme = new Theme(json.id, json.name, json.description)
      this.currentTheme = newTheme;
      this.currentThemeNum = json.id
    }.bind(this)).catch(function(ex) {
    });


  }

  @action changeTheme(num) {
    fetch(`/api/theme/${num}`).then(function(response) {
      return response.json()
    }).then(function(json) {
      let newTheme = new Theme(json.id, json.name, json.description)
      this.currentTheme = newTheme;
      this.currentThemeNum = json.id
    }.bind(this)).catch(function(ex) {
    });
  }

}


var store = window.store = new AppStore
export default store

// autorun(() => {
//   console.log(store.filter);
//   console.log(store.todos[0]);
// })
