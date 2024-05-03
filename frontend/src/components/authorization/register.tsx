import React, { useState, useEffect, ChangeEvent } from "react";
import AuthRequests, { UserDetail } from '../../utils/authorizationRequests'; 

const Register: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const [emailErr, setEmailErr] = useState<string>("");
  const [nameErr, setNameErr] = useState<string>("");
  const [passwordErr, setPasswordErr] = useState<string>("");

  const authRequests = new AuthRequests();

  useEffect(() => {
    const fetchData = async () => {
      validateEmail() 
        ? (await checkEmail() 
          ? setEmailErr("") 
          : setEmailErr("Email уже существует" ))
        : setEmailErr("Некорректный email");
      validateName() 
        ? (await checkName() 
          ? setNameErr("") 
          : setNameErr('Имя пользователя занято'))
        : setNameErr("Имя пользователя не может быть пустым");
      validatePassword() 
        ? setPasswordErr("") 
        : setPasswordErr("Пароль должен состоять хотя бы из 6 символов");
    };

    fetchData();
  }, [email, name, password]);

  const validateEmail = ():boolean => (/^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/).test(email);
  const validateName = ():boolean => name.length > 0;
  const validatePassword = ():boolean => password.length >= 6;

  const checkName = async (): Promise<boolean> => {
    try{
      const exists:boolean = await authRequests.checkIfUsernameExists(name);
      return !exists;
    }catch(error){
      console.log("Попытка проверить существование username",error);
      return false;
    }
  }

  const checkEmail = async (): Promise<boolean> => {
    try{
      const exists:boolean = await authRequests.checkIfEmailExists(email);
      return !exists;
    }catch(error){
      console.log("Попытка проверить существование email",error);
      return false;
    }
  }

  const handleRegister = async () => {
    if (!emailErr && !nameErr && !passwordErr) {
      const user: UserDetail = { emailOrUsername: name, password };
      try {
        const success = await authRequests.createUser(user);
        // todo route to main or email conformation
        if (!success) {
          console.log("Failed to register.");
        }
      } catch (error) {
        console.log("Failed to register.", error);
      }
    }
  };

  return (
    <div className="form-container" style={{ textAlign: "center" }}>

      <div className="form-group">
        <input type="text" placeholder="Электронная почта" className="form-input" value={email} onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)} />
        {emailErr && <small style={{ color: "red" }}>{emailErr}</small>}
      </div>

      <div className="form-group">
        <input type="text" placeholder="Логин" className="form-input" value={name} onChange={(e: ChangeEvent<HTMLInputElement>) => setName(e.target.value)} />
        {nameErr && <small style={{ color: "red" }}>{nameErr}</small>}
      </div>

      <div className="form-group">
        <input type="password" placeholder="Пароль" className="form-input" value={password} onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)} />
        {passwordErr && <small style={{ color: "red" }}>{passwordErr}</small>}
      </div>

      <button className={`btn-primary ${!!emailErr || !!nameErr || !!passwordErr ? 'disabled' : ''}`} onClick={handleRegister}>Зарегистрироваться</button>
    </div>
  )
}

export default Register;