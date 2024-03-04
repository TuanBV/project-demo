import RestClient from './rest-client';

export default class BaseRepository {
  client;

  constructor(servicePath, version = 'v1') {
    this.client = new RestClient(servicePath, version);
  }
}
