import React, { Component } from "react";

export default class Register extends Component {
  constructor() {
    super({});
  }

  render() {
    return (
      <div>
        <div>
          <label>Электронная почта</label>
          <br />
          <input type="text" />
        </div>

        <div>
          <label>Логин</label>
          <br />
          <input type="text" />
        </div>

        <div>
          <label>Пароль</label>
          <br />
          <input type="text" />
        </div>

        <button>Зрегистрироваться</button>
      </div>
    );
  }
}
