import { makeAutoObservable } from "mobx";
import AuthService from "../services/AuthService";
import axios from "axios";
import { AuthResponse } from "../models/response/AuthResponse";
import { API_URL } from "../http";
import ProfileService from "../services/ProfileService";
import { IProfile } from "../models/IProfile";
import GroupService from "../services/GroupService";
import { IVideoGroup } from "../models/IVideoGroup";
import { IChannelGroup } from "../models/IChannelGroup";

export default class Store {
  isAuth = false;
  isLoading = false;
  profile = {} as IProfile;
  videoGroups = [] as Array<IVideoGroup>;
  channelGroups = [] as Array<IChannelGroup>;

  constructor() {
    makeAutoObservable(this);
  }

  setAuthState(state: boolean) {
    this.isAuth = state;
  }

  setLoading(state: boolean) {
    this.isLoading = state;
  }

  setProfile(profile: IProfile) {
    this.profile = profile;
  }

  setChannelGroups(channelGroups: Array<IChannelGroup>) {
    this.channelGroups = channelGroups;
  }

  setVideoGroups(videoGroups: Array<IVideoGroup>) {
    this.videoGroups = videoGroups;
  }

  addChannelGroup(channelGroup: IChannelGroup) {
    this.channelGroups.push(channelGroup);
  }

  addVideoGroup(videoGroup: IVideoGroup) {
    this.videoGroups.push(videoGroup);
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

  async getProfile() {
    try {
      const response = await ProfileService.profile();
      this.setProfile({
        email: response.data.email,
        username: response.data.username,
      });
    } catch (e: any) {
      console.log(e.response?.data?.message);
    }
  }

  async changePassword(oldPass: string, newPass: string) {
    try {
      await ProfileService.changePassword(oldPass, newPass);
    } catch (e: any) {
      console.log(e.response?.data?.message);
    }
  }

  async createGroup(title: string, type: string) {
    try {
      const response = await GroupService.createGroup(title, type);

      if (type === "channel") this.addChannelGroup(response.data);
      else if (type === "video") this.addVideoGroup(response.data);
    } catch (e: any) {
      console.log(e.response?.data?.message);
    }
  }

  async getGroups(type: string) {
    try {
      if (type === "channel") {
        const response = await GroupService.getChannelGroups();
        this.setChannelGroups(response.data);
      } else if (type === "video") {
        const response = await GroupService.getVideoGroups();
        this.setVideoGroups(response.data);
      }
    } catch (e: any) {
      console.log(e.response?.data?.message);
    }
  }
}
