import { observer } from "mobx-react-lite";
import "bootstrap/dist/css/bootstrap.css";

interface Props {}

const ChannelGroup: React.FC<Props> = (props: Props) => {
  return (
    <>
      <div
        className="mx-3 border border-primary"
        style={{ width: "100wh", height: "30vh" }}
      ></div>
    </>
  );
};

export default observer(ChannelGroup);
