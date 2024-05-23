import $api from "../http";
import { AxiosResponse } from "axios";
import { ChannelGroupResponse } from "../models/response/ChannelGroupResponse";
import { VideoGroupResponse } from "../models/response/VideogroupResponse";

export default class GroupService {
  static async createGroup(
    title: string,
    type: string
  ): Promise<AxiosResponse> {
    if (type === "video")
      return $api.post(`video-group/`, { title, videos: [] });

    return $api.post(`channel-group/`, { title, channel: [] });
  }

  static async getChannelGroups(): Promise<
    AxiosResponse<Array<ChannelGroupResponse>>
  > {
    return $api.get(`channel-group/`);
  }

  static async getVideoGroups(): Promise<
    AxiosResponse<Array<VideoGroupResponse>>
  > {
    return $api.get(`video-group/`);
  }
}
