import React, { Component } from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import Register from "./register";
import Login from "./login";
import "react-tabs/style/react-tabs.css";
import "../../style/tab.css";
import "../../style/authorization.css";

export default class Authorization extends Component {
  constructor() {
    super({});
  }

  render() {
    return (
      <div className="home">
        <Tabs className="tab">
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
