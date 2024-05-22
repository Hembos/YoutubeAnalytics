import { observer } from "mobx-react-lite";
import "bootstrap/dist/css/bootstrap.css";
import { Form, Button } from "react-bootstrap";
import { Context } from "../..";
import { useContext, useEffect } from "react";

const Profile: React.FC = () => {
  const { store } = useContext(Context);

  useEffect(() => {
    store.getProfile();
  }, []);

  return (
    <Form className="col-lg-5">
      <Form.Group className="my-3 mx-3">
        <Form.Label>Адрес электронной почты</Form.Label>
        <Form.Control
          type="text"
          placeholder={store.profile.email}
          disabled
          readOnly
        />
      </Form.Group>
      <Form.Group className="my-3 mx-3">
        <Form.Label>Логин</Form.Label>
        <Form.Control
          type="text"
          placeholder={store.profile.username}
          disabled
          readOnly
        />
      </Form.Group>
      <Button className="mx-3">Изменить пароль</Button>
    </Form>
  );
};

export default observer(Profile);
