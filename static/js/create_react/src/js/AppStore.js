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
  @observable rank

  constructor(id, name, theme, description, applications, rank=100){
    this.id = id;
    this.name = name;
    this.theme = theme;
    this.description = description;
    this.applications = applications;
    this.rank = rank;
  }
}

class AppStore {
  @observable categoryList = []
  @observable currentTheme
  @observable currentThemeNum
  @observable appList = []
  @observable isLoading = true;

  constructor() {
    this.loadCategories();
  }

  @action
  loadCategories() {
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
      let arr2 = [];
      console.log('arr', arr);
      for (var obj in arr) {
        console.log('arr[obj].id', arr[obj].id);
        arr2[arr[obj].id] = arr[obj];
      }
      console.log('arr2', arr2);
      this.appList = arr2;
      console.log('this.appList internal', this.appList);
    }.bind(this)).catch(function(ex) {
      console.log('parsing failed', ex)
    });
    fetch('/api/category/').then(function(response) {
      return response.json()
    }).then(function(json) {
      var arr = Object.values(json);
      arr.sort(function(a, b) {
        return a.rank - b.rank;
      });
      console.log(arr);
      for (var obj in arr) {
        let newCategory = new Category(arr[obj].id, arr[obj].name, arr[obj].theme, arr[obj].description, arr[obj].applications, arr[obj].rank)
        console.log('newCategory', newCategory);
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
      console.log('theme json', json);
      let newTheme = new Theme(json.id, json.name, json.description)
      this.currentTheme = newTheme;
      console.log('currentTheme', this.currentTheme);
      this.currentThemeNum = json.id
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
