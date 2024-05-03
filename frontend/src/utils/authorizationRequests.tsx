export interface UserDetail {
    emailOrUsername: string,
    password: string,
}

class AuthRequests {

    baseUrl = 'http://localhost:8080/';

    async checkIfEmailExists(email: string): Promise<boolean> {
        const response = await fetch(this.baseUrl + 'checkEmail/' + email, {
            method: 'GET',
        });
        const result = await response.json();
        if (result.status === 'exists') {
            console.log("Email already exists!");
            return true;
        } else {
            console.log("Email does not exist.");
            return false;
        }
    }
    
    async checkIfUsernameExists(username: string): Promise<boolean> {
        const response = await fetch(this.baseUrl + 'checkUsername/'+username, {
            method: 'GET',
        }) ;
        const result = await response.json();
        if (result.status === 'exists') {
            console.log("Username already exists!");
            return true;
        } else {
            console.log("Username does not exist.");
            return false;
        }
    }
    
    async createUser(userDetails: UserDetail): Promise<boolean> {
        const response = await fetch(this.baseUrl + 'addUser/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userDetails)
        }) ;
        const result = await response.json();
        if (result.status === 'success') {
            console.log("User has been added successfully!");
            return true;
        } else {
            console.log("Failed to add the user.");
            return false;
        }
    }
    
    async checkCredentials(credentials: UserDetail): Promise<boolean> {
        const response = await fetch(this.baseUrl + 'checkCredentials/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials)
        }) ;
        const result = await response.json();
        if (result.status === 'success') {
            console.log("Username and password are correct!");
            return true;
        } else {
            console.log("Failed to login. Invalid username or password.");
            return false;
        }
    }
    

}

export default AuthRequests;