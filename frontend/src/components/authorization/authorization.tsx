import React, { Component } from "react";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import Register from "./register";
import Login from "./login";
import "react-tabs/style/react-tabs.css";
import "../../style/authorization.css";


export default class Authorization extends Component {
  render() {
    return (
      <div className="authorization">
        <Tabs className="tab">
          <TabList>
          <Tab className="tab-item">Войти</Tab>
            <Tab className="tab-item">Регистрация</Tab>
          </TabList>
          <TabPanel>
            <Login />
          </TabPanel>
          <TabPanel>
            <Register />
          </TabPanel>
        </Tabs>
      </div>
    );
  }
}
