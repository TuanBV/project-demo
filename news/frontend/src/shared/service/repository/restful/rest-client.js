/* eslint-disable class-methods-use-this */
import Axios from 'axios'
import { useAuthStore } from 'stores/auth-store'
import { useAppStore } from 'stores/app-store'
import { STATUS_CODE } from 'utility/const'
import ToastUtil from 'utility/toast'

// merge params to axios config
function mergeAxiosConfig(data, config) {
  const axiosConfig = Object.assign(config || {}, {
    params: data
  })
  return axiosConfig
}

export default class RestClient {
  constructor(version = 'v1') {
    this.client = this.createAxiosClient()
    this.version = version
  }

  createAxiosClient() {
    const axiosInstance = Axios.create({
      baseURL: 'http://localhost:8000',
      headers: {
        'Content-type': 'application/json'
      },
      withCredentials: true
    })

    axiosInstance.interceptors.request.use(this.onRequest, this.onRequestError)

    return axiosInstance
  }

  onRequest = async (config) => config

  onRequestError(error) {
    return Promise.reject(error)
  }

  async extendTokenValidityPeriod() {
    // extend token here
  }

  request(method, url, data, config, setLoading = true) {
    const app = useAppStore()

    return new Promise((resolve, reject) => {
      // show loading
      app.setLoading(setLoading)
      const axiosConfig = Object.assign(config, {
        url: `${this.version}${url}`,
        method,
        data,
        timeout: 0
      })
      this.client
        .request(axiosConfig)
        .then((response) => {
          const result = response.data
          if (result.code === STATUS_CODE.INVALID_REQUEST) {
            const auth = useAuthStore()
            auth.signOut()
          }

          resolve(result)
        })
        .catch((error) => {
          if (Axios.isAxiosError(error)) {
            if (error.response) {
              // The request was made and the server responded with a status code
              // that falls out of the range of 2xx
              if (error.response.data) {
                // error data from server
                const serviceErrorResponse = error.response.data
                ToastUtil.error(error.response.data.message)
                reject(serviceErrorResponse)
              } else {
                reject(error)
              }
            } else if (error.request) {
              // The request was made but no response was received
              // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
              // http.ClientRequest in node.js
              reject(error)
            } else {
              // Something happened in setting up the request that triggered an Error
              reject(error)
            }
          } else {
            reject(error)
          }
        })
        .finally(() => {
          // hide loading
          app.setLoading(false)
        })
    })
  }

  get(url, data, config, setLoading = true) {
    // merge params to axios config
    const axiosConfig = mergeAxiosConfig(data, config)
    return this.request('GET', url, null, axiosConfig, setLoading)
  }

  post(url, data, config) {
    // merge params to axios config
    const axiosConfig = mergeAxiosConfig(data, config)
    delete axiosConfig.params
    return this.request('POST', url, data, axiosConfig)
  }

  put(url, data, config) {
    // merge params to axios config
    const axiosConfig = mergeAxiosConfig(data, config)
    delete axiosConfig.params
    return this.request('PUT', url, data, axiosConfig)
  }

  delete(url, data, config) {
    // merge params to axios config
    const axiosConfig = mergeAxiosConfig(data, config)
    delete axiosConfig.params
    return this.request('DELETE', url, data, axiosConfig)
  }
}
