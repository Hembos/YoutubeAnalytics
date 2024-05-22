import { makeAutoObservable } from "mobx";
import AuthService from "../services/AuthService";
import axios from "axios";
import { AuthResponse } from "../models/response/AuthResponse";
import { API_URL } from "../http";

export default class Store {
  isAuth = false;
  isLoading = false;

  constructor() {
    makeAutoObservable(this);
  }

  setAuthState(state: boolean) {
    this.isAuth = state;
  }

  setLoading(state: boolean) {
    this.isLoading = state;
  }

  async login(emailOrUsername: string, password: string) {
    try {
      const response = await AuthService.login(emailOrUsername, password);
      console.log(response);
      localStorage.setItem("token", response.data.token);
      this.setAuthState(true);
    } catch (e: any) {
      console.log(e.response?.data?.message);
    }
  }

  async signup(email: string, username: string, password: string) {
    try {
      await AuthService.signup(email, username, password);
    } catch (e: any) {
      console.log(e.response?.data?.message);
    }
  }

  async logout() {
    try {
      await AuthService.logout();
      localStorage.removeItem("token");
      this.setAuthState(false);
    } catch (e: any) {
      console.log(e.response?.data?.message);
    }
  }

  async checkAuth() {
    this.setLoading(true);

    try {
      const response = await axios.post<AuthResponse>(
        `${API_URL}/refresh/`,
        {},
        {
          withCredentials: true,
        }
      );
      localStorage.setItem("token", response.data.token);
      this.setAuthState(true);
    } catch (e: any) {
      console.log(e.response?.data?.message);
    } finally {
      this.setLoading(false);
    }
  }
}
