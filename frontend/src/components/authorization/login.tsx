import React, { useState } from "react";
import AuthRequests from '../../utils/authorizationRequests'; 
import { UserDetail } from "../../utils/authorizationRequests";
const authRequests = new AuthRequests(); 

const Login = () => {
  const [emailOrUsername, setEmailOrUsername] = useState(''); 
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); 

  const handleLogin = async () => { 
    const credentials:UserDetail = {emailOrUsername, password};
    try {
      const isOk: boolean = await authRequests.checkCredentials(credentials);
      if (isOk) { 
        // to do route to main page
        console.log('Login successful'); 
       } else {
        setError('Email/Login does not exist or password is wrong'); 
      }
    }catch(error){
      setError('Server error');
    }
   
  };

  return (
      <div style={{ textAlign: "center" }}>
        <div>
          <input 
            type="text" 
            className="form-input" 
            placeholder="Введите вашу электронную почту или логин" 
            value={emailOrUsername} 
            onChange={e => setEmailOrUsername(e.target.value)} 
          />
        </div>

        <div>
          <input 
            type="password" 
            className="form-input" 
            placeholder="Введите ваш пароль" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
          />
        </div>

        {error && <div>{error}</div>}

        <button onClick={handleLogin} className="btn-primary">Войти</button>
      </div>
  );
};

export default Login;