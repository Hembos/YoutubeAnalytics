import React, { Component } from "react";

export default class Login extends Component {
  constructor() {
    super({});
  }

  render() {
    return (
      <div>
        <div>
          <label>Электронная почта или логин</label>
          <br />
          <input type="text" />
        </div>

        <div>
          <label>Пароль</label>
          <br />
          <input type="text" />
        </div>

        <button>Войти</button>
      </div>
    );
  }
}
