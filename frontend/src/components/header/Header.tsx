import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";
import { observer } from "mobx-react-lite";
import Nav from "react-bootstrap/Nav";
import "bootstrap/dist/css/bootstrap.css";
import youtube_icon from "../../img/youtube.svg";
import logout_icon from "../../img/logout.svg";
import profile_icon from "../../img/profile.svg";
import home_icon from "../../img/home.svg";
import { Form, Row, Col, Button } from "react-bootstrap";
import { Context } from "../..";
import { useContext, useEffect } from "react";

const Header: React.FC = () => {
  const { store } = useContext(Context);

  return (
    <Nav
      className="navbar navbar-expand-lg navbar-light justify-content-between"
      style={{ background: "#e3f2fd" }}
    >
      <Navbar.Brand>
        <img
          alt=""
          src={youtube_icon}
          width="30"
          height="30"
          className="d-inline-block align-top"
        />{" "}
        Youtube аналитика
      </Navbar.Brand>
      <Form>
        <Col>
          <Button variant="light">
            <img alt="" width="30" height="30" src={home_icon} />
          </Button>
          <Button variant="light">
            <img alt="" width="30" height="30" src={profile_icon} />
          </Button>
          <Button variant="light" onClick={() => store.logout()}>
            <img alt="" width="30" height="30" src={logout_icon} />
          </Button>
        </Col>
      </Form>
    </Nav>
  );
};

export default observer(Header);
