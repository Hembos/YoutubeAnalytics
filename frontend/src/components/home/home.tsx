import React, { Component } from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import Register from "./register";
import Login from "./login";

export default class Home extends Component {
  constructor() {
    super({});
  }

  render() {
    return (
      <div>
        <Tabs>
          <TabList>
            <Tab>Регистрация</Tab>
            <Tab>Войти</Tab>
          </TabList>

          <TabPanel>
            <Register />
          </TabPanel>
          <TabPanel>
            <Login />
          </TabPanel>
        </Tabs>
      </div>
    );
  }
}
