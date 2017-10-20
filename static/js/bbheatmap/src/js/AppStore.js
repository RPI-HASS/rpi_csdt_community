import { autorun, computed, observable, action } from "mobx"


// class Theme {
//   @observable id
//   @observable name
//   @observable description
//
//   constructor(id, name, description)
//   {
//     this.id = id
//     this.name = name
//     this.description = description
//   }
// }

class Circle {
  @observable id;
  @observable shots
  @observable makes

  constructor(id){
    this.id = id
    this.shots = 0
    this.makes = 0
  }
}

class AppStore {
  @observable circleList = [];

  constructor() {
    this.circleList = [new Circle(0), new Circle(1), new Circle(2), new Circle(3), new Circle(4),
      new Circle(5), new Circle(6), new Circle(7),
      new Circle(8), new Circle(9), new Circle(10), new Circle(11), new Circle(12), new Circle(13)
    ]
  }
}


var store = window.store = new AppStore
export default store

// autorun(() => {
//   console.log(store.filter);
//   console.log(store.todos[0]);
// })
