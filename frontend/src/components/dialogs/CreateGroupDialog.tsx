import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import { observer } from "mobx-react-lite";
import { Form } from "react-bootstrap";

interface Props {
  show: boolean;
  onChangeShowState: (state: boolean) => void;
  onCreateGroup: (title: string, type: string) => void;
}

const CreateGroupDialog: React.FC<Props> = (props: Props) => {
  const [type, setType] = useState("channel");
  const [title, setTitle] = useState("");

  const handleCreate = () => {
    if (title === "") return;

    props.onCreateGroup(title, type);

    setTitle("");
    setType("channel");
    props.onChangeShowState(false);
  };

  return (
    <Modal show={props.show} onHide={() => props.onChangeShowState(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Создание группы</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form.Group>
          <Form.Label>Введите название группы:</Form.Label>
          <Form.Control
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            type="text"
            placeholder="Название группы"
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>Выберите тип группы:</Form.Label>
          <Form.Select
            id="group_type_select"
            value={type}
            onChange={(e) => setType(e.target.value)}
          >
            <option value="channel">Канал</option>
            <option value="video">Видео</option>
          </Form.Select>
        </Form.Group>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleCreate}>
          Создать
        </Button>
        <Button
          variant="primary"
          onClick={() => props.onChangeShowState(false)}
        >
          Отмена
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default observer(CreateGroupDialog);
